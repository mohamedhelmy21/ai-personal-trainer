from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.user import UserProfile
from app.meal_planner.planner import generate_week_plan
from app.meal_planner.portioning_engine import portion_all_templates
from app.utils.export import export_json
from app.workout_planner.planner import WeeklyPlanBuilder
from app.workout_planner.registry import TEMPLATE_REGISTRY
from app.rag_layer.meal_validator import validate_meal_plan as rag_validate_meal_plan
from app.rag_layer.workout_validator import validate_workout_plan as rag_validate_workout_plan
import pandas as pd

app = FastAPI(title="AI Personal Trainer API", description="Meal & Workout Plan Generation with RAG/Chatbot integration.")

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

class ChatRequest(BaseModel):
    user: UserProfileIn
    plan: Dict[str, Any]
    message: str

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
    """
    Chatbot endpoint for conversational plan editing/queries (placeholder).
    """
    # TODO: Integrate with chatbot + RAG
    # For now, just echo the message and plan
    return {
        "response": f"Chatbot not yet implemented. You said: {req.message}",
        "plan": req.plan
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