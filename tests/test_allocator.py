from app.user import UserProfile
from app.meal_planner.portion_allocator import (
    calculate_bmr,
    calculate_tdee,
    determine_macros,
    generate_meal_macros
)

# Step 1: Create a sample user profile
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

# Step 2: Calculate BMR and TDEE
bmr = calculate_bmr(profile)
tdee = calculate_tdee(bmr, profile.activity_level)

# Step 3: Calculate daily macros
daily_macros = determine_macros(profile, tdee)

# Step 4: Generate meal plan for one meal (e.g., lunch)
dataset_path = "data/final_nutrition_data_with_tags.csv"
meal_output = generate_meal_macros(dataset_path, profile, daily_macros, "lunch")

# Step 5: Print results
import json
print(json.dumps(meal_output, indent=2))
