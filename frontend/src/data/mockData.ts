// This file contains the mock data for the demo
// In a production environment, this would be replaced with actual API calls

import { WeeklyMealPlan } from '../types/meal';
import { WeeklyWorkoutPlan } from '../types/workout';

// Mock meal plan data
export const mockMealPlan: WeeklyMealPlan = [
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Greek Yogurt", portion: "120g", calories: 126.0 },
          carb: { item: "Oats", portion: "168g", calories: 665.4 },
          fat: { item: "Walnuts", portion: "15g", calories: 105.3 },
          fruits: [{ item: "Figs", portion: "100g", calories: 82.0 }]
        },
        totals: { protein_g: 42.2, fat_g: 26.9, carbs_g: 130.0, calories: 978.7 },
        tags: ["mediterranean", "sweet", "high protein"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Chicken Thigh", portion: "250g", calories: 362.5 },
          carb: { item: "White Rice", portion: "150g", calories: 522.0 },
          fat: { item: "Sunflower Oil", portion: "30g", calories: 273.6 },
          vegetables: [
            { item: "Green Bell Pepper", portion: "50g", calories: 11.0 },
            { item: "Tomato", portion: "50g", calories: 10.5 }
          ]
        },
        totals: { protein_g: 58.0, fat_g: 51.9, carbs_g: 120.0, calories: 1179.6 },
        tags: ["egyptian", "high protein", "variety"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Shrimp", portion: "180g", calories: 151.2 },
          carb: { item: "White Rice", portion: "140g", calories: 488.5 },
          fat: { item: "Vegetable Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Cabbage", portion: "50g", calories: 14.5 },
            { item: "Carrot", portion: "50g", calories: 22.0 }
          ]
        },
        totals: { protein_g: 47.6, fat_g: 18.2, carbs_g: 112.3, calories: 811.2 },
        tags: ["seafood", "fresh", "summer"]
      }
    },
    totals: { calories: 2969.5, protein_g: 147.8, carbs_g: 362.3, fat_g: 97.0 },
    date: "Day 1"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Feta Cheese", portion: "120g", calories: 318.0 },
          carb: { item: "Multigrain Bread", portion: "160g", calories: 422.4 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Tomato", portion: "50g", calories: 10.5 },
            { item: "Green Bell Pepper", portion: "50g", calories: 11.0 }
          ]
        },
        totals: { protein_g: 40.4, fat_g: 49.4, carbs_g: 75.2, calories: 896.9 },
        tags: ["mediterranean", "vegetarian", "balanced"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Shrimp", portion: "220g", calories: 184.8 },
          carb: { item: "White Rice", portion: "187g", calories: 651.6 },
          fat: { item: "Vegetable Oil", portion: "30g", calories: 273.6 },
          vegetables: [
            { item: "Green Bell Pepper", portion: "50g", calories: 11.0 },
            { item: "Carrot", portion: "50g", calories: 22.0 }
          ]
        },
        totals: { protein_g: 59.3, fat_g: 34.5, carbs_g: 149.8, calories: 1143.0 },
        tags: ["mediterranean", "seafood", "fresh"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Talipa (Bulty) Fish", portion: "180g", calories: 171.0 },
          carb: { item: "White Rice", portion: "140g", calories: 488.5 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Broccoli", portion: "50g", calories: 20.5 },
            { item: "Carrot", portion: "50g", calories: 22.0 }
          ]
        },
        totals: { protein_g: 47.6, fat_g: 20.0, carbs_g: 112.3, calories: 837.0 },
        tags: ["fish", "classic", "balanced"]
      }
    },
    totals: { calories: 2876.9, protein_g: 147.3, carbs_g: 337.3, fat_g: 103.9 },
    date: "Day 2"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Fava Beans (Foul)", portion: "154g", calories: 540.8 },
          carb: { item: "Pita Bread (Shami)", portion: "120g", calories: 333.6 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Tomato", portion: "50g", calories: 10.5 },
            { item: "Parsley", portion: "50g", calories: 22.0 }
          ],
          fruits: [
            { item: "Oranges", portion: "100g", calories: 52.0 }
          ]
        },
        totals: { protein_g: 53.6, fat_g: 20.5, carbs_g: 158.1, calories: 1093.9 },
        tags: ["egyptian", "plant-based", "fiber-rich"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Chicken Breast", portion: "241g", calories: 257.7 },
          carb: { item: "White Rice", portion: "150g", calories: 522.0 },
          fat: { item: "Olive Oil", portion: "30g", calories: 273.6 },
          vegetables: [
            { item: "Broccoli", portion: "50g", calories: 20.5 },
            { item: "Carrot", portion: "50g", calories: 22.0 }
          ]
        },
        totals: { protein_g: 65.9, fat_g: 36.7, carbs_g: 120.0, calories: 1095.8 },
        tags: ["universal", "lean protein", "classic"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Eggs", portion: "200g", calories: 276.0 },
          carb: { item: "Whole-Wheat Bread (Baladi)", portion: "120g", calories: 344.4 },
          fat: { item: "Ghee", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Tomato", portion: "50g", calories: 10.5 },
            { item: "Green Bell Pepper", portion: "50g", calories: 11.0 }
          ]
        },
        totals: { protein_g: 36.8, fat_g: 42.2, carbs_g: 64.4, calories: 776.9 },
        tags: ["universal", "high protein", "vegetarian"]
      }
    },
    totals: { calories: 2966.6, protein_g: 156.3, carbs_g: 342.5, fat_g: 99.4 },
    date: "Day 3"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Cottage Cheese", portion: "150g", calories: 163.5 },
          carb: { item: "Granola", portion: "100g", calories: 471.0 },
          fat: { item: "Almonds", portion: "20g", calories: 121.8 },
          fruits: [{ item: "Blueberries", portion: "100g", calories: 57.0 }]
        },
        totals: { protein_g: 38.5, fat_g: 22.3, carbs_g: 85.6, calories: 813.3 },
        tags: ["antioxidant", "high fiber", "balanced"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Beef Steak", portion: "200g", calories: 414.0 },
          carb: { item: "Sweet Potato", portion: "200g", calories: 180.0 },
          fat: { item: "Olive Oil", portion: "20g", calories: 180.0 },
          vegetables: [
            { item: "Spinach", portion: "100g", calories: 23.0 },
            { item: "Mushrooms", portion: "100g", calories: 22.0 }
          ]
        },
        totals: { protein_g: 52.0, fat_g: 32.0, carbs_g: 45.0, calories: 819.0 },
        tags: ["iron-rich", "high protein", "nutrient-dense"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Salmon", portion: "180g", calories: 367.2 },
          carb: { item: "Quinoa", portion: "150g", calories: 180.0 },
          fat: { item: "Avocado", portion: "50g", calories: 80.0 },
          vegetables: [
            { item: "Asparagus", portion: "100g", calories: 20.0 },
            { item: "Bell Peppers", portion: "100g", calories: 31.0 }
          ]
        },
        totals: { protein_g: 45.0, fat_g: 28.0, carbs_g: 40.0, calories: 678.2 },
        tags: ["omega-3", "heart-healthy", "superfood"]
      }
    },
    totals: { calories: 2310.5, protein_g: 135.5, carbs_g: 170.6, fat_g: 82.3 },
    date: "Day 4"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Eggs", portion: "150g", calories: 207.0 },
          carb: { item: "Whole Grain Toast", portion: "80g", calories: 216.0 },
          fat: { item: "Avocado", portion: "50g", calories: 80.0 },
          vegetables: [
            { item: "Spinach", portion: "50g", calories: 11.5 },
            { item: "Tomato", portion: "50g", calories: 10.5 }
          ]
        },
        totals: { protein_g: 27.0, fat_g: 18.0, carbs_g: 30.0, calories: 525.0 },
        tags: ["protein-packed", "heart-healthy", "energy-boosting"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Turkey Breast", portion: "200g", calories: 220.0 },
          carb: { item: "Brown Rice", portion: "150g", calories: 165.0 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Broccoli", portion: "100g", calories: 34.0 },
            { item: "Carrots", portion: "100g", calories: 41.0 }
          ]
        },
        totals: { protein_g: 48.0, fat_g: 20.0, carbs_g: 45.0, calories: 595.0 },
        tags: ["lean protein", "fiber-rich", "balanced"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Tofu", portion: "200g", calories: 176.0 },
          carb: { item: "Soba Noodles", portion: "150g", calories: 231.0 },
          fat: { item: "Sesame Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Bok Choy", portion: "100g", calories: 13.0 },
            { item: "Shiitake Mushrooms", portion: "100g", calories: 34.0 }
          ]
        },
        totals: { protein_g: 30.0, fat_g: 22.0, carbs_g: 50.0, calories: 589.0 },
        tags: ["plant-based", "asian-inspired", "iron-rich"]
      }
    },
    totals: { calories: 1709.0, protein_g: 105.0, carbs_g: 125.0, fat_g: 60.0 },
    date: "Day 5"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Protein Shake", portion: "1 serving", calories: 150.0 },
          carb: { item: "Banana", portion: "120g", calories: 107.0 },
          fat: { item: "Peanut Butter", portion: "30g", calories: 188.0 },
          fruits: [{ item: "Strawberries", portion: "100g", calories: 32.0 }]
        },
        totals: { protein_g: 25.0, fat_g: 16.0, carbs_g: 35.0, calories: 477.0 },
        tags: ["quick", "pre-workout", "energy-boosting"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Grilled Chicken", portion: "200g", calories: 330.0 },
          carb: { item: "Couscous", portion: "150g", calories: 176.0 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Zucchini", portion: "100g", calories: 17.0 },
            { item: "Eggplant", portion: "100g", calories: 25.0 }
          ]
        },
        totals: { protein_g: 50.0, fat_g: 22.0, carbs_g: 40.0, calories: 683.0 },
        tags: ["mediterranean", "lean protein", "fiber-rich"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Lentils", portion: "200g", calories: 230.0 },
          carb: { item: "Basmati Rice", portion: "150g", calories: 195.0 },
          fat: { item: "Coconut Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Cauliflower", portion: "100g", calories: 25.0 },
            { item: "Peas", portion: "100g", calories: 81.0 }
          ]
        },
        totals: { protein_g: 35.0, fat_g: 18.0, carbs_g: 65.0, calories: 666.0 },
        tags: ["plant-based", "high-fiber", "indian-inspired"]
      }
    },
    totals: { calories: 1826.0, protein_g: 110.0, carbs_g: 140.0, fat_g: 56.0 },
    date: "Day 6"
  },
  {
    meals: {
      breakfast: {
        type: "Breakfast",
        components: {
          protein: { item: "Smoked Salmon", portion: "100g", calories: 117.0 },
          carb: { item: "Bagel", portion: "100g", calories: 250.0 },
          fat: { item: "Cream Cheese", portion: "30g", calories: 101.0 },
          vegetables: [
            { item: "Red Onion", portion: "30g", calories: 12.0 },
            { item: "Capers", portion: "10g", calories: 2.0 }
          ]
        },
        totals: { protein_g: 25.0, fat_g: 15.0, carbs_g: 40.0, calories: 482.0 },
        tags: ["omega-3", "weekend", "brunch"]
      },
      lunch: {
        type: "Lunch",
        components: {
          protein: { item: "Grass-fed Beef", portion: "180g", calories: 378.0 },
          carb: { item: "Potato", portion: "200g", calories: 164.0 },
          fat: { item: "Butter", portion: "15g", calories: 108.0 },
          vegetables: [
            { item: "Green Beans", portion: "100g", calories: 31.0 },
            { item: "Carrots", portion: "100g", calories: 41.0 }
          ]
        },
        totals: { protein_g: 45.0, fat_g: 25.0, carbs_g: 35.0, calories: 722.0 },
        tags: ["classic", "comfort food", "nutrient-dense"]
      },
      dinner: {
        type: "Dinner",
        components: {
          protein: { item: "Sea Bass", portion: "180g", calories: 195.0 },
          carb: { item: "Wild Rice", portion: "150g", calories: 166.0 },
          fat: { item: "Olive Oil", portion: "15g", calories: 135.0 },
          vegetables: [
            { item: "Asparagus", portion: "100g", calories: 20.0 },
            { item: "Cherry Tomatoes", portion: "100g", calories: 18.0 }
          ]
        },
        totals: { protein_g: 40.0, fat_g: 20.0, carbs_g: 30.0, calories: 534.0 },
        tags: ["omega-3", "gourmet", "light"]
      }
    },
    totals: { calories: 1738.0, protein_g: 110.0, carbs_g: 105.0, fat_g: 60.0 },
    date: "Day 7"
  }
];

// Mock workout plan data
export const mockWorkoutPlan: WeeklyWorkoutPlan = [
  {
    day: "Day 1",
    focus: "Upper Body",
    exercises: [
      {
        name: "Bench Press",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "barbell",
        instructions: "Lie on bench, lower bar to chest, press up to starting position."
      },
      {
        name: "Pull-ups",
        sets: 3,
        reps: 8,
        rest: "90 seconds",
        equipment: "bodyweight",
        instructions: "Hang from bar, pull body up until chin over bar, lower back down."
      },
      {
        name: "Shoulder Press",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "dumbbell",
        instructions: "Sit with back support, press weights overhead, lower to shoulder level."
      }
    ],
    completed: false
  },
  {
    day: "Day 2",
    focus: "Lower Body",
    exercises: [
      {
        name: "Squats",
        sets: 4,
        reps: 8,
        rest: "120 seconds",
        equipment: "barbell",
        instructions: "Stand with feet shoulder-width apart, lower body by bending knees, return to standing."
      },
      {
        name: "Romanian Deadlift",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "barbell",
        instructions: "Hold bar at hip level, hinge at hips while keeping back straight, return to standing."
      },
      {
        name: "Leg Press",
        sets: 3,
        reps: 12,
        rest: "90 seconds",
        equipment: "machine",
        instructions: "Sit on machine, push platform away by extending knees, return to starting position."
      }
    ],
    completed: false
  },
  {
    day: "Day 3",
    focus: "Full Body",
    exercises: [
      {
        name: "Deadlift",
        sets: 3,
        reps: 6,
        rest: "120 seconds",
        equipment: "barbell",
        instructions: "Stand with feet hip-width apart, bend to grip bar, lift by extending hips and knees."
      },
      {
        name: "Push-ups",
        sets: 3,
        reps: 15,
        rest: "60 seconds",
        equipment: "bodyweight",
        instructions: "Start in plank position, lower chest to floor by bending elbows, push back up."
      },
      {
        name: "Dumbbell Rows",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "dumbbell",
        instructions: "Bend at waist with one hand on bench, pull dumbbell to side of chest, lower back down."
      },
      {
        name: "Lunges",
        sets: 3,
        reps: 12,
        rest: "90 seconds",
        equipment: "bodyweight",
        instructions: "Step forward with one leg, lower body by bending both knees, return to standing."
      }
    ],
    completed: false
  },
  {
    day: "Day 4",
    focus: "Rest/Active Recovery",
    exercises: [
      {
        name: "Light Walking",
        sets: 1,
        reps: 30,
        rest: "0 seconds",
        equipment: "none",
        instructions: "Walk at a comfortable pace for 30 minutes to promote blood flow and recovery."
      },
      {
        name: "Stretching Routine",
        sets: 1,
        reps: 15,
        rest: "0 seconds",
        equipment: "none",
        instructions: "Perform full-body stretching routine, holding each stretch for 15-30 seconds."
      },
      {
        name: "Foam Rolling",
        sets: 1,
        reps: 10,
        rest: "0 seconds",
        equipment: "foam roller",
        instructions: "Roll major muscle groups (quads, hamstrings, back, calves) for 10 passes each."
      }
    ],
    completed: false
  },
  {
    day: "Day 5",
    focus: "Push (Chest, Shoulders, Triceps)",
    exercises: [
      {
        name: "Incline Bench Press",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "dumbbell",
        instructions: "Lie on incline bench, press dumbbells up from shoulder level, lower back down."
      },
      {
        name: "Lateral Raises",
        sets: 3,
        reps: 12,
        rest: "60 seconds",
        equipment: "dumbbell",
        instructions: "Stand with dumbbells at sides, raise arms out to sides until parallel with floor, lower back down."
      },
      {
        name: "Tricep Dips",
        sets: 3,
        reps: 12,
        rest: "60 seconds",
        equipment: "bodyweight",
        instructions: "Support body on parallel bars or bench, lower by bending elbows, push back up."
      },
      {
        name: "Chest Flyes",
        sets: 3,
        reps: 12,
        rest: "60 seconds",
        equipment: "cable",
        instructions: "Stand with cables at chest height, bring handles together in front of chest with slight elbow bend."
      }
    ],
    completed: false
  },
  {
    day: "Day 6",
    focus: "Pull (Back, Biceps)",
    exercises: [
      {
        name: "Lat Pulldown",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "cable",
        instructions: "Sit at machine, grip bar wider than shoulders, pull down to chest level, control return."
      },
      {
        name: "Barbell Rows",
        sets: 3,
        reps: 10,
        rest: "90 seconds",
        equipment: "barbell",
        instructions: "Bend at hips with slight knee bend, pull bar to lower chest, lower with control."
      },
      {
        name: "Bicep Curls",
        sets: 3,
        reps: 12,
        rest: "60 seconds",
        equipment: "dumbbell",
        instructions: "Stand with dumbbells at sides, curl up to shoulder level while keeping elbows fixed, lower back down."
      },
      {
        name: "Face Pulls",
        sets: 3,
        reps: 15,
        rest: "60 seconds",
        equipment: "cable",
        instructions: "Pull rope attachment to face with high elbows, squeezing shoulder blades together."
      }
    ],
    completed: false
  },
  {
    day: "Day 7",
    focus: "Legs and Core",
    exercises: [
      {
        name: "Front Squats",
        sets: 3,
        reps: 8,
        rest: "120 seconds",
        equipment: "barbell",
        instructions: "Hold bar at front of shoulders, squat down keeping chest up, return to standing."
      },
      {
        name: "Hamstring Curls",
        sets: 3,
        reps: 12,
        rest: "60 seconds",
        equipment: "machine",
        instructions: "Lie face down on machine, curl legs up by bending knees, lower with control."
      },
      {
        name: "Plank",
        sets: 3,
        reps: 45,
        rest: "45 seconds",
        equipment: "bodyweight",
        instructions: "Hold position with body straight, supported on forearms and toes for 45 seconds."
      },
      {
        name: "Calf Raises",
        sets: 3,
        reps: 15,
        rest: "60 seconds",
        equipment: "machine",
        instructions: "Stand on edge of platform, lower heels below level, raise up onto toes."
      }
    ],
    completed: false
  }
];
