import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import Header from '../components/layout/Header';
import Layout from '../components/layout/Layout';
import { WeeklyWorkoutPlan } from '../types/workout';
import api from '../services/api';
import { ChatMessage } from '../types/chat';

const WorkoutPlan: React.FC = () => {
  const { user } = useUser();
  const [workoutPlan, setWorkoutPlan] = useState<WeeklyWorkoutPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeDay, setActiveDay] = useState(0);
  const [showExerciseDetails, setShowExerciseDetails] = useState<number | null>(null);
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {role: 'assistant', content: 'Hello! I\'m your FitGenie workout assistant. How can I help you with your workout plan today?'}
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Load workout plan
        const data = await api.loadWorkoutPlan();
        setWorkoutPlan(data);
      } catch (err) {
        console.error('Error loading workout plan:', err);
        setError('Failed to load your workout plan. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const handleCompleteWorkout = () => {
    if (!workoutPlan) return;
    
    const updatedPlan = [...workoutPlan];
    updatedPlan[activeDay] = {
      ...updatedPlan[activeDay],
      completed: !updatedPlan[activeDay].completed
    };
    setWorkoutPlan(updatedPlan);
    
    if (!updatedPlan[activeDay].completed) {
      // Show success modal
      alert('Great job completing your workout!');
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !user || !workoutPlan) return;
    
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
        { days: workoutPlan },
        chatInput,
        'workout',
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

  if (loading || !workoutPlan) {
    return (
      <>
        <Header />
        <Layout>
          <div className="max-w-7xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-secondary-navy">Weekly Workout Plan</h1>
            </div>
            
            {error ? (
              <div className="bg-accent-red bg-opacity-10 border border-accent-red text-accent-red p-4 rounded-md">
                <p>{error}</p>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  {[...Array(3)].map((_, i) => (
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
            <h1 className="text-2xl font-bold text-secondary-navy">Weekly Workout Plan</h1>
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
            <div className="grid grid-cols-3 md:grid-cols-7 border-b">
              {workoutPlan.map((day, index) => (
                <button
                  key={index}
                  className={`py-3 text-center font-medium relative ${
                    activeDay === index
                      ? 'text-primary-blue border-b-2 border-primary-blue'
                      : 'text-secondary-grey hover:text-secondary-navy'
                  }`}
                  onClick={() => setActiveDay(index)}
                >
                  {day.day}
                  {day.completed && (
                    <span className="absolute top-1 right-1 w-3 h-3 bg-accent-green rounded-full"></span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Workout focus */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold text-secondary-navy">
                  {workoutPlan[activeDay].focus}
                </h2>
                <p className="text-secondary-grey mt-1">
                  {workoutPlan[activeDay].exercises.length} exercises
                </p>
              </div>
              <div>
                <button
                  onClick={handleCompleteWorkout}
                  className={`px-4 py-2 rounded-md font-medium ${
                    workoutPlan[activeDay].completed
                      ? 'bg-accent-green text-white'
                      : 'bg-secondary-grey bg-opacity-20 text-secondary-grey'
                  }`}
                >
                  {workoutPlan[activeDay].completed ? 'Completed ✓' : 'Mark as Complete'}
                </button>
              </div>
            </div>
          </div>

          {/* Exercise list */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-6">
              <h3 className="text-lg font-medium text-secondary-navy mb-4">Exercises</h3>
              <div className="space-y-4">
                {workoutPlan[activeDay].exercises.map((exercise, index) => (
                  <div key={index} className="border rounded-lg overflow-hidden">
                    <div 
                      className="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-50"
                      onClick={() => setShowExerciseDetails(showExerciseDetails === index ? null : index)}
                    >
                      <div>
                        <h4 className="font-medium text-secondary-navy">{exercise.name}</h4>
                        <p className="text-sm text-secondary-grey">
                          {exercise.sets} sets × {exercise.reps} reps • {exercise.equipment}
                        </p>
                      </div>
                      <div className="text-primary-blue">
                        {showExerciseDetails === index ? '▲' : '▼'}
                      </div>
                    </div>
                    
                    {showExerciseDetails === index && (
                      <div className="p-4 bg-secondary-mint bg-opacity-10 border-t">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                          <div>
                            <div className="text-sm text-secondary-grey">Sets</div>
                            <div className="font-medium">{exercise.sets}</div>
                          </div>
                          <div>
                            <div className="text-sm text-secondary-grey">Reps</div>
                            <div className="font-medium">{exercise.reps}</div>
                          </div>
                          <div>
                            <div className="text-sm text-secondary-grey">Rest</div>
                            <div className="font-medium">{exercise.rest}</div>
                          </div>
                        </div>
                        
                        <div className="mb-4">
                          <div className="text-sm text-secondary-grey mb-1">Equipment</div>
                          <div className="font-medium capitalize">{exercise.equipment}</div>
                        </div>
                        
                        <div>
                          <div className="text-sm text-secondary-grey mb-1">Instructions</div>
                          <div className="text-sm">{exercise.instructions}</div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Chatbot Popup */}
          {showChatbot && (
            <div className="fixed bottom-6 right-6 w-80 h-96 bg-white rounded-lg shadow-lg z-40 flex flex-col">
              <div className="bg-primary-blue text-white p-3 rounded-t-lg flex justify-between items-center">
                <h3 className="font-medium">FitGenie AI - Workout Assistant</h3>
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
                    placeholder="Ask about your workout..." 
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

export default WorkoutPlan;
