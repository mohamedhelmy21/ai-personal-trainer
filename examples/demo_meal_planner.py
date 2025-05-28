from app.user import UserProfile
from app.meal_planner.planner import generate_week_plan
from app.utils.export import export_json

# Example usage for meal planner
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

weekly_plan = generate_week_plan(user, "data/portioned_meal_templates.json")
export_json(weekly_plan, "weekly_meal_plan.json") 