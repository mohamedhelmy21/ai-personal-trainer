import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import Header from '../components/layout/Header';
import Layout from '../components/layout/Layout';
import { WeeklyMealPlan } from '../types/meal';
import api from '../services/api';
import { ChatMessage } from '../types/chat';

// Define interfaces for meal components
interface MealComponent {
  item: string;
  portion: string;
}

const MealPlan: React.FC = () => {
  const { user } = useUser();
  const [mealPlan, setMealPlan] = useState<WeeklyMealPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeDay, setActiveDay] = useState(0);
  const [showRecipe, setShowRecipe] = useState(false);
  const [selectedMeal, setSelectedMeal] = useState<string | null>(null);
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {role: 'assistant', content: 'Hello! I\'m your FitGenie meal assistant. How can I help you with your meal plan today?'}
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Load meal plan
        const data = await api.loadMealPlan();
        setMealPlan(data);
      } catch (err) {
        console.error('Error loading meal plan:', err);
        setError('Failed to load your meal plan. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const handleMealClick = (mealType: string) => {
    setSelectedMeal(mealType);
    setShowRecipe(true);
  };

  const handleSwapMeal = () => {
    // Mock meal swap functionality
    alert('Meal swap feature coming soon!');
    setShowRecipe(false);
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !user || !mealPlan) return;
    
    // Add user message to chat
    const userMessage: ChatMessage = {
      role: 'user',
      content: chatInput
    };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);
    
    try {
      // Send message to API
      const sessionId = 'demo-session-123';
      const response = await api.chat(
        sessionId,
        user,
        { days: mealPlan },
        chatInput,
        'meal',
        chatMessages
      );
      
      // Add assistant response
      setChatMessages(response.history);
    } catch (err) {
      console.error('Error sending chat message:', err);
      setChatMessages(prev => [
        ...prev,
        { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error processing your request. Please try again later.' 
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  if (loading || !mealPlan) {
    return (
      <>
        <Header />
        <Layout>
          <div className="max-w-7xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-secondary-navy">Weekly Meal Plan</h1>
            </div>
            
            {error ? (
              <div className="bg-accent-red bg-opacity-10 border border-accent-red text-accent-red p-4 rounded-md">
                <p>{error}</p>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
                <div className="grid grid-cols-7 gap-4 mb-6">
                  {[...Array(7)].map((_, i) => (
                    <div key={i} className="h-10 bg-gray-200 rounded"></div>
                  ))}
                </div>
                <div className="h-64 bg-gray-200 rounded mb-4"></div>
              </div>
            )}
          </div>
        </Layout>
      </>
    );
  }

  return (
    <>
      <Header />
      <Layout>
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-secondary-navy">Weekly Meal Plan</h1>
            <button 
              onClick={() => setShowChatbot(!showChatbot)}
              className="btn-primary flex items-center"
            >
              <span className="mr-2">Ask FitGenie</span>
              <span>💬</span>
            </button>
          </div>

          {/* Day selector tabs */}
          <div className="bg-white rounded-lg shadow-md mb-6">
            <div className="grid grid-cols-7 border-b">
              {mealPlan.map((day, index) => (
                <button
                  key={index}
                  className={`py-3 text-center font-medium ${
                    activeDay === index
                      ? 'text-primary-blue border-b-2 border-primary-blue'
                      : 'text-secondary-grey hover:text-secondary-navy'
                  }`}
                  onClick={() => setActiveDay(index)}
                >
                  {day.date}
                </button>
              ))}
            </div>
          </div>

          {/* Daily nutrition summary */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold text-secondary-navy mb-4">Daily Nutrition</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-secondary-mint bg-opacity-20 p-4 rounded-lg text-center">
                <div className="text-sm text-secondary-grey">Calories</div>
                <div className="text-2xl font-bold text-secondary-navy">
                  {mealPlan[activeDay].totals.calories.toFixed(0)}
                </div>
                <div className="text-xs text-secondary-grey">kcal</div>
              </div>
              <div className="bg-secondary-mint bg-opacity-20 p-4 rounded-lg text-center">
                <div className="text-sm text-secondary-grey">Protein</div>
                <div className="text-2xl font-bold text-secondary-navy">
                  {mealPlan[activeDay].totals.protein_g.toFixed(0)}
                </div>
                <div className="text-xs text-secondary-grey">grams</div>
              </div>
              <div className="bg-secondary-mint bg-opacity-20 p-4 rounded-lg text-center">
                <div className="text-sm text-secondary-grey">Carbs</div>
                <div className="text-2xl font-bold text-secondary-navy">
                  {mealPlan[activeDay].totals.carbs_g.toFixed(0)}
                </div>
                <div className="text-xs text-secondary-grey">grams</div>
              </div>
              <div className="bg-secondary-mint bg-opacity-20 p-4 rounded-lg text-center">
                <div className="text-sm text-secondary-grey">Fat</div>
                <div className="text-2xl font-bold text-secondary-navy">
                  {mealPlan[activeDay].totals.fat_g.toFixed(0)}
                </div>
                <div className="text-xs text-secondary-grey">grams</div>
              </div>
            </div>
          </div>

          {/* Meals for the day */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(mealPlan[activeDay].meals).map(([mealType, meal]) => (
              <div key={mealType} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="bg-primary-blue text-white p-4">
                  <h3 className="font-semibold capitalize">{mealType}</h3>
                  <div className="text-sm opacity-80">{meal.totals.calories.toFixed(0)} kcal</div>
                </div>
                <div className="p-4">
                  <div className="space-y-3">
                    <div>
                      <span className="text-sm font-medium text-secondary-grey">Protein:</span>
                      <div className="flex justify-between">
                        <span>{meal.components.protein.item}</span>
                        <span className="text-sm">{meal.components.protein.portion}</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-secondary-grey">Carbs:</span>
                      <div className="flex justify-between">
                        <span>{meal.components.carb.item}</span>
                        <span className="text-sm">{meal.components.carb.portion}</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-secondary-grey">Fat:</span>
                      <div className="flex justify-between">
                        <span>{meal.components.fat.item}</span>
                        <span className="text-sm">{meal.components.fat.portion}</span>
                      </div>
                    </div>
                    
                    {meal.components.vegetables && (
                      <div>
                        <span className="text-sm font-medium text-secondary-grey">Vegetables:</span>
                        {meal.components.vegetables.map((veg: MealComponent, i: number) => (
                          <div key={i} className="flex justify-between">
                            <span>{veg.item}</span>
                            <span className="text-sm">{veg.portion}</span>
                          </div>
                        ))}
                      </div>
                    )}
                    
                    {meal.components.fruits && (
                      <div>
                        <span className="text-sm font-medium text-secondary-grey">Fruits:</span>
                        {meal.components.fruits.map((fruit: MealComponent, i: number) => (
                          <div key={i} className="flex justify-between">
                            <span>{fruit.item}</span>
                            <span className="text-sm">{fruit.portion}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-wrap gap-2 mt-4">
                    {meal.tags.map((tag: string, i: number) => (
                      <span key={i} className="text-xs bg-secondary-mint bg-opacity-30 text-secondary-navy px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div className="mt-4 flex space-x-2">
                    <button 
                      onClick={() => handleMealClick(mealType)}
                      className="btn-outline text-sm py-1 flex-1"
                    >
                      View Recipe
                    </button>
                    <button className="btn-secondary text-sm py-1 flex-1">
                      Swap Meal
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Recipe Modal */}
          {showRecipe && selectedMeal && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div className="p-6">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-secondary-navy capitalize">
                      {selectedMeal} Recipe
                    </h3>
                    <button 
                      onClick={() => setShowRecipe(false)}
                      className="text-secondary-grey hover:text-secondary-navy"
                    >
                      ✕
                    </button>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-secondary-navy">Ingredients</h4>
                      <ul className="list-disc pl-5 mt-2 space-y-1">
                        {Object.entries(mealPlan[activeDay].meals[selectedMeal as keyof typeof mealPlan[0]['meals']].components)
                          .flatMap(([key, value]) => {
                            if (key === 'vegetables' || key === 'fruits') {
                              return (value as MealComponent[]).map(item => `${item.portion} ${item.item}`);
                            }
                            return [`${(value as MealComponent).portion} ${(value as MealComponent).item}`];
                          })
                          .map((ingredient, i) => (
                            <li key={i}>{ingredient}</li>
                          ))
                        }
                      </ul>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-secondary-navy">Instructions</h4>
                      <p className="mt-2 text-secondary-grey">
                        Combine all ingredients according to your preference. For detailed cooking instructions, ask FitGenie AI in the chatbot.
                      </p>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-secondary-navy">Nutrition Facts</h4>
                      <div className="grid grid-cols-2 gap-2 mt-2">
                        <div className="bg-secondary-mint bg-opacity-20 p-2 rounded">
                          <div className="text-sm text-secondary-grey">Calories</div>
                          <div className="font-bold text-secondary-navy">
                            {mealPlan[activeDay].meals[selectedMeal as keyof typeof mealPlan[0]['meals']].totals.calories.toFixed(0)} kcal
                          </div>
                        </div>
                        <div className="bg-secondary-mint bg-opacity-20 p-2 rounded">
                          <div className="text-sm text-secondary-grey">Protein</div>
                          <div className="font-bold text-secondary-navy">
                            {mealPlan[activeDay].meals[selectedMeal as keyof typeof mealPlan[0]['meals']].totals.protein_g.toFixed(0)}g
                          </div>
                        </div>
                        <div className="bg-secondary-mint bg-opacity-20 p-2 rounded">
                          <div className="text-sm text-secondary-grey">Carbs</div>
                          <div className="font-bold text-secondary-navy">
                            {mealPlan[activeDay].meals[selectedMeal as keyof typeof mealPlan[0]['meals']].totals.carbs_g.toFixed(0)}g
                          </div>
                        </div>
                        <div className="bg-secondary-mint bg-opacity-20 p-2 rounded">
                          <div className="text-sm text-secondary-grey">Fat</div>
                          <div className="font-bold text-secondary-navy">
                            {mealPlan[activeDay].meals[selectedMeal as keyof typeof mealPlan[0]['meals']].totals.fat_g.toFixed(0)}g
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-6 flex justify-end space-x-3">
                    <button 
                      onClick={() => setShowRecipe(false)}
                      className="btn-outline"
                    >
                      Close
                    </button>
                    <button 
                      onClick={handleSwapMeal}
                      className="btn-primary"
                    >
                      Swap Meal
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Chatbot Popup */}
          {showChatbot && (
            <div className="fixed bottom-6 right-6 w-80 h-96 bg-white rounded-lg shadow-lg z-40 flex flex-col">
              <div className="bg-primary-blue text-white p-3 rounded-t-lg flex justify-between items-center">
                <h3 className="font-medium">FitGenie AI - Meal Assistant</h3>
                <button onClick={() => setShowChatbot(false)}>✕</button>
              </div>
              <div className="flex-1 p-3 overflow-y-auto bg-gray-50">
                <div className="space-y-3">
                  {chatMessages.map((msg, index) => (
                    <div 
                      key={index}
                      className={`${
                        msg.role === 'assistant' 
                          ? 'bg-secondary-mint bg-opacity-20 text-secondary-navy' 
                          : 'bg-primary-blue text-white ml-auto'
                      } p-2 rounded-lg max-w-[80%] ${msg.role === 'user' ? 'ml-auto' : ''}`}
                    >
                      <p className="text-sm">{msg.content}</p>
                    </div>
                  ))}
                  {chatLoading && (
                    <div className="bg-secondary-mint bg-opacity-20 p-2 rounded-lg max-w-[80%]">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
              <div className="p-3 border-t">
                <div className="flex">
                  <input 
                    type="text" 
                    placeholder="Ask about your meal plan..." 
                    className="input-field text-sm flex-1"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                    disabled={chatLoading}
                  />
                  <button 
                    className="ml-2 bg-primary-blue text-white p-2 rounded"
                    onClick={handleSendMessage}
                    disabled={chatLoading || !chatInput.trim()}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </Layout>
    </>
  );
};

export default MealPlan;
