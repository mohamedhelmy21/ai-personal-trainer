import random
from app.meal_planner.constants import FORBIDDEN_CARBS, FORBIDDEN_PROTEINS, FORBIDDEN_VEGETABLES, SYNERGY_PAIRS, VEGETABLE_PAIRS_BY_PROTEIN, VEGETABLE_GROUPS
from typing import List, Dict, Any

def is_valid_food(name: str) -> bool:
    """
    Check if a food name is valid (not forbidden).
    """
    name = name.lower()
    if any(x in name for x in FORBIDDEN_PROTEINS | FORBIDDEN_CARBS | FORBIDDEN_VEGETABLES):
        return False
    return True

def get_preferred_carbs_by_category(protein_group: str, synergy_map: Dict[str, List[str]] = SYNERGY_PAIRS) -> Any:
    """
    Get preferred carbs for a given protein group.
    """
    return synergy_map.get(protein_group, None)

def select_contextual_veggies(df: Any, protein_group: str, max_veggies: int = 4) -> List[str]:
    """
    Select contextual vegetables for a protein group.
    """
    allowed = set(VEGETABLE_PAIRS_BY_PROTEIN.get(protein_group, []))
    veg_df = df[df["food_groups"].str.contains("vegetable", case=False, na=False)]
    veg_df = veg_df[
        veg_df["standardized_food_name"].str.lower().isin(allowed)
    ]
    veg_df = veg_df[
        veg_df.apply(lambda row: is_valid_food(row["standardized_food_name"]), axis=1)
    ]
    available = veg_df["standardized_food_name"].str.lower().tolist()
    selected = []
    used_veggies = set()
    used_groups = set()
    for group in ["base", "fresh", "stewable", "salad"]:
        group_options = [v for v in VEGETABLE_GROUPS.get(group, []) if v in available and v not in used_veggies]
        if group_options:
            choice = random.choice(group_options)
            selected.append(choice)
            used_veggies.add(choice)
            used_groups.add(group)
    for group in ["base", "fresh", "stewable", "salad"]:
        if len(selected) >= max_veggies:
            break
        if group in used_groups:
            continue
        group_options = [v for v in VEGETABLE_GROUPS.get(group, []) if v in available and v not in used_veggies]
        if group_options:
            choice = random.choice(group_options)
            selected.append(choice)
            used_veggies.add(choice)
            used_groups.add(group)
    return selected

def select_fruits(df: Any, count: int = 1) -> List[str]:
    """
    Select a number of valid fruits from the dataset.
    """
    fruit_df = df[df["food_groups"].str.contains("fruit", case=False, na=False)]
    fruit_df = fruit_df[fruit_df["standardized_food_name"].apply(is_valid_food)]
    return fruit_df["standardized_food_name"].sample(n=count).tolist() if not fruit_df.empty else []

def tag_meal(meal: dict, df: Any) -> List[str]:
    """
    Tag a meal with dietary and protein tags.
    """
    tags = []
    protein_name = meal["components"].get("protein", "").lower()
    protein_row = df[df["standardized_food_name"].str.lower() == protein_name]
    if not protein_row.empty:
        row = protein_row.iloc[0]
        if row.get("is_high_protein", 0) == 1:
            tags.append("high protein")
        dietary = str(row.get("dietary_tags", "")).lower()
        if "plant" in dietary:
            tags.append("vegetarian")
        elif "animal" in dietary:
            tags.append("animal-based")
    return tags

def get_template_signature(meal: dict) -> tuple:
    """
    Get a unique signature for a meal template.
    """
    comp = meal["components"]
    return (
        comp.get("protein", "").lower(),
        comp.get("carb", "").lower(),
        comp.get("fat", "").lower(),
        tuple(sorted([v.lower() for v in comp.get("vegetables", [])])),
        tuple(sorted([v.lower() for v in comp.get("fruits", [])])),
    )
