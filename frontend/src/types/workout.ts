export interface Exercise {
  name: string;
  sets: number;
  reps: number;
  rest: string;
  equipment: string;
  instructions: string;
}

export interface WorkoutDay {
  day: string;
  focus: string;
  exercises: Exercise[];
  completed?: boolean;
}

export type WeeklyWorkoutPlan = WorkoutDay[];
