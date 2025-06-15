import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { useUser } from '../context/UserContext';
import Header from '../components/layout/Header';
import Layout from '../components/layout/Layout';
import { ChatMessage } from '../types/chat';
import api from '../services/api';

const Chatbot: React.FC = () => {
  const { user } = useUser();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m FitGenie AI, your personal fitness and nutrition assistant. How can I help you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState<'meal' | 'workout'>('workout');
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !user) return;
    
    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content: input
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);
    
    try {
      // Send message to API
      const sessionId = 'demo-session-123';
      const response = await api.chat(
        sessionId,
        user,
        null, // No specific plan needed for general chat
        input,
        context,
        messages
      );
      
      // Update messages with response
      setMessages(response.history);
    } catch (err) {
      console.error('Error sending chat message:', err);
      setError('Failed to get a response. Please try again later.');
      setMessages(prev => [
        ...prev,
        { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error processing your request. Please try again later.' 
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <Header />
      <Layout>
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-6 border-b">
              <h1 className="text-2xl font-bold text-secondary-navy">FitGenie AI Assistant</h1>
              <p className="text-secondary-grey mt-2">
                Ask me anything about your fitness and nutrition plans.
              </p>
              
              <div className="mt-4 flex">
                <div className="bg-white rounded-full shadow-sm p-1 inline-flex">
                  <button
                    className={`px-4 py-2 rounded-full text-sm font-medium ${
                      context === 'workout'
                        ? 'bg-primary-blue text-white'
                        : 'text-secondary-grey'
                    }`}
                    onClick={() => setContext('workout')}
                  >
                    Workout
                  </button>
                  <button
                    className={`px-4 py-2 rounded-full text-sm font-medium ${
                      context === 'meal'
                        ? 'bg-primary-blue text-white'
                        : 'text-secondary-grey'
                    }`}
                    onClick={() => setContext('meal')}
                  >
                    Meal
                  </button>
                </div>
                <div className="ml-4 text-sm text-secondary-grey flex items-center">
                  Current context: <span className="font-medium ml-1 capitalize">{context}</span>
                </div>
              </div>
            </div>
            
            {error && (
              <div className="bg-accent-red bg-opacity-10 border border-accent-red text-accent-red p-4 mx-6 mt-4 rounded-md">
                <p>{error}</p>
              </div>
            )}
            
            <div className="h-[60vh] overflow-y-auto p-6 bg-gray-50">
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-3 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-primary-blue text-white'
                          : 'bg-white border border-gray-200'
                      }`}
                    >
                      {message.role === 'assistant' ? (
                        <div className="text-sm prose prose-sm max-w-none">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                      </div>
                      ) : (
                        <p className="text-sm">{message.content}</p>
                      )}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] p-3 rounded-lg bg-white border border-gray-200">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
            
            <div className="p-4 border-t">
              <div className="flex">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={`Ask about your ${context} plan...`}
                  className="input-field flex-1 resize-none"
                  rows={2}
                  disabled={loading}
                />
                <button
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  className="ml-3 bg-primary-blue text-white px-4 py-2 rounded-md self-end disabled:opacity-50"
                >
                  Send
                </button>
              </div>
              <p className="text-xs text-secondary-grey mt-2">
                Press Enter to send, Shift+Enter for a new line
              </p>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default Chatbot;
