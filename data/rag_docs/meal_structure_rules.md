# 🍽 Meal Structure Guidelines for AI Plan Validator

This document defines typical, nutritionally balanced meal compositions based on rule-based templates and cultural realism.

## 🥣 Breakfast Meal Structure
**Most common structure:** `protein + carb + fat + vegetables` (108 cases)

### ✅ Recommended Components
- **Protein:** Eggs, Greek yogurt, cottage cheese, feta
- **Carb:** Oats, pita bread, baladi bread, multigrain toast
- **Fat:** Olive oil, nuts, tahini, nut butter
- **Vegetables:** Tomato, cucumber, parsley (light, fresh)
- **Optional:** Fruit (banana, dates), dairy (milk, yogurt)

### ❌ Unnatural Combinations
- Avoid strong savory/fatty vegetables with oats (e.g., onion, spinach)
- Avoid overly greasy setups (e.g., cheese + butter + bread + oil)

## 🍛 Lunch/Dinner Meal Structure
**Most common structure:** `protein + carb + fat + vegetables` (1,297 cases)

### ✅ Recommended Components
- **Protein:** Chicken, beef, fish, lentils, eggs
- **Carb:** Rice, pasta, potatoes, pita bread
- **Fat:** Olive oil, butter (used sparingly), nuts/seeds
- **Vegetables:** Onion, tomato, spinach, zucchini, carrots

### ❌ Common Issues to Flag
- Too many fats (e.g., butter + oil + fatty cheese)
- Lack of vegetables for fiber
- Fruit included in main course without proper pairing

## 🔁 Guiding Rules for Validation
- Each meal should include at least **3 macros** (protein, carb, fat)
- Vegetables or fruit should appear in at least **2 out of 3 meals**
- Ingredients should match the **meal context** (e.g., oats = breakfast)
- Avoid duplicative fats or unbalanced macros