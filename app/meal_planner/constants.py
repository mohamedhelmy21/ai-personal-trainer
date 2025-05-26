MEAL_COMPOSITIONS = {
    "Breakfast": [
        {
            "type": "Breakfast",
            "components": {
                "protein": ["Dairy and Egg Products"],
                "carbs": ["Cereal Grains and Pasta", "Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"],
                "fruits" : ["Fruits and Fruit Juices"]
            }
        },
        {
            "type": "Breakfast",
            "components": {
                "protein": ["Legumes and Legume Products"],
                "carbs": ["Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"], 
            }
        }
    ],
    "Lunch": [
        {
            "type": "Lunch",
            "components": {
                "protein": ["Poultry Products", "Beef Products", "Lamb, Veal, and Game Products", "Finfish and Shellfish Products"],
                "carbs": ["Cereal Grains and Pasta", "Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"],
            }
        },
        {
            "type": "Lunch",
            "components": {
                "protein": ["Legumes and Legume Products"],
                "carbs": ["Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"],
            }
        }
    ],
    "Dinner": [
        {
            "type": "Dinner",
            "components": {
                "protein": ["Poultry Products", "Beef Products", "Lamb, Veal, and Game Products", "Finfish and Shellfish Products"],
                "carbs": ["Cereal Grains and Pasta", "Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"],
            }
        },
        {
            "type": "Dinner",
            "components": {
                "protein": ["Legumes and Legume Products"],
                "carbs": ["Baked Products"],
                "fat": ["olive oil", "butter"],
                "vegetables": ["Vegetables and Vegetable Products"],
            }
        }
    ], 
    "Snack" : [
        {
            "type": "Snack",
            "components": {
                "protein": ["Dairy and Egg Products"],
                "carbs": ["Cereal Grains and Pasta"],
                "fat": ["almonds", "peanuts", "pumpkin seeds"],
                "fruits": ["Fruits and Fruit Juices"]
            }
        }
    ] 
}

FORBIDDEN_PROTEINS = { "peas", "chicken liver", "ghee", "butter", "mozzarella cheese"}


FORBIDDEN_CARBS = {"flour"}

FORBIDDEN_VEGETABLES= {"potato", "sweet potato"}

SYNERGY_PAIRS = {
    "Poultry Products": ["white rice", "pita bread (shami)", "pasta", "tortilla (wrap)"],
    "Beef Products": ["pasta", "potato", "white rice"],
    "Lamb, Veal, and Game Products": ["pasta", "potato", "white rice"],
    "Legumes and Legume Products": ["whole-wheat bread (Baladi)", "pita bread (shami)"],
    "Dairy and Egg Products": ["oats", "white bread", "pita bread (shami)", "whole-wheat bread (Baladi)"],
    "Finfish and Shellfish Products": ["white rice", "pasta"]
}

VEGETABLE_PAIRS_BY_PROTEIN = {
    "Legumes and Legume Products": ["onion", "garlic", "parsley", "carrot", "tomato", "green bell pepper"],
    "Poultry Products": ["garlic", "onion", "red bell pepper", "green bell pepper", "yellow bell pepper", "tomato", "zucchini", "carrot", ],
    "Beef Products": ["onion", "garlic", "carrot", "okra", "eggplant", "zucchini", "cabbage", "spinach"],
    "Lamb, Veal, and Game Products": ["onion", "garlic", "okra", "zucchini", "carrot", "cabbage", "spinach"],
    "Finfish and Shellfish Products": ["lettuce", "parsley", "cucumber"],
    "Dairy and Egg Products": ["tomato", "onion", "parsley","red bell pepper", "yellow bell pepper", "green bell pepper"]
}

VEGETABLE_GROUPS = {
    "base": ["onion", "garlic"],
    "fresh": ["tomato", "cucumber", "lettuce", "parsley"],
    "stewable": ["zucchini", "okra", "eggplant", "carrot", "spinach", "mushroom", "cabbage"],
    "salad": ["red bell pepper", "yellow bell pepper", "green bell pepper"]
}