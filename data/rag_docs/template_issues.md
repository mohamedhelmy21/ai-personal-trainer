# ⚠️ Known Template Generator Issues

This document outlines recurring flaws in rule-based meal template generation. It is used to help the LLM validator recognize and fix problematic combinations.

## 1. Overuse of Onion or Garlic
- **Detected in:** 1,321 templates
- **Problem:** Onion and garlic appear across almost all meals, even in sweet or light breakfast meals.
- **Fix Recommendation:** Remove from breakfast templates or when paired with oats, yogurt, or fruit.

## 2. Oats Combined with Savory/Vegetable/Fatty Ingredients
- **Detected in:** 108 templates
- **Problem:** Oats were paired with onion, spinach, garlic, cheese, or olive oil.
- **Fix Recommendation:** Keep oats limited to sweet pairings like milk, banana, honey, yogurt.

## 3. Cheese + Bread + Fat (Greasy Meals)
- **Detected in:** 24 templates
- **Problem:** Gouda or cheddar cheese combined with white bread and butter/oil creates high-fat, unbalanced meals.
- **Fix Recommendation:** Limit fat redundancy. Add fresh vegetables or lean protein.

## 4. Dairy + Sautéed Vegetables
- **Detected in:** 108 templates
- **Problem:** Milk or yogurt paired with cooked onion, garlic, or spinach is an unusual and conflicting combination.
- **Fix Recommendation:** Use dairy in cold or sweet meals only. Avoid sautéed vegetable pairings unless in a baked recipe.

## 5. Tuna + Sweet or Breakfast Ingredients
- **Detected in:** Rare but should be avoided
- **Problem:** Tuna paired with oats, banana, or yogurt creates incoherent meal logic.
- **Fix Recommendation:** Limit tuna to savory lunch or dinner meals. Avoid breakfast contexts.
