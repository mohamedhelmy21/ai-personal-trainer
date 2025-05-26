# portioning_engine.py
import pandas as pd
from app.user import UserProfile
from typing import Dict, Tuple, Any
from app.meal_planner.portion_allocator import (
    get_meal_macros, 
    PORTION_CONSTRAINTS, 
    calculate_tdee, 
    calculate_bmr, 
    determine_macros,
    identify_food_category,
    get_combo_constraints
)

def portion_meal_template(
    template: Dict,
    df: pd.DataFrame,
    profile: Any,
    daily_macros: Tuple[float, float, float]
) -> Dict:
    """
    Portion a single meal template based on user profile and macros.
    Returns a dictionary with meal details.
    Raises Exception if required food items are not found.
    """
    meal_type = template["type"].lower()
    meal_macros = get_meal_macros(profile, daily_macros, meal_type)
    target_macros = {"protein": meal_macros[0], "fat": meal_macros[1], "carbs": meal_macros[2]}
    result = {
        "type": template["type"],
        "components": {},
        "totals": {"protein_g": 0, "fat_g": 0, "carbs_g": 0, "calories": 0},
        "tags": template.get("tags", [])
    }
    protein_name = template["components"].get("protein", "")
    carb_name = template["components"].get("carb", "")
    def find_food_in_db(food_name, df):
        rows = df[df["standardized_food_name"].str.lower() == food_name.lower()]
        if not rows.empty:
            return rows.iloc[0]
        rows = df[df["standardized_food_name"].str.lower().str.contains(food_name.lower())]
        if not rows.empty:
            return rows.iloc[0]
        return None
    protein_row = find_food_in_db(protein_name, df)
    carb_row = find_food_in_db(carb_name, df)
    protein_category = protein_row["category"] if protein_row is not None else "Unknown"
    carb_category = carb_row["category"] if carb_row is not None else "Unknown"
    combo_constraints = get_combo_constraints(protein_category, carb_category, meal_type)
    for macro_type, item_name in template["components"].items():
        if macro_type == "vegetables":
            veggies = []
            for veg in item_name:
                row = df[df["standardized_food_name"].str.lower() == veg.lower()]
                if row.empty:
                    continue
                portion = 50
                calories = (row.iloc[0]["calories"] * portion) / 100
                veggies.append({
                    "item": veg,
                    "portion": f"{portion}g",
                    "calories": round(calories, 1)
                })
                result["totals"]["calories"] += calories
            result["components"][macro_type] = veggies
        elif macro_type == "fruits":
            fruits = []
            for fruit in item_name:
                row = df[df["standardized_food_name"].str.lower() == fruit.lower()]
                if row.empty:
                    continue
                portion = 100
                calories = (row.iloc[0]["calories"] * portion) / 100
                fruits.append({
                    "item": fruit,
                    "portion": f"{portion}g",
                    "calories": round(calories, 1)
                })
                result["totals"]["calories"] += calories
            result["components"][macro_type] = fruits
        else:
            macro_lookup = "carbs" if macro_type == "carb" else macro_type
            item_row = find_food_in_db(item_name, df)
            if item_row is None:
                raise Exception(f"Could not find {item_name} in nutrition database")
            macro_g = item_row.get(f"{macro_lookup}_g", 0)
            if macro_g == 0:
                if macro_type == "carb":
                    min_p, _ = combo_constraints.get("carbs", (60, 150))
                    grams = min_p
                else:
                    grams = 0
            else:
                grams = (target_macros[macro_lookup] * 100) / macro_g
            if macro_type in ["protein", "carb"]:
                constraint_key = "protein" if macro_type == "protein" else "carbs"
                min_p, max_p = combo_constraints.get(constraint_key, (0, 0))
                grams = max(min(grams, max_p), min_p)
            else:
                group_name = macro_type.capitalize()
                if group_name in PORTION_CONSTRAINTS and meal_type in PORTION_CONSTRAINTS[group_name]:
                    min_p, max_p = PORTION_CONSTRAINTS[group_name][meal_type]
                    grams = max(min(grams, max_p), min_p)
            calories = (item_row["calories"] * grams) / 100
            result["components"][macro_type] = {
                "item": item_name,
                "portion": f"{round(grams)}g",
                "calories": round(calories, 1)
            }
            result["totals"]["protein_g"] += round((item_row["protein_g"] * grams) / 100, 1)
            result["totals"]["fat_g"] += round((item_row["fat_g"] * grams) / 100, 1)
            result["totals"]["carbs_g"] += round((item_row["carbs_g"] * grams) / 100, 1)
            result["totals"]["calories"] += round(calories, 1)
    return result

def portion_all_templates(
    templates_path: str,
    nutrition_data_path: str,
    profile: UserProfile
) -> list:
    """
    Portion all meal templates for a user profile.
    Returns a list of portioned meal templates.
    Raises Exception if any error occurs during processing.
    Also sets daily macros and per-meal macros on the user profile.
    """
    df = pd.read_csv(nutrition_data_path)
    with open(templates_path, "r", encoding="utf-8") as f:
        import json
        templates = json.load(f)
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(bmr, profile.activity_level)
    daily_macros = determine_macros(profile, tdee)
    # Save daily macros to user profile
    profile.set_macros({
        "protein_g": daily_macros[0],
        "fat_g": daily_macros[1],
        "carbs_g": daily_macros[2],
        "tdee": daily_macros[3] if len(daily_macros) > 3 else tdee
    })
    # Save per-meal macros to user profile
    meal_types = ["breakfast", "lunch", "dinner", "snack"]
    meal_macros = {}
    for meal_type in meal_types:
        try:
            macros = get_meal_macros(profile, daily_macros, meal_type)
            meal_macros[meal_type] = {
                "protein_g": macros[0],
                "fat_g": macros[1],
                "carbs_g": macros[2]
            }
        except Exception:
            continue
    profile.set_meal_macros(meal_macros)
    portioned = []
    for meal in templates:
        result = portion_meal_template(meal, df, profile, daily_macros)
        portioned.append(result)
    return portioned
