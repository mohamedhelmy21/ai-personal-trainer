import json
import random
from typing import List, Dict, Tuple
from app.meal_planner.portioning_engine import calculate_bmr, calculate_tdee, determine_macros
from app.user import UserProfile


# -------------------------------
# Load Portioned Meals
# -------------------------------
def load_portioned_meals(path: str) -> Dict[str, List[Dict]]:
    """
    Load portioned meals from a JSON file and categorize them by meal type.
    """
    with open(path, "r", encoding="utf-8") as f:
        all_meals = json.load(f)

    categorized = {"Breakfast": [], "Lunch": [], "Dinner": []}
    for meal in all_meals:
        m_type = meal.get("type")
        if m_type in categorized:
            categorized[m_type].append(meal)
    return categorized


# -------------------------------
# Utility to Calculate Totals
# -------------------------------
def sum_macros(meals: Dict[str, Dict]) -> Dict:
    """
    Sum macros for a set of meals.
    """
    total = {"calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0}
    for meal in meals.values():
        for k in total:
            total[k] += meal.get("totals", {}).get(k, 0.0)
    return {k: round(v, 1) for k, v in total.items()}


# -------------------------------
# Filter Meals Based on Macro Suitability
# -------------------------------
def filter_meals(meals: List[Dict], macro_targets: Dict[str, float], tolerance: float = 0.25) -> List[Dict]:
    """
    Filter meals based on macro suitability.
    """
    filtered = []
    for meal in meals:
        totals = meal.get("totals", {})
        if not totals:
            continue
        protein_item = meal.get("components", {}).get("protein", {})
        protein_name = ""
        if isinstance(protein_item, dict):
            protein_name = protein_item.get("item", "")
        elif isinstance(protein_item, str):
            protein_name = protein_item
        is_egg_dairy = any(p in protein_name.lower() for p in ["egg", "cheese", "milk", "yogurt"])
        is_fish = any(p in protein_name.lower() for p in ["fish", "salmon", "tuna", "tilapia", "cod"])
        calories_match = abs(totals.get("calories", 0) - macro_targets["calories"]) <= tolerance * macro_targets["calories"]
        if totals.get("calories", 0) < 100:
            continue
        has_protein = totals.get("protein_g", 0) > 5
        has_carbs = totals.get("carbs_g", 0) > 5
        has_fat = totals.get("fat_g", 0) > 3
        if not has_protein or (not has_carbs and not has_fat):
            continue
        if is_egg_dairy or is_fish:
            protein_match = abs(totals.get("protein_g", 0) - macro_targets["protein_g"]) <= tolerance * macro_targets["protein_g"]
            if calories_match and protein_match:
                filtered.append(meal)
        else:
            protein_match = abs(totals.get("protein_g", 0) - macro_targets["protein_g"]) <= tolerance * macro_targets["protein_g"]
            carbs_match = abs(totals.get("carbs_g", 0) - macro_targets["carbs_g"]) <= tolerance * 1.8 * macro_targets["carbs_g"]
            fat_match = abs(totals.get("fat_g", 0) - macro_targets["fat_g"]) <= tolerance * 1.8 * macro_targets["fat_g"]
            if calories_match and protein_match and (carbs_match or fat_match):
                filtered.append(meal)
    return filtered


# -------------------------------
# Save Valid Meals to JSON File
# -------------------------------
def save_valid_meals(valid_meals: Dict[str, List[Dict]], path: str) -> None:
    """
    Save valid meals to a JSON file, organized by meal type.
    """
    output = {}
    for meal_type, meals in valid_meals.items():
        meal_summaries = []
        for meal in meals:
            protein_item = meal.get("components", {}).get("protein", {})
            carb_item = meal.get("components", {}).get("carb", {})
            protein_name = protein_item.get("item", "") if isinstance(protein_item, dict) else protein_item
            protein_portion = protein_item.get("portion", "") if isinstance(protein_item, dict) else ""
            carb_name = carb_item.get("item", "") if isinstance(carb_item, dict) else carb_item
            carb_portion = carb_item.get("portion", "") if isinstance(carb_item, dict) else ""
            meal_summaries.append({
                "protein": protein_name,
                "protein_portion": protein_portion,
                "carb": carb_name,
                "carb_portion": carb_portion,
                "calories": meal.get("totals", {}).get("calories", 0),
                "protein_g": meal.get("totals", {}).get("protein_g", 0),
                "carbs_g": meal.get("totals", {}).get("carbs_g", 0),
                "fat_g": meal.get("totals", {}).get("fat_g", 0)
            })
        output[meal_type] = meal_summaries
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


# -------------------------------
# Generate Single Day Plan
# -------------------------------
def generate_day_plan(
    profile: UserProfile,
    categorized_meals: Dict[str, List[Dict]],
    daily_macros: Tuple[float, float, float],
    tdee: float,
    max_attempts: int = 1000
) -> Dict:
    """
    Generate a single day meal plan for the user profile.
    Raises Exception if unable to generate a valid plan.
    """
    if profile.meal_frequency > 3:
        proportions = {
            "breakfast": 0.25,
            "lunch": 0.35,
            "dinner": 0.30,
            "snack": 0.10
        }
    else:
        proportions = {
            "breakfast": 0.30,
            "lunch": 0.40,
            "dinner": 0.30
        }
    macro_keys = ["protein_g", "fat_g", "carbs_g"]
    expected_macros = {}
    for meal_type, prop in proportions.items():
        expected_macros[meal_type] = {
            "calories": tdee * prop,
            "protein_g": daily_macros[0] * prop,
            "fat_g": daily_macros[1] * prop,
            "carbs_g": daily_macros[2] * prop,
        }
    valid_meals = {}
    for meal_type in ["breakfast", "lunch", "dinner"]:
        pool = categorized_meals.get(meal_type.capitalize(), [])
        macro_target = expected_macros[meal_type]
        valid_meals[meal_type] = filter_meals(pool, macro_target)
    for _ in range(max_attempts):
        if not all(valid_meals.values()):
            break
        selected = {
            "breakfast": random.choice(valid_meals["breakfast"]),
            "lunch": random.choice(valid_meals["lunch"]),
            "dinner": random.choice(valid_meals["dinner"])
        }
        totals = sum_macros(selected)
        if abs(totals["calories"] - tdee) <= (tdee * 0.20):
            return {
                "meals": selected,
                "totals": totals
            }
    raise Exception("Unable to generate valid day plan within macro tolerance.")


# -------------------------------
# Generate Weekly Plan (7 Days)
# -------------------------------
def generate_week_plan(profile: UserProfile, meals_path: str) -> List[Dict]:
    """
    Generate a weekly meal plan for the user profile.
    Returns a list of daily plans.
    """
    categorized_meals = load_portioned_meals(meals_path)
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(bmr, profile.activity_level)
    protein, fat, carbs, adjusted_tdee = determine_macros(profile, tdee)
    daily_macros = (protein, fat, carbs)
    week_plan = []
    for i in range(7):
        day_plan = generate_day_plan(profile, categorized_meals, daily_macros, adjusted_tdee)
        day_plan["date"] = f"Day {i+1}"
        week_plan.append(day_plan)
    return week_plan


# -------------------------------
# Save Plan to JSON
# -------------------------------
def save_week_plan(week_plan: List[Dict], path: str) -> None:
    """
    Save the weekly meal plan to a JSON file.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(week_plan, f, indent=2, ensure_ascii=False)