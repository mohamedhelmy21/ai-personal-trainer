from app.user import UserProfile
from app.workout_planner.split_generator import WorkoutSplitGenerator

# Example usage for split generator
user = UserProfile(
    age=27,
    gender="male",
    height_cm=180,
    weight_kg=80,
    level="intermediate",
    activity_level="moderate",
    available_equipment=["barbell", "dumbbell", "bodyweight"],
    days_per_week=6,
    goal="fat loss",
    subgoal="recomposition"
)

split_generator = WorkoutSplitGenerator()
weekly_split = split_generator.generate_weekly_split(user)

print("Generated Weekly Split:")
for day in weekly_split["days_assignment"]:
    print(day) 