from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from app.user import UserProfile
from app.meal_planner.planner import generate_week_plan
from app.meal_planner.portioning_engine import portion_all_templates
from app.utils.export import export_json
from app.workout_planner.planner import WeeklyPlanBuilder
from app.workout_planner.registry import TEMPLATE_REGISTRY
from app.rag_layer.meal_validator import validate_meal_plan as rag_validate_meal_plan
from app.rag_layer.workout_validator import validate_workout_plan as rag_validate_workout_plan
from app.rag_layer.chatbot import chat
import pandas as pd
import json

app = FastAPI(title="AI Personal Trainer API", description="Meal & Workout Plan Generation with RAG/Chatbot integration.")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    session_id: str
    user: Dict[str, Any]
    plan: Optional[Dict[str, Any]] = Field(default_factory=dict)
    message: str
    history: List[ChatMessage] = Field(default_factory=list)
    plan_type: Literal["meal", "workout"]


# --- Pydantic Schemas ---
class UserProfileIn(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    level: str
    activity_level: str
    available_equipment: List[str]
    days_per_week: int
    goal: str
    subgoal: str
    meal_frequency: Optional[int] = 3

class PlanRequest(BaseModel):
    user: UserProfileIn
    save: Optional[bool] = False

class PlanValidationRequest(BaseModel):
    plan: Dict[str, Any]
    user: UserProfileIn

# --- Endpoints ---
@app.post("/generate-meal-plan")
def generate_meal_plan(req: PlanRequest):
    """
    Generate a weekly meal plan for the user. Optionally save to output/.
    """
    user = UserProfile(**req.user.dict())
    plan = generate_week_plan(user, "output/portioned_meal_templates.json")
    if req.save:
        export_json(plan, "weekly_meal_plan.json")
    # Attach macros/meal_macros for RAG layer
    return {"plan": plan, "macros": user.macros, "meal_macros": user.meal_macros}

@app.post("/register-and-generate-meal-plan")
def register_and_generate_meal_plan(req: PlanRequest):
    """
    Register user (profile input), generate a weekly meal plan (rule-based),
    automatically validate/refine it with the RAG layer, and return only the RAG-refined plan.
    Ensures meal templates are portioned for the user before plan generation.
    """
    user = UserProfile(**req.user.dict())
    # Step 0: Portion all meal templates for this user (required for plan generation)
    templates = portion_all_templates(
        "output/all_meal_templates.json",
        "data/final_nutrition_data_with_tags.csv",
        user
    )
    # Save the user-specific portioned templates before generating the plan
    export_json(templates, "output/portioned_meal_templates.json")
    # Step 1: Rule-based plan generation
    plan = generate_week_plan(user, "output/portioned_meal_templates.json")
    # Step 2: RAG validation/refinement
    try:
        validated_plan, explanations = rag_validate_meal_plan({"days": plan}, user)
        return {"plan": validated_plan, "explanations": explanations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG validation failed: {e}")

def normalize_workout_plan(plan):
    # If already a list or has 'days', return as-is
    if isinstance(plan, list):
        return plan
    if isinstance(plan, dict):
        if "days" in plan and isinstance(plan["days"], list):
            return plan["days"]
        # If keys are like "Day 1", "Day 2", etc.
        if all(isinstance(k, str) and k.lower().startswith("day") for k in plan.keys()):
            days = []
            for day_label, day_data in plan.items():
                if isinstance(day_data, dict):
                    day_data = dict(day_data)  # copy to avoid mutating input
                    day_data["label"] = day_label  # Optionally keep the label
                days.append(day_data)
            return days
    raise ValueError("Unrecognized workout plan format: expected a list, a dict with 'days', or a dict with day keys.")

@app.post("/register-and-generate-workout-plan")
def register_and_generate_workout_plan(req: PlanRequest):
    """
    Register user (profile input), generate a weekly workout plan (rule-based),
    automatically validate/refine it with the RAG layer, and return only the RAG-refined plan.
    """
    user = UserProfile(**req.user.dict())
    exercise_df = pd.read_csv("data/preprocessed_exercise_dataset.csv")
    # Step 1: Rule-based plan generation
    plan = WeeklyPlanBuilder.generate_weekly_plan(user, exercise_df, TEMPLATE_REGISTRY)
    # Normalize plan structure for validator
    try:
        normalized_days = normalize_workout_plan(plan)
        normalized_plan = {"days": normalized_days}
        validated_plan, explanations = rag_validate_workout_plan(normalized_plan, user)
        return {"plan": validated_plan, "explanations": explanations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG validation failed: {e}")

@app.post("/generate-meal-templates")
def generate_meal_templates(req: PlanRequest):
    """
    Portion all meal templates for the user. Optionally save to output/.
    """
    user = UserProfile(**req.user.dict())
    templates = portion_all_templates(
        "output/all_meal_templates.json",
        "data/final_nutrition_data_with_tags.csv",
        user
    )
    if req.save:
        export_json(templates, "portioned_meal_templates.json")
    return {"templates": templates, "macros": user.macros, "meal_macros": user.meal_macros}

@app.post("/validate-meal-plan")
def validate_meal_plan(req: PlanValidationRequest):
    """
    Pass a plan to the RAG layer for validation and revision.
    """
    user = UserProfile(**req.user.dict())
    try:
        validated_plan, explanations = rag_validate_meal_plan(req.plan, user)
        return {"validated_plan": validated_plan, "explanations": explanations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_trainer(req: ChatRequest):
    current_plan = req.plan
    # If plan is an empty dict (default_factory kicked in because it wasn't provided)
    if not current_plan: 
        plan_file_path = None
        if req.plan_type == "workout":
            plan_file_path = r"e:\ai-personal-trainer\output\weekly_workout_plan.json"
        elif req.plan_type == "meal":
            plan_file_path = r"e:\ai-personal-trainer\output\weekly_meal_plan.json"

        if plan_file_path:
            try:
                with open(plan_file_path, "r") as f:
                    current_plan = json.load(f)
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail=f"Default {req.plan_type} plan file not found at {plan_file_path}")
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail=f"Error decoding default {req.plan_type} plan from {plan_file_path}")
        else:
            # Fallback to an empty dict if plan_type is somehow neither, or if we decide not to load for some types
            current_plan = {}

    reply, updated_plan, updated_history = chat(
        session_id=req.session_id,
        user_profile=req.user,
        plan=current_plan,  # Use the potentially loaded or original plan
        message=req.message,
        plan_type=req.plan_type,
    )
    return {
        "response": reply,
        "plan": updated_plan,
        "history": updated_history,
    }

@app.post("/generate-workout-plan")
def generate_workout_plan(req: PlanRequest):
    """
    Generate a weekly workout plan for the user. Optionally save to output/.
    """
    user = UserProfile(**req.user.dict())
    exercise_df = pd.read_csv("data/preprocessed_exercise_dataset.csv")
    plan = WeeklyPlanBuilder.generate_weekly_plan(user, exercise_df, TEMPLATE_REGISTRY)
    if req.save:
        export_json(plan, "weekly_workout_plan.json")
    return {"plan": plan}

@app.post("/validate-workout-plan")
def validate_workout_plan(req: PlanValidationRequest):
    """
    Pass a workout plan to the RAG layer for validation and revision.
    """
    user = UserProfile(**req.user.dict())
    try:
        validated_plan, explanations = rag_validate_workout_plan(req.plan, user)
        return {"validated_plan": validated_plan, "explanations": explanations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Future: Add /generate-workout-plan, /validate-workout-plan, etc. ---

# --- API Docs available at /docs --- 