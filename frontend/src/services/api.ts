import axios from 'axios';
import { UserProfile } from '../types/user';
// Import DailyPlan specifically for the transformation logic
import { DailyPlan, WeeklyMealPlan } from '../types/meal'; 
import { WorkoutDay, WeeklyWorkoutPlan } from '../types/workout';
import { ChatMessage } from '../types/chat';

// Import the local JSON plan files
import weeklyMealPlanData from '../data/weekly_meal_plan.json';
import weeklyWorkoutPlanData from '../data/weekly_workout_plan.json';

// Base API URL - Pointing to the local backend server
// Ensure your backend FastAPI server is running on this address and port
const API_BASE_URL = 'http://localhost:8000'; // Default FastAPI port is 8000

// API response type for chat from backend
interface BackendChatResponse {
  response: string; // The chatbot's reply message
  plan: any; // The potentially updated plan (meal or workout)
  history: ChatMessage[]; // The updated conversation history
}

// API response type expected by the frontend chat component
interface FrontendChatResponse {
  message: string;
  history: ChatMessage[];
}

// Helper function to transform workout plan object to array
const transformWorkoutPlan = (data: any): WeeklyWorkoutPlan => {
  if (Array.isArray(data)) {
    return data as WeeklyWorkoutPlan; // Already in correct format
  }
  if (typeof data === 'object' && data !== null) {
    // Assuming keys are 'Day 1', 'Day 2', etc.
    return Object.entries(data).map(([dayKey, dayData]: [string, any]) => ({
      day: dayKey, 
      focus: dayData.type || 'Unknown', 
      exercises: dayData.workout || [], 
      // Ensure exercises match the Exercise interface structure if needed
      // Add completed field if necessary
      completed: false, // Default to false
    })) as WeeklyWorkoutPlan;
  }
  console.warn('Unexpected workout plan data format:', data);
  return []; 
};

// Helper function to transform meal plan object to array (if needed)
const transformMealPlan = (data: any): WeeklyMealPlan => {
  if (Array.isArray(data)) {
    return data as WeeklyMealPlan; // Already in correct format
  }
  if (typeof data === 'object' && data !== null && data.days && Array.isArray(data.days)) {
     // If data is { days: [...] }
     return data.days as WeeklyMealPlan;
  }
  if (typeof data === 'object' && data !== null) {
    // If data is { 'Day 1': {...}, ... }
    // Map to DailyPlan structure
    return Object.entries(data).map(([dayKey, dayData]: [string, any]): DailyPlan => ({
      // Assuming dayData contains meals and totals
      // Add a placeholder date or extract if available
      date: dayData.date || new Date().toISOString().split('T')[0], // Placeholder date
      meals: dayData.meals || { breakfast: null, lunch: null, dinner: null }, // Ensure DailyMeals structure
      totals: dayData.totals || { protein_g: 0, fat_g: 0, carbs_g: 0, calories: 0 }, // Ensure MealTotals structure
      // Add day property if needed by frontend components, though not in DailyPlan type
      // day: dayKey, // This might be needed depending on how components use the data
    })) as WeeklyMealPlan; // Cast the array of DailyPlan objects to WeeklyMealPlan
  }
  console.warn('Unexpected meal plan data format:', data);
  return [];
};


// API service for interacting with the backend
const api = {
  // User authentication (using mock for demo)
  login: async (email: string, password: string): Promise<UserProfile> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          age: 28,
          gender: 'male',
          height_cm: 175,
          weight_kg: 75,
          level: 'intermediate',
          activity_level: 'moderately active',
          available_equipment: ['barbell', 'dumbbell', 'bodyweight', 'machine'],
          days_per_week: 4,
          goal: 'muscle gain',
          subgoal: 'hypertrophy',
          meal_frequency: 3,
        });
      }, 500);
    });
  },

  // Update user profile (using mock for demo)
  updateProfile: async (profile: UserProfile): Promise<UserProfile> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(profile);
      }, 500);
    });
  },

  // Load meal plan from local JSON
  loadMealPlan: async (): Promise<WeeklyMealPlan> => {
    try {
      return new Promise((resolve) => {
        setTimeout(() => {
          const transformedPlan = transformMealPlan(weeklyMealPlanData);
          resolve(transformedPlan);
        }, 500);
      });
    } catch (error) {
      console.error('Load meal plan error:', error);
      return Promise.reject('Failed to load meal plan data.');
    }
  },

  // Load workout plan from local JSON
  loadWorkoutPlan: async (): Promise<WeeklyWorkoutPlan> => {
    try {
      return new Promise((resolve) => {
        setTimeout(() => {
          const transformedPlan = transformWorkoutPlan(weeklyWorkoutPlanData);
          resolve(transformedPlan);
        }, 500);
      });
    } catch (error) {
      console.error('Load workout plan error:', error);
      return Promise.reject('Failed to load workout plan data.');
    }
  },

  // Chat with AI assistant (connecting to backend)
  chat: async (
    sessionId: string,
    user: UserProfile,
    plan: WeeklyMealPlan | WeeklyWorkoutPlan | null, 
    message: string,
    planType: 'meal' | 'workout',
    history: ChatMessage[]
  ): Promise<FrontendChatResponse> => {
    try {
      const planPayload = plan ? plan : null;

      const response = await axios.post<BackendChatResponse>(`${API_BASE_URL}/chat`, {
        session_id: sessionId,
        user: user,
        plan: planPayload, 
        message: message,
        plan_type: planType,
        history: history
      });

      return {
        message: response.data.response,
        history: response.data.history
      };
    } catch (error) {
      console.error('Chat API error:', error);
      let errorMessage = 'Sorry, I encountered an error trying to connect to the chat assistant.';
      if (axios.isAxiosError(error) && error.response) {
        errorMessage += ` Server responded with: ${error.response.status} - ${JSON.stringify(error.response.data)}`;
      } else if (axios.isAxiosError(error) && error.request) {
        errorMessage = 'Unable to reach the chat assistant. Please ensure the backend server is running and accessible at ' + API_BASE_URL;
      }
      return {
        message: errorMessage,
        history: [...history, { role: 'user', content: message }, { role: 'assistant', content: errorMessage }]
      };
    }
  }
};

export default api;

