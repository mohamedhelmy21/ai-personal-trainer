export interface UserProfile {
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;
  activity_level: 'sedentary' | 'lightly active' | 'moderately active' | 'very active' | 'super active';
  workout_days_per_week: number;
  fitness_level: 'beginner' | 'intermediate' | 'advanced';
  primary_goal: 'muscle gain' | 'fat loss' | 'maintenance';
  sub_goal?: string;
  preferred_meal_frequency: number;
  available_equipment: string[];
}

export const defaultUserProfile: UserProfile = {
  age: 21,
  gender: "male",
  height_cm: 172,
  weight_kg: 63,
  activity_level: "moderately active",
  workout_days_per_week: 3,
  primary_goal: "muscle gain",
  sub_goal: "hypertrophy",
  fitness_level: "intermediate",
  preferred_meal_frequency: 3,
  available_equipment: ["bodyweight", "dumbbell", "barbell"]
};
