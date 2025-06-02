// Matches the backend UserProfileIn schema
export interface UserProfile {
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;
  level: string; // e.g., 'beginner', 'intermediate', 'advanced'
  activity_level: string; // e.g., 'sedentary', 'moderately active'
  available_equipment: string[];
  days_per_week: number; // Number of workout days
  goal: string; // e.g., 'muscle gain', 'fat loss'
  subgoal: string; // e.g., 'hypertrophy'
  meal_frequency?: number; // Optional, defaults to 3 in backend
}

// Default profile for initial state or fallback
export const defaultUserProfile: UserProfile = {
  age: 21,
  gender: "male",
  height_cm: 172,
  weight_kg: 63,
  level: "intermediate",
  activity_level: "moderately active",
  available_equipment: ["bodyweight", "dumbbell", "barbell"],
  days_per_week: 3,
  goal: "muscle gain",
  subgoal: "hypertrophy",
  meal_frequency: 3,
};

