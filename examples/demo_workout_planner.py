from app.user import UserProfile
from app.workout_planner.planner import WeeklyPlanBuilder
from app.workout_planner.registry import TEMPLATE_REGISTRY
import pandas as pd
from app.utils.export import export_json



# Load dataset
exercise_df = pd.read_csv("preprocessed_exercise_dataset.csv")

# Sample user profile
user = UserProfile(
    age=21,
    gender="male",
    height_cm=172,
    weight_kg=63,
    level="intermediate",
    activity_level="moderate",
    available_equipment=["machine", "cable", "dumbells", "treadmill", "mat", "bodyweight", "barbell"],
    days_per_week=5,
    goal="muscle",
    subgoal="hypertrophy"
)

builder = WeeklyPlanBuilder()
# Generate the plan
weekly_plan = builder.generate_weekly_plan(user, exercise_df, TEMPLATE_REGISTRY)

# Pretty-print result
for day, content in weekly_plan.items():
    print(f"\n🗓️ {day}")
    if isinstance(content, str):
        print(f"  {content}")
    else:
        print(f"  Type: {content['type']}")

        # Warmup
        print("  Warm-up:")
        for w in content.get("warmup", []):
            print(f"    - {w['name']} ({w['phase']}) — {w['prescription']}")

        # Workout
        print("  Workout:")
        for ex in content.get("workout", []):
            line = f"    - {ex['name']} — {ex['sets']} sets x {ex['reps']} reps"
            if 'note' in ex:
                line += f" | Note: {ex['note']}"
            print(line)

        # Cooldown
        print("  Cooldown:")
        for c in content.get("cooldown", []):
            print(f"    - {c['name']} — {c['prescription']}")

export_json(weekly_plan, "user_weekly_plan.json")
