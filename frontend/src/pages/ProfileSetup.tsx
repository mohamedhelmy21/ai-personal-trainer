import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { UserProfile } from '../types/user';
import axios from 'axios'; // Import axios

const API_BASE_URL = 'http://localhost:8000'; // Define your API base URL

const ProfileSetup: React.FC = () => {
  const { setUser } = useUser();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<UserProfile>({
    age: 30,
    gender: 'male',
    height_cm: 175,
    weight_kg: 75,
    activity_level: 'moderately active',
    level: 'intermediate',
    goal: 'muscle gain',
    subgoal: '',
    days_per_week: 4,
    meal_frequency: 3,
    available_equipment: ['barbell', 'dumbbell', 'bodyweight']
  });
  
  const [step, setStep] = useState(1);
  const [savingProfile, setSavingProfile] = useState(false); // Renamed from 'loading'
  const [profileCompleted, setProfileCompleted] = useState(false);
  const [generatingPlans, setGeneratingPlans] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: Number(value) }));
  };

  const handleEquipmentChange = (equipment: string) => {
    setFormData(prev => {
      const currentEquipment = [...prev.available_equipment];
      if (currentEquipment.includes(equipment)) {
        return { ...prev, available_equipment: currentEquipment.filter(item => item !== equipment) };
      } else {
        return { ...prev, available_equipment: [...currentEquipment, equipment] };
      }
    });
  };

  const nextStep = (e?: React.MouseEvent<HTMLButtonElement>) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    console.log('Current step before nextStep:', step);
    setStep(prev => {
      console.log('Setting step to:', prev + 1);
      return prev + 1;
    });
  };
  const prevStep = () => {
    console.log('Current step before prevStep:', step);
    setStep(prev => {
      console.log('Setting step to:', prev - 1);
      return prev - 1;
    });
  };

  const handleProfileSubmit = async (e: React.FormEvent) => {
    console.log('handleProfileSubmit called. Current step:', step);
    e.preventDefault();
    e.preventDefault();
    setSavingProfile(true);
    setApiError(null);
    // Here, you might typically save the profile to a backend
    // For this demo, we'll just update context and proceed
    try {
      // Simulate API call for saving profile if you had one
      // await axios.post(`${API_BASE_URL}/profile`, formData);
      setUser(formData); // Update user context
      setProfileCompleted(true); // Mark profile as completed to show next step
    } catch (error) {
      console.error('Error saving profile:', error);
      setApiError('Failed to save profile. Please try again.');
    } finally {
      setSavingProfile(false);
    }
  };

  const handleGeneratePlans = async () => {
    if (!formData) {
      setApiError('Profile data is not available. Please complete your profile first.');
      return;
    }
    setGeneratingPlans(true);
    setApiError(null);
    console.log('Simulating plan generation with formData:', formData);

    // Simulate a delay for plan generation
    setTimeout(() => {
      console.log('Mock plan generation complete. Navigating to home.');
      // The home/dashboard page will be responsible for loading mock plans
      // based on the user profile in UserContext.
      setGeneratingPlans(false);
      navigate('/home');
    }, 2000); // Simulate a 2-second delay
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <img className="mx-auto h-20 w-auto" src="/assets/FitGenieLogo.png" alt="FitGenie" />
          <h2 className="mt-6 text-3xl font-bold text-secondary-navy">
            {profileCompleted ? 'Profile Saved!' : 'Set Up Your Profile'}
          </h2>
          <p className="mt-2 text-secondary-grey">
            {profileCompleted ? 'Next, let us generate your personalized plans.' : 'Let\'s personalize your fitness journey'}
          </p>
        </div>
        
        <div className="bg-white shadow-md rounded-lg p-8">
          {!profileCompleted ? (
            <>
              <div className="mb-8">
                {/* Progress Indicator */}
                <div className="flex justify-between items-center">
                  {[1, 2, 3].map((stepNumber) => (
                    <div key={stepNumber} className="flex flex-col items-center">
                      <div 
                        className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          step >= stepNumber 
                            ? 'bg-primary-blue text-white' 
                            : 'bg-gray-200 text-secondary-grey'
                        }`}
                      >
                        {stepNumber}
                      </div>
                      <div className="text-xs mt-2 text-secondary-grey">
                        {stepNumber === 1 && 'Basic Info'}
                        {stepNumber === 2 && 'Fitness Goals'}
                        {stepNumber === 3 && 'Equipment'}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-2 h-1 bg-gray-200 rounded">
                  <div 
                    className="h-1 bg-primary-blue rounded" 
                    style={{ width: `${(step / 3) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <form onSubmit={handleProfileSubmit}> {/* Changed to handleProfileSubmit */}
                {/* Step 1: Basic Info */}
                {step === 1 && (() => { return (
                  <div className="space-y-6">
                    <h3 className="text-xl font-medium text-secondary-navy">Basic Information</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="age" className="block text-sm font-medium text-gray-700">Age</label>
                        <input type="number" name="age" id="age" min="10" max="100" value={formData.age} onChange={handleNumberChange} className="input-field mt-1" required />
                      </div>
                      <div>
                        <label htmlFor="gender" className="block text-sm font-medium text-gray-700">Gender</label>
                        <select name="gender" id="gender" value={formData.gender} onChange={handleChange} className="input-field mt-1" required>
                          <option value="male">Male</option>
                          <option value="female">Female</option>
                          <option value="other">Other</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="height_cm" className="block text-sm font-medium text-gray-700">Height (cm)</label>
                        <input type="number" name="height_cm" id="height_cm" min="100" max="250" value={formData.height_cm} onChange={handleNumberChange} className="input-field mt-1" required />
                      </div>
                      <div>
                        <label htmlFor="weight_kg" className="block text-sm font-medium text-gray-700">Weight (kg)</label>
                        <input type="number" name="weight_kg" id="weight_kg" min="30" max="200" value={formData.weight_kg} onChange={handleNumberChange} className="input-field mt-1" required />
                      </div>
                      <div>
                        <label htmlFor="activity_level" className="block text-sm font-medium text-gray-700">Activity Level</label>
                        <select name="activity_level" id="activity_level" value={formData.activity_level} onChange={handleChange} className="input-field mt-1" required>
                          <option value="sedentary">Sedentary</option>
                          <option value="lightly active">Lightly Active</option>
                          <option value="moderately active">Moderately Active</option>
                          <option value="very active">Very Active</option>
                          <option value="super active">Super Active</option>
                        </select>
                      </div>
                    </div>
                  </div>
                ); })()}
                
                {/* Step 2: Fitness Goals */}
                {step === 2 && (() => { return (
                  <div className="space-y-6">
                    <h3 className="text-xl font-medium text-secondary-navy">Fitness Goals</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="level" className="block text-sm font-medium text-gray-700">Fitness Level</label>
                        <select name="level" id="level" value={formData.level} onChange={handleChange} className="input-field mt-1" required>
                          <option value="beginner">Beginner</option>
                          <option value="intermediate">Intermediate</option>
                          <option value="advanced">Advanced</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="goal" className="block text-sm font-medium text-gray-700">Primary Fitness Goal</label>
                        <select name="goal" id="goal" value={formData.goal} onChange={handleChange} className="input-field mt-1" required>
                          <option value="muscle gain">Muscle Gain</option>
                          <option value="fat loss">Fat Loss</option>
                          <option value="maintenance">Maintenance</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="subgoal" className="block text-sm font-medium text-gray-700">Specific Sub-Goal (Optional)</label>
                        <select name="subgoal" id="subgoal" value={formData.subgoal} onChange={handleChange} className="input-field mt-1">
                          <option value="">Select a sub-goal</option>
                          <option value="hypertrophy">Hypertrophy</option>
                          <option value="strength">Strength</option>
                          <option value="endurance">Endurance</option>
                          <option value="recomposition">Recomposition</option>
                          <option value="upper body">Upper Body</option>
                          <option value="lower body">Lower Body</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="days_per_week" className="block text-sm font-medium text-gray-700">Workout Days Per Week</label>
                        <input type="range" name="days_per_week" id="days_per_week" min="1" max="6" value={formData.days_per_week} onChange={handleNumberChange} className="w-full mt-1" required />
                        <div className="text-center mt-1">{formData.days_per_week} days</div>
                      </div>
                      <div>
                        <label htmlFor="meal_frequency" className="block text-sm font-medium text-gray-700">Preferred Meal Frequency</label>
                        <select name="meal_frequency" id="meal_frequency" value={formData.meal_frequency} onChange={handleNumberChange} className="input-field mt-1" required>
                          <option value={3}>3 meals per day</option>
                          <option value={4}>4 meals per day</option>
                        </select>
                      </div>
                    </div>
                  </div>
                ); })()}
                
                {/* Step 3: Equipment */}
                {step === 3 && (() => { return (
                  <div className="space-y-6">
                    <h3 className="text-xl font-medium text-secondary-navy">Available Equipment</h3>
                    <p className="text-secondary-grey">Select all equipment you have access to for your workouts.</p>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {[
                        'assisted machine', 'barbell', 'bodyweight', 'cable', 'dumbbell', 
                        'lever', 'machine', 'resistance band', 'smith machine'
                      ].map((equipment) => (
                        <div key={equipment} className="flex items-center">
                          <input
                            type="checkbox"
                            id={`equipment-${equipment}`}
                            checked={formData.available_equipment.includes(equipment)}
                            onChange={() => handleEquipmentChange(equipment)}
                            className="h-4 w-4 text-primary-blue focus:ring-primary-blue border-gray-300 rounded"
                          />
                          <label htmlFor={`equipment-${equipment}`} className="ml-2 block text-sm text-gray-700 capitalize">
                            {equipment}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                ); })()}
                
                {/* Navigation Buttons */}
                <div className="mt-8 flex justify-between">
                  {step > 1 ? (
                    <button type="button" onClick={prevStep} className="btn-outline">Back</button>
                  ) : (
                    <div></div> // Placeholder for alignment
                  )}
                  
                  {step < 3 ? (
                    <button type="button" onClick={(e) => nextStep(e)} className="btn-primary">Next</button>
                  ) : (
                    <button type="submit" disabled={savingProfile} className="btn-primary">
                      {savingProfile ? 'Saving Profile...' : 'Save Profile'}
                    </button>
                  )}
                </div>
              </form>
            </>
          ) : (
            // Profile Completed View
            <div className="text-center space-y-6">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-green-500 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-2xl font-semibold text-secondary-navy">Profile Saved Successfully!</h3>
              <p className="text-secondary-grey">
                Your personalized profile is ready. Now let's generate your fitness and meal plans.
              </p>
              {apiError && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 border border-red-300 rounded-md">
                  <p>{apiError}</p>
                </div>
              )}
              <button 
                type="button" 
                onClick={handleGeneratePlans} 
                disabled={generatingPlans} 
                className="btn-primary w-full md:w-auto mt-4"
              >
                {generatingPlans ? 'Generating Plans...' : 'Generate My Plans'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileSetup;

