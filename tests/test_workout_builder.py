from app.workout_planner.registry import TEMPLATE_REGISTRY
from app.workout_planner.builder import WorkoutBuilder
from app.user import UserProfile
import pandas as pd

# Load dataset
df = pd.read_csv("data/preprocessed_exercise_dataset.csv")

# Sample user profile
user = UserProfile(
    age=21,
    gender="male",
    height_cm=172,
    weight_kg=74,
    level="intermediate",
    activity_level="moderately active",
    available_equipment=["bodyweight"],
    days_per_week=5,
    goal="muscle gain",
    subgoal="hypertrophy",
    meal_frequency=3
)

# Generate workout for Push day
day_workout = WorkoutBuilder.generate_day_workout("Push", user, df, TEMPLATE_REGISTRY)

# Output
for ex in day_workout:
    print(f"{ex['name']} — {ex['sets']} sets x {ex['reps']} reps")
