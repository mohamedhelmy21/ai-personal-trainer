import React, { createContext, useContext, useState, ReactNode } from 'react';
import { UserProfile } from '../types/user';

// Default user profile for demo purposes
const defaultUser: UserProfile | null = null; // Changed to null to force profile setup

interface UserContextType {
  user: UserProfile | null;
  setUser: (user: UserProfile) => void;
  isAuthenticated: boolean;
  isProfileComplete: boolean; // Added to track profile completion status
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(defaultUser);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // Determine if profile is complete based on user object existence
  const isProfileComplete = user !== null;

  // Mock login function for demo
  const login = async (email: string, password: string): Promise<boolean> => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        // Only set authenticated, but don't set user profile
        // This will force the user to complete profile setup
        setIsAuthenticated(true);
        resolve(true);
      }, 1000);
    });
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <UserContext.Provider value={{ 
      user, 
      setUser, 
      isAuthenticated, 
      isProfileComplete,
      login, 
      logout 
    }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
