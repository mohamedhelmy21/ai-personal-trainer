# meal_template_generator.py

import pandas as pd
import random
import json
from app.meal_planner.utils import is_valid_food, get_preferred_carbs_by_category, select_contextual_veggies, tag_meal, select_fruits
import typing

# -----------------------------
# Load nutrition dataset
# -----------------------------
def load_nutrition_dataset(path: str = "data/final_nutrition_data_with_tags.csv") -> pd.DataFrame:
    """
    Load the nutrition dataset from a CSV file.
    """
    return pd.read_csv(path)

# -----------------------------
# Get foods by food group keyword
# -----------------------------
def get_items_by_category(df: pd.DataFrame, group_name: str) -> pd.DataFrame:
    """
    Get foods by food group keyword.
    """
    return df[df["category"].str.contains(group_name, case=False, na=False)]

# -----------------------------
# Generate a single meal from a given template
# -----------------------------
def generate_meal_template(template: dict, df: pd.DataFrame) -> dict:
    """
    Generate a single meal from a given template.
    Returns a meal dictionary.
    Raises Exception if no valid protein or carb is found.
    """
    meal = {"type": template["type"], "components": {}}

    # Gather all protein candidates
    protein_choices = pd.concat([
        get_items_by_category(df, group)
        for group in template["components"]["protein"]
    ])

    # Apply filters
    valid_proteins = protein_choices[
        protein_choices.apply(
             lambda row: is_valid_food(row["standardized_food_name"]), axis = 1)
    ]

    if valid_proteins.empty:
        raise Exception("No valid protein found based on filters.")
    

    selected_protein = valid_proteins.sample(1).iloc[0]
    protein_name = selected_protein["standardized_food_name"]
    protein_group = selected_protein["category"]

    meal["components"]["protein"] = protein_name
    preferred_carb_keywords = get_preferred_carbs_by_category(protein_group)


    # Gather all carb candidates
    carb_choices = pd.concat([
        get_items_by_category(df, group)
        for group in template["components"]["carbs"]
    ])

    # Filter based on macro and validity
    valid_carbs = carb_choices[
        carb_choices.apply(
            lambda row: is_valid_food(row["standardized_food_name"]), axis = 1
        )
    ]

    # If synergy exists, prioritize those
    if preferred_carb_keywords:
        preferred_carbs = valid_carbs[
            valid_carbs["standardized_food_name"].str.lower().apply(
                lambda x: any(pref in x for pref in preferred_carb_keywords)
            )
        ]
        if not preferred_carbs.empty:
            selected_carb = preferred_carbs.sample(1).iloc[0]["standardized_food_name"]
        else:
            selected_carb = valid_carbs.sample(1).iloc[0]["standardized_food_name"]
    else:
        selected_carb = valid_carbs.sample(1).iloc[0]["standardized_food_name"]

    meal["components"]["carb"] = selected_carb




    # Fat (direct string choices)
    meal["components"]["fat"] = random.choice(template["components"]["fat"])


    for macro_type, group_list in template["components"].items():
        if macro_type == "vegetables":
            veggies = select_contextual_veggies(df, protein_group, max_veggies=4)
            meal["components"]["vegetables"] = veggies
            continue

        if macro_type == "fruits":
            fruits = select_fruits(df)
            meal["components"]["fruits"] = fruits
            continue
    
    """"
    # Vegetables
    if not template["components"]["vegetables"]:
        meal["components"]["vegetables"] = None
    else:
        selected_veggies = select_contextual_veggies(df, protein_group, max_veggies=4)
        meal["components"]["vegetables"] = selected_veggies
    
    #Fruits
    if not template["components"]["fruits"]:
        meal["components"]["fruits"] = None
    else:
        fruit_choices = pd.concat([
            get_items_by_category(df, "fruits")
        ])

        selected_fruit = fruit_choices.sample(1).iloc[0]
        fruit_name = selected_fruit["standardized_food_name"]
        meal["components"]["fruits"] = fruit_name
    """

    meal['tags'] = tag_meal(meal, df)
    return meal

# -----------------------------
# Select a random structure from multiple templates
# -----------------------------
def generate_meal_template_for_type(meal_type: str, templates_dict: dict, df: pd.DataFrame) -> dict:
    """
    Select a random structure from multiple templates for a meal type.
    Returns a meal dictionary.
    Raises Exception if no templates are defined for the meal type.
    """
    options = templates_dict.get(meal_type)
    if not options:
        raise ValueError(f"No templates defined for meal type: {meal_type}")
    template = random.choice(options)
    return generate_meal_template(template, df)


