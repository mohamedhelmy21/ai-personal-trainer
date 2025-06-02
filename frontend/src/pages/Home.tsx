import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import { Link } from 'react-router-dom';
import Header from '../components/layout/Header';
import Layout from '../components/layout/Layout';
import { WeeklyMealPlan } from '../types/meal';
import { WeeklyWorkoutPlan } from '../types/workout';
import api from '../services/api';

const Home: React.FC = () => {
  const { user } = useUser();
  const [mealPlan, setMealPlan] = useState<WeeklyMealPlan | null>(null);
  const [workoutPlan, setWorkoutPlan] = useState<WeeklyWorkoutPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Load meal and workout plans
        const mealData = await api.loadMealPlan();
        const workoutData = await api.loadWorkoutPlan();
        
        setMealPlan(mealData);
        setWorkoutPlan(workoutData);
      } catch (err) {
        console.error('Error loading data:', err);
        setError('Failed to load your fitness data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  // Get today's meal and workout
  const todayMeal = mealPlan ? mealPlan[0] : null;
  const todayWorkout = workoutPlan ? workoutPlan[0] : null;

  return (
    <>
      <Header />
      <Layout>
        <div className="max-w-7xl mx-auto">
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-secondary-navy">
              Welcome back, {user?.gender === 'male' ? 'Mr.' : user?.gender === 'female' ? 'Ms.' : ''} Fitness Enthusiast!
            </h1>
            <p className="text-secondary-grey mt-2">
              Here's your personalized fitness dashboard for today.
            </p>
          </div>

          {error && (
            <div className="bg-accent-red bg-opacity-10 border border-accent-red text-accent-red p-4 rounded-md mb-6">
              <p>{error}</p>
            </div>
          )}

          {loading ? (
            // Loading skeleton
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
                  <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-4/6 mb-6"></div>
                  <div className="h-10 bg-gray-200 rounded w-full"></div>
                </div>
              ))}
            </div>
          ) : (
            // Dashboard content
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Today's Meal Plan */}
              {todayMeal && (
                <div className="card">
                  <h2 className="text-xl font-semibold text-secondary-navy mb-4">Today's Meal Plan</h2>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="font-medium">Total Calories:</span>
                      <span className="text-primary-blue font-bold">{todayMeal.totals.calories.toFixed(0)} kcal</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="bg-secondary-mint bg-opacity-30 p-2 rounded">
                        <div className="text-sm text-secondary-grey">Protein</div>
                        <div className="font-bold text-secondary-navy">{todayMeal.totals.protein_g.toFixed(0)}g</div>
                      </div>
                      <div className="bg-secondary-mint bg-opacity-30 p-2 rounded">
                        <div className="text-sm text-secondary-grey">Carbs</div>
                        <div className="font-bold text-secondary-navy">{todayMeal.totals.carbs_g.toFixed(0)}g</div>
                      </div>
                      <div className="bg-secondary-mint bg-opacity-30 p-2 rounded">
                        <div className="text-sm text-secondary-grey">Fat</div>
                        <div className="font-bold text-secondary-navy">{todayMeal.totals.fat_g.toFixed(0)}g</div>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium">Breakfast: {todayMeal.meals.breakfast.components.protein.item} & {todayMeal.meals.breakfast.components.carb.item}</div>
                      <div className="text-sm font-medium">Lunch: {todayMeal.meals.lunch.components.protein.item} & {todayMeal.meals.lunch.components.carb.item}</div>
                      <div className="text-sm font-medium">Dinner: {todayMeal.meals.dinner.components.protein.item} & {todayMeal.meals.dinner.components.carb.item}</div>
                    </div>
                    <Link to="/meal-plan" className="btn-primary w-full mt-4 block text-center">View Full Meal Plan</Link>
                  </div>
                </div>
              )}

              {/* Today's Workout */}
              {todayWorkout && (
                <div className="card">
                  <h2 className="text-xl font-semibold text-secondary-navy mb-4">Today's Workout</h2>
                  <div className="space-y-4">
                    <div className="bg-primary-blue bg-opacity-10 p-3 rounded-md">
                      <div className="font-medium text-primary-blue">{todayWorkout.focus} Focus</div>
                      <div className="text-sm text-secondary-grey mt-1">{todayWorkout.exercises.length} exercises</div>
                    </div>
                    <div className="space-y-2">
                      {todayWorkout.exercises.map((exercise, index) => (
                        <div key={index} className="flex items-center">
                          <div className="w-2 h-2 rounded-full bg-secondary-navy mr-2"></div>
                          <div className="text-sm">{exercise.name}: {exercise.sets} sets × {exercise.reps} reps</div>
                        </div>
                      ))}
                    </div>
                    <div className="flex items-center justify-between mt-4">
                      <div className="text-sm text-secondary-grey">Equipment needed:</div>
                      <div className="text-sm font-medium">
                        {Array.from(new Set(todayWorkout.exercises.map(e => e.equipment))).join(', ')}
                      </div>
                    </div>
                    <Link to="/workout-plan" className="btn-primary w-full mt-4 block text-center">View Full Workout Plan</Link>
                  </div>
                </div>
              )}

              {/* Progress Overview */}
              <div className="card">
                <h2 className="text-xl font-semibold text-secondary-navy mb-4">Progress Overview</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Weekly Streak:</span>
                    <span className="text-accent-green font-bold">3 days</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-accent-green h-2.5 rounded-full" style={{ width: '45%' }}></div>
                  </div>
                  <div className="text-xs text-secondary-grey text-right">45% to weekly goal</div>
                  
                  <div className="mt-6">
                    <h3 className="font-medium text-secondary-navy mb-2">Recent Achievements</h3>
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <div className="w-8 h-8 rounded-full bg-primary-blue bg-opacity-20 flex items-center justify-center mr-3">
                          <span className="text-primary-blue text-sm">🏋️</span>
                        </div>
                        <div>
                          <div className="text-sm font-medium">First Workout Completed</div>
                          <div className="text-xs text-secondary-grey">2 days ago</div>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <div className="w-8 h-8 rounded-full bg-primary-blue bg-opacity-20 flex items-center justify-center mr-3">
                          <span className="text-primary-blue text-sm">🥗</span>
                        </div>
                        <div>
                          <div className="text-sm font-medium">Nutrition Plan Started</div>
                          <div className="text-xs text-secondary-grey">3 days ago</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <Link to="/profile" className="btn-outline w-full mt-4 block text-center">View All Progress</Link>
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card bg-gradient-to-r from-primary-blue to-secondary-navy text-white">
              <h2 className="text-xl font-semibold mb-4">Need Guidance?</h2>
              <p className="mb-6">Ask FitGenie AI any questions about your workout or meal plan.</p>
              <Link to="/chatbot" className="bg-white text-secondary-navy font-medium px-4 py-2 rounded-md hover:bg-opacity-90 transition-all inline-block">
                Open Chatbot
              </Link>
            </div>
            <div className="card bg-secondary-mint">
              <h2 className="text-xl font-semibold text-secondary-navy mb-4">Coming Soon</h2>
              <p className="text-secondary-navy mb-6">Progress tracking, workout analytics, and integration with wearables.</p>
              <div className="bg-white text-secondary-grey text-sm px-4 py-2 rounded-md inline-block">
                In Development
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default Home;
