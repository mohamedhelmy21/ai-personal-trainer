import pandas as pd
import random
from typing import List, Dict, Tuple
from app.user import UserProfile

# --------------------------------------
# Portion Constraints (min, max) by group and meal
# --------------------------------------
PORTION_CONSTRAINTS = {
    "Protein": {
        "breakfast": (100, 150),
        "lunch": (150, 250),
        "dinner": (120, 200),
        "snack": (50, 100)
    },
    "Carb": {
        "breakfast": (60, 150),
        "lunch": (100, 150),
        "dinner": (80, 120),
        "snack": (40, 80)
    },
    "Fat": {
        "breakfast": (10, 15),
        "lunch": (20, 40),
        "dinner": (10, 15),
        "snack": (10, 20)
    },
    "Vegetables": {
        "breakfast": (100, 150),
        "lunch": (150, 300),
        "dinner": (150, 250)
    },
    "Fruits": {
        "snack": (100, 200)
    }
}

# --------------------------------------
# Food Combination Portion Constraints
# --------------------------------------
FOOD_COMBO_CONSTRAINTS = {
    "breakfast": {
        # Dairy/Egg + Grains combinations
        ("Dairy and Egg Products", "Cereal Grains and Pasta"): {
            "protein": (80, 120),   # Lower protein, eggs are dense
            "carbs": (100, 180),    # Higher carbs to compensate
        },
        # Dairy/Egg + Baked products
        ("Dairy and Egg Products", "Baked Products"): {
            "protein": (80, 120),   
            "carbs": (100, 160),    
        },
        # Legumes + Grains
        ("Legumes and Legume Products", "Cereal Grains and Pasta"): {
            "protein": (120, 180),  # Higher protein as legumes are less protein-dense
            "carbs": (60, 120),     # Lower carbs as legumes provide carbs
        },
        # Legumes + Baked products
        ("Legumes and Legume Products", "Baked Products"): {
            "protein": (120, 180),  
            "carbs": (50, 120),    
        }
    },
    "lunch": {
        # Poultry + Grains
        ("Poultry Products", "Cereal Grains and Pasta"): {
            "protein": (120, 250),
            "carbs": (100, 150),
        },
        # Beef + Grains
        ("Beef Products", "Cereal Grains and Pasta"): {
            "protein": (120, 180),  # Lower protein as beef is protein-dense
            "carbs": (120, 180),    # Higher carbs to balance
        },
        # Fish + Grains
        ("Finfish and Shellfish Products", "Cereal Grains and Pasta"): {
            "protein": (140, 220),  # Higher protein as fish has lower calories
            "carbs": (120, 200),    # Higher carbs to reach calorie needs
        },
        # Legumes + Grains
        ("Legumes and Legume Products", "Cereal Grains and Pasta"): {
            "protein": (160, 220),  # Higher protein from legumes needed
            "carbs": (80, 120),     # Lower carbs as legumes provide carbs
        },
        # Poultry + Baked Products
        ("Poultry Products", "Baked Products"): {
            "protein": (120, 180),
            "carbs": (100, 150),
        },
        # Beef + Baked Products
        ("Beef Products", "Baked Products"): {
            "protein": (120, 160),
            "carbs": (120, 180),
        },
        # Fish + Baked Products
        ("Finfish and Shellfish Products", "Baked Products"): {
            "protein": (140, 200),
            "carbs": (120, 200),
        },
        # Legumes + Baked Products
        ("Legumes and Legume Products", "Baked Products"): {
            "protein": (160, 220),
            "carbs": (80, 120),
        }
    },
    "dinner": {
        # Poultry + Grains
        ("Poultry Products", "Cereal Grains and Pasta"): {
            "protein": (100, 160),
            "carbs": (80, 130),
        },
        # Beef + Grains
        ("Beef Products", "Cereal Grains and Pasta"): {
            "protein": (100, 140),
            "carbs": (100, 150),
        },
        # Fish + Grains
        ("Finfish and Shellfish Products", "Cereal Grains and Pasta"): {
            "protein": (120, 180),
            "carbs": (100, 170),
        },
        # Legumes + Grains
        ("Legumes and Legume Products", "Cereal Grains and Pasta"): {
            "protein": (140, 200),
            "carbs": (60, 100),
        },
        # Poultry + Baked Products
        ("Poultry Products", "Baked Products"): {
            "protein": (100, 160),
            "carbs": (80, 130),
        },
        # Beef + Baked Products
        ("Beef Products", "Baked Products"): {
            "protein": (100, 140),
            "carbs": (100, 150),
        },
        # Fish + Baked Products
        ("Finfish and Shellfish Products", "Baked Products"): {
            "protein": (120, 180),
            "carbs": (100, 170),
        },
        # Legumes + Baked Products
        ("Legumes and Legume Products", "Baked Products"): {
            "protein": (140, 200),
            "carbs": (60, 100),
        }
    }
}

# --------------------------------------
# Helper Functions for Combo Constraints
# --------------------------------------
def identify_food_category(food_name: str, df: pd.DataFrame) -> str:
    """Identify the food category of a given food item"""
    rows = df[df["standardized_food_name"].str.lower() == food_name.lower()]
    if rows.empty:
        return "Unknown"
    return rows.iloc[0]["category"]

def get_combo_constraints(protein_category: str, carb_category: str, meal_type: str) -> Dict:
    """Get portion constraints based on food combination"""
    meal_type = meal_type.lower()
    
    # Default constraints if anything fails
    default_constraints = {
        "protein": PORTION_CONSTRAINTS["Protein"].get(meal_type, (100, 150)),
        "carbs": PORTION_CONSTRAINTS["Carb"].get(meal_type, (60, 150))
    }
    
    # Handle unknown categories or meal types gracefully
    if protein_category == "Unknown" or carb_category == "Unknown" or meal_type not in FOOD_COMBO_CONSTRAINTS:
        print(f"WARNING: Using default constraints for {protein_category} + {carb_category} in {meal_type}")
        return default_constraints
    
    # Try direct match
    combo_key = (protein_category, carb_category)
    if combo_key in FOOD_COMBO_CONSTRAINTS[meal_type]:
        print(f"Found direct match for {combo_key} in {meal_type}")
        return FOOD_COMBO_CONSTRAINTS[meal_type][combo_key]
    
    # Try partial match on protein category
    for (p_cat, c_cat), constraints in FOOD_COMBO_CONSTRAINTS[meal_type].items():
        if protein_category in p_cat or p_cat in protein_category:
            if carb_category in c_cat or c_cat in carb_category:
                print(f"Found partial match: {(p_cat, c_cat)} for {(protein_category, carb_category)}")
                return constraints
    
    # Try reverse order
    combo_key = (carb_category, protein_category)
    if combo_key in FOOD_COMBO_CONSTRAINTS[meal_type]:
        print(f"Found reverse match for {combo_key} in {meal_type}")
        return FOOD_COMBO_CONSTRAINTS[meal_type][combo_key]
    
    # Try partial match with categories reversed
    for (p_cat, c_cat), constraints in FOOD_COMBO_CONSTRAINTS[meal_type].items():
        if carb_category in p_cat or p_cat in carb_category:
            if protein_category in c_cat or c_cat in protein_category:
                print(f"Found partial reverse match: {(p_cat, c_cat)} for {(carb_category, protein_category)}")
                return constraints
    
    # If still no match, look for any constraints with the same protein category
    for (p_cat, _), constraints in FOOD_COMBO_CONSTRAINTS[meal_type].items():
        if protein_category in p_cat or p_cat in protein_category:
            print(f"Found protein category match: {p_cat} for {protein_category}")
            return constraints
            
    # Fallback to default constraints for this meal type
    print(f"No match found, using default constraints for {meal_type}")
    return default_constraints

# Manually identified calorie-dense fruits that should count toward macros
CALORIE_DENSE_FRUITS = [
    "Banana", "Dates", "Figs", "Grapes", "Mango", "Guava", "Avocado"
]

# --------------------------------------
# Step 1: Calculate BMR and TDEE
# --------------------------------------
def calculate_bmr(profile: UserProfile) -> float:
    if profile.gender == "male":
        return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    else:
        return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161

def calculate_tdee(bmr: float, activity_level: str) -> float:
    multiplier = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "super active": 1.9
    }
    return bmr * multiplier.get(activity_level, 1.2)

# --------------------------------------
# Step 2: Macro Distribution Based on Goal
# --------------------------------------
def determine_macros(profile: UserProfile, tdee: float) -> Tuple[float, float, float]:
    if profile.goal == "muscle gain":
        tdee = tdee * 1.1
        protein = profile.weight_kg * 2.2
    elif profile.goal == "fat loss":
        tdee -= 500
        protein = profile.weight_kg * 2.0
    else:
        protein = profile.weight_kg * 1.8

    fat = (tdee * 0.25) / 9
    carbs = (tdee - (protein * 4 + fat * 9)) / 4

    return protein, fat, carbs, tdee

# --------------------------------------
# Step 3: Split Daily Macros into Meals
# --------------------------------------
def get_meal_macros(profile: UserProfile, daily_macros: Tuple[float, float, float], meal_type: str) -> Tuple[float, float, float]:
    if profile.meal_frequency > 3:
        split_ratios = {
            "breakfast": 0.25,
            "lunch": 0.35,
            "dinner": 0.30,
            "snack": 0.10
        }
    else:
        split_ratios = {
            "breakfast": 0.30,
            "lunch": 0.40,
            "dinner": 0.30
        }

    ratio = split_ratios.get(meal_type.lower(), 1.0 / profile.meal_frequency)

    return (
        round(daily_macros[0] * ratio, 1),  # protein_g
        round(daily_macros[1] * ratio, 1),  # fat_g
        round(daily_macros[2] * ratio, 1)   # carb_g
    )

# --------------------------------------
# Step 4: Filter Nutrition Dataset by Macro Role & Meal Type
# --------------------------------------
def load_filtered_dataset(path: str, meal_type: str, macro_group: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=["calories", "protein_g", "fat_g", "carbs_g"])

    # Filter by food group and meal tag
    df = df[df["food_groups"].str.contains(macro_group, na=False, case=False)]
    df = df[df["meal_tags"].str.contains(meal_type, na=False, case=False)]

    return df.reset_index(drop=True)

"""
def calculate_portion(item: pd.Series, macro_type: str, target_cals: float, meal_type: str) -> Tuple[float, float, float]:
    if macro_type in ["protein", "fat", "carbs"]:
        total_cal = item["calories"]
        cal_from_protein = item["protein_g"] * 4
        cal_from_fat = item["fat_g"] * 9
        cal_from_carbs = item["carbs_g"] * 4
        cal_from_total_macros = cal_from_protein + cal_from_fat + cal_from_carbs

        if total_cal == 0 or cal_from_total_macros == 0:
            return 0, 0, 0

        ratio = {
            "protein": cal_from_protein / total_cal,
            "fat": cal_from_fat / total_cal,
            "carbs": cal_from_carbs / total_cal
        }[macro_type]



        grams_needed = (target_cals * 100) / total_cal
        score = ratio
    else:
        group_name = macro_type.capitalize()
        if group_name in PORTION_CONSTRAINTS and meal_type in PORTION_CONSTRAINTS[group_name]:
            min_p, max_p = PORTION_CONSTRAINTS[group_name][meal_type]
            grams_needed = (min_p + max_p) / 2
        else:
            grams_needed = 100
        score = 1.0

    calories = (item["calories"] * grams_needed) / 100
    return grams_needed, calories, score

# --------------------------------------
# Step 5: Generate Meal Macro Structure
# --------------------------------------
def generate_meal_macros(dataset_path: str, profile: UserProfile, 
                          daily_macros: Tuple[float, float, float], meal_type: str) -> Dict:

    proportion = 0.3 if meal_type in ["lunch", "dinner"] else 0.2

    macro_calories_targets = {
        "protein": (daily_macros[0] * 4) * proportion,
        "fat": (daily_macros[1] * 9) * proportion,
        "carbs": (daily_macros[2] * 4) * proportion
    }

    meal_structure = {}
    macro_keys = ["protein", "carbs", "fat"]

    if meal_type == "snack":
        macro_keys.append("fruits")
    else:
        macro_keys.append("vegetables")

    total_macros = {"protein": 0.0, "carbs": 0.0, "fat": 0.0}

    for macro in macro_keys:
        macro_group = macro.capitalize() if macro != "fruits" else "Fruits"
        df = load_filtered_dataset(dataset_path, meal_type, macro_group)
        scored_items = []

        for _, row in df.iterrows():
            target_cals = macro_calories_targets.get(macro, 50)
            macro_lookup = macro if macro != "fruits" else "carbs"
            portion_g, cals, score = calculate_portion(row, macro_lookup, target_cals, meal_type)
            if portion_g > 0:
                entry = {
                    "item": row["standardized_food_name"],
                    "portion": f"{portion_g:.0f}g",
                    "calories": round(cals, 1),
                    "score": round(score, 3)
                }
                if macro_lookup in ["protein", "carbs", "fat"]:
                    if macro != "fruits" or any(f in row["standardized_food_name"] for f in CALORIE_DENSE_FRUITS):
                        entry["macro_g"] = round(row[f"{macro_lookup}_g"] * (portion_g / 100), 1)
                scored_items.append(entry)

        scored_items.sort(key=lambda x: x["score"], reverse=True)
        top_items = scored_items

        if macro in total_macros:
            total_macros[macro] += sum([item.get("macro_g", 0.0) for item in top_items])

        for item in top_items:
            item.pop("score", None)
            item.pop("macro_g", None)

        meal_structure[macro] = top_items

    return {
        "meal_type": meal_type,
        "macros": meal_structure,
        "totals": {
            "protein_g": round(total_macros["protein"], 1),
            "carbs_g": round(total_macros["carbs"], 1),
            "fat_g": round(total_macros["fat"], 1)
        }
    }
"""