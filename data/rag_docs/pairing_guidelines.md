# ✅ Ingredient Pairing Guidelines for Meal Plan Validation

This document is used to guide LLM validation of meal plans by identifying realistic pairings and flagging unnatural ones.

## 🔗 Commonly Paired Ingredients (Extracted from Templates)

### Protein  +  Carb
| Pair | Frequency |
|------|-----------|
| Beef Liver + Pasta | 24 |
| Beef Ribs + Pasta | 24 |
| Beef Shank + Pasta | 24 |
| Ground Beef + White Rice | 23 |
| Beef Shank + White Rice | 23 |
| Beef Steak + Pasta | 23 |
| Ground Beef + Pasta | 23 |
| Beef Liver + White Rice | 22 |
| Beef Steak + White Rice | 22 |
| Lean Ground Beef + White Rice | 22 |

### Protein  +  Fat
| Pair | Frequency |
|------|-----------|
| Chicken Thigh + olive oil | 43 |
| Turkey Breast + butter | 39 |
| Chicken Breast + butter | 38 |
| Chicken Thigh + butter | 37 |
| Dove + olive oil | 37 |
| Dove + butter | 36 |
| Duck Breast + olive oil | 35 |
| Turkey Breast + olive oil | 34 |
| Chicken Breast + olive oil | 33 |
| Duck Breast + butter | 33 |

### Carb  +  Fat
| Pair | Frequency |
|------|-----------|
| Pasta + olive oil | 225 |
| Pasta + butter | 224 |
| White Rice + butter | 222 |
| White Rice + olive oil | 213 |
| Pita Bread (Shami) + butter | 106 |
| Pita Bread (Shami) + olive oil | 103 |
| Oats + olive oil | 54 |
| White Bread + olive oil | 54 |
| White Bread + butter | 54 |
| Oats + butter | 54 |

### Protein  +  Vegetable
| Pair | Frequency |
|------|-----------|
| Chicken Thigh + tomato | 80 |
| Turkey Breast + tomato | 73 |
| Dove + tomato | 73 |
| Chicken Breast + tomato | 71 |
| Duck Breast + tomato | 68 |
| Chicken Thigh + garlic | 42 |
| Chicken Thigh + zucchini | 41 |
| Chicken Thigh + carrot | 39 |
| Chicken Breast + garlic | 38 |
| Chicken Thigh + onion | 38 |

### Carb  +  Vegetable
| Pair | Frequency |
|------|-----------|
| Pasta + garlic | 207 |
| Pasta + onion | 200 |
| White Rice + onion | 199 |
| White Rice + garlic | 194 |
| Pita Bread (Shami) + onion | 158 |
| Pita Bread (Shami) + tomato | 147 |
| Pasta + carrot | 109 |
| Oats + onion | 108 |
| Oats + spinach | 108 |
| White Bread + onion | 108 |

### Fat  +  Vegetable
| Pair | Frequency |
|------|-----------|
| butter + onion | 416 |
| olive oil + onion | 404 |
| butter + tomato | 268 |
| olive oil + tomato | 267 |
| olive oil + garlic | 253 |
| butter + garlic | 248 |
| butter + spinach | 220 |
| olive oil + spinach | 216 |
| butter + carrot | 162 |
| olive oil + carrot | 155 |

## 🚫 Unrealistic or Odd Pairings (To Avoid)

### ❌ Oats with Savory/Fatty Ingredients
- **Avoid**: Oats + onion, oats + garlic, oats + cheese, oats + spinach, oats + olive oil
- **Reason**: Oats are typically eaten sweet. These combinations create conflicting taste and meal context.

### ❌ Cheese + Bread + Butter/Oil
- **Avoid**: Gouda or Cheddar + White Bread + Butter/Olive Oil
- **Reason**: This becomes overly greasy and lacks vegetables or fiber to balance the fat load.

### ❌ Tuna with Breakfast Ingredients
- **Avoid**: Tuna + oats, tuna + banana
- **Reason**: Tuna is a savory lunch protein and clashes with breakfast components.

### ❌ Yogurt or Milk with Sautéed Vegetables
- **Avoid**: Yogurt/Milk + onion, garlic, spinach
- **Reason**: These dairy items are typically used in sweet or cold dishes, not with stir-fried vegetables.
