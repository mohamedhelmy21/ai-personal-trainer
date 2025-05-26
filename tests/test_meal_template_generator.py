import pandas as pd
import json
from app.meal_planner.constants import MEAL_COMPOSITIONS
from app.meal_planner.generator import generate_meal_template_for_type, load_nutrition_dataset
from app.meal_planner.utils import get_template_signature
from app.utils.export import export_json

df = load_nutrition_dataset()

template_limit = 300
global_signatures = set()
global_templates = []

print("📦 Generating meal templates...\n")

for meal_type, variations in MEAL_COMPOSITIONS.items():
    for i, _ in enumerate(variations):
        signatures = set()
        templates = []
        attempts = 0

        while len(templates) < template_limit and attempts < template_limit * 10:
            meal = generate_meal_template_for_type(meal_type, MEAL_COMPOSITIONS, df)
            sig = get_template_signature(meal)

            if sig not in signatures and sig not in global_signatures:
                templates.append(meal)
                signatures.add(sig)
                global_signatures.add(sig)
                global_templates.append(meal)

            attempts += 1

        print(f"✅ {meal_type} (variation {i+1}): {len(templates)} unique templates")

# Save everything
export_json(global_templates, "all_meal_templates.json")

print(f"\n🎉 Total unique templates generated: {len(global_templates)}")
