import sys
import uuid
import json
from app.rag_layer.chatbot import chat

if __name__ == "__main__":
    print("Welcome to the AI Personal Trainer CLI Chat!")
    session_id = str(uuid.uuid4())
    plan_type = input("Plan type (meal/workout): ").strip().lower()
    assert plan_type in ("meal", "workout"), "Plan type must be 'meal' or 'workout'"

    user_profile = {
        "age": 21,
        "gender": "male",
        "height_cm": 172,
        "weight_kg": 63,
        "level": "intermediate",
        "activity_level": "moderately active",
        "available_equipment": [
            "barbell", "dumbbell", "machine", "cable", "bodyweight"
        ],
        "days_per_week": 3,
        "goal": "muscle gain",
        "subgoal": "hypertrophy",
        "meal_frequency": 3
    }
    plan_file = input("Enter the path to your initial plan JSON file: ").strip()
    with open(plan_file, "r") as f:
        plan = json.load(f)

    history = []
    print("Type your message and press Enter. Type 'exit' to quit.")
    while True:
        message = input("You: ").strip()
        if message.lower() == "exit":
            break
        reply, updated_plan, updated_history = chat(
            session_id=session_id,
            user_profile=user_profile,
            plan=plan,
            message=message,
            plan_type=plan_type
        )
        print(f"Bot: {reply}")
        plan = updated_plan
        history = updated_history
