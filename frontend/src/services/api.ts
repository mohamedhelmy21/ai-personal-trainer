import axios from 'axios';
import { UserProfile } from '../types/user';
import { WeeklyMealPlan } from '../types/meal';
import { WeeklyWorkoutPlan } from '../types/workout';
import { ChatMessage } from '../types/chat';
import { mockMealPlan, mockWorkoutPlan } from '../data/mockData';

// Base API URL - would be replaced with actual backend URL in production
const API_BASE_URL = 'http://localhost:5000/api';

// API response type for chat
interface ChatResponse {
  message: string;
  history: ChatMessage[];
}

// API service for interacting with the backend
const api = {
  // User authentication
  login: async (email: string, password: string): Promise<UserProfile> => {
    try {
      // In a real app, this would be an actual API call
      // const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password });
      // return response.data;
      
      // For demo, return mock data
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            age: 28,
            gender: 'male',
            height_cm: 175,
            weight_kg: 75,
            activity_level: 'moderately active',
            fitness_level: 'intermediate',
            primary_goal: 'muscle gain',
            sub_goal: 'hypertrophy',
            workout_days_per_week: 4,
            preferred_meal_frequency: 3,
            available_equipment: ['barbell', 'dumbbell', 'bodyweight', 'machine']
          });
        }, 1000);
      });
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Update user profile
  updateProfile: async (profile: UserProfile): Promise<UserProfile> => {
    try {
      // In a real app, this would be an actual API call
      // const response = await axios.put(`${API_BASE_URL}/user/profile`, profile);
      // return response.data;
      
      // For demo, return the same profile
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(profile);
        }, 1000);
      });
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  },

  // Load meal plan
  loadMealPlan: async (): Promise<WeeklyMealPlan> => {
    try {
      // In a real app, this would be an actual API call
      // const response = await axios.get(`${API_BASE_URL}/meal-plan`);
      // return response.data;
      
      // For demo, return mock data
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockMealPlan);
        }, 1000);
      });
    } catch (error) {
      console.error('Load meal plan error:', error);
      throw error;
    }
  },

  // Load workout plan
  loadWorkoutPlan: async (): Promise<WeeklyWorkoutPlan> => {
    try {
      // In a real app, this would be an actual API call
      // const response = await axios.get(`${API_BASE_URL}/workout-plan`);
      // return response.data;
      
      // For demo, return mock data
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockWorkoutPlan);
        }, 1000);
      });
    } catch (error) {
      console.error('Load workout plan error:', error);
      throw error;
    }
  },

  // Chat with AI assistant
  chat: async (
    sessionId: string,
    user: UserProfile,
    plan: { days: WeeklyMealPlan } | { days: WeeklyWorkoutPlan } | null,
    message: string,
    context: 'meal' | 'workout',
    history: ChatMessage[]
  ): Promise<ChatResponse> => {
    try {
      // In a real app, this would be an actual API call to the backend
      // const response = await axios.post(`${API_BASE_URL}/chat`, {
      //   sessionId,
      //   user,
      //   plan,
      //   message,
      //   context,
      //   history
      // });
      // return response.data;
      
      // For demo, simulate a response
      return new Promise((resolve) => {
        setTimeout(() => {
          const newHistory = [...history, { role: 'user' as const, content: message }];
          
          let responseContent = '';
          if (context === 'meal') {
            responseContent = `I can help you with your meal plan. Based on your ${user.primary_goal} goal, I recommend focusing on ${user.primary_goal === 'muscle gain' ? 'protein-rich foods' : 'balanced nutrition with a caloric deficit'}. Would you like specific meal suggestions?`;
          } else {
            responseContent = `For your ${user.primary_goal} goal with a ${user.fitness_level} fitness level, I recommend ${user.workout_days_per_week} workouts per week. Would you like me to suggest specific exercises for your next workout?`;
          }
          
          newHistory.push({ role: 'assistant' as const, content: responseContent });
          
          resolve({
            message: responseContent,
            history: newHistory
          });
        }, 1500);
      });
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }
};

export default api;
