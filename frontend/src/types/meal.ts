export interface MealComponent {
  item: string;
  portion: string;
  calories: number;
}

export interface MealComponents {
  protein: MealComponent;
  carb: MealComponent;
  fat: MealComponent;
  vegetables?: MealComponent[];
  fruits?: MealComponent[];
}

export interface MealTotals {
  protein_g: number;
  fat_g: number;
  carbs_g: number;
  calories: number;
}

export interface Meal {
  type: string;
  components: MealComponents;
  totals: MealTotals;
  tags: string[];
}

export interface DailyMeals {
  breakfast: Meal;
  lunch: Meal;
  dinner: Meal;
}

export interface DailyPlan {
  meals: DailyMeals;
  totals: MealTotals;
  date: string;
}

export type WeeklyMealPlan = DailyPlan[];
