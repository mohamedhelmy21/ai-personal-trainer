# test_portioning_script.py
import json
from app.meal_planner.portioning_engine import portion_all_templates
from app.user import UserProfile

# --------------------------------------
# Define User Profile
# --------------------------------------
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

# --------------------------------------
# File Paths
# --------------------------------------
templates_path = "output/all_meal_templates.json"
nutrition_data_path = "data/final_nutrition_data_with_tags.csv"
output_path = "portioned_meal_templates.json"

# --------------------------------------
# Run Portioning
# --------------------------------------
print("🚀 Portioning meals based on user profile...")
meals = portion_all_templates(templates_path, nutrition_data_path, user)

# Save to file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(meals, f, indent=2, ensure_ascii=False)

print(f"✅ Portioning complete. Saved {len(meals)} meals to '{output_path}'")
