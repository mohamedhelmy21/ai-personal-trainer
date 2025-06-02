import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { UserProfile } from '../types/user';

const ProfileSetup: React.FC = () => {
  const { user, setUser } = useUser();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<UserProfile>({
    age: 30,
    gender: 'male',
    height_cm: 175,
    weight_kg: 75,
    activity_level: 'moderately active',
    fitness_level: 'intermediate',
    primary_goal: 'muscle gain',
    sub_goal: '',
    workout_days_per_week: 4,
    preferred_meal_frequency: 3,
    available_equipment: ['barbell', 'dumbbell', 'bodyweight']
  });
  
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: Number(value)
    }));
  };

  const handleEquipmentChange = (equipment: string) => {
    setFormData(prev => {
      const currentEquipment = [...prev.available_equipment];
      if (currentEquipment.includes(equipment)) {
        return {
          ...prev,
          available_equipment: currentEquipment.filter(item => item !== equipment)
        };
      } else {
        return {
          ...prev,
          available_equipment: [...currentEquipment, equipment]
        };
      }
    });
  };

  const nextStep = () => {
    setStep(prev => prev + 1);
  };

  const prevStep = () => {
    setStep(prev => prev - 1);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Save user profile
    setTimeout(() => {
      setUser(formData);
      setLoading(false);
      navigate('/home');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <img
            className="mx-auto h-20 w-auto"
            src="/assets/FitGenieLogo.png"
            alt="FitGenie"
          />
          <h2 className="mt-6 text-3xl font-bold text-secondary-navy">
            Set Up Your Profile
          </h2>
          <p className="mt-2 text-secondary-grey">
            Let's personalize your fitness journey
          </p>
        </div>
        
        <div className="bg-white shadow-md rounded-lg p-8">
          <div className="mb-8">
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
          
          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <div className="space-y-6">
                <h3 className="text-xl font-medium text-secondary-navy">Basic Information</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Age */}
                  <div>
                    <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                      Age
                    </label>
                    <input
                      type="number"
                      name="age"
                      id="age"
                      min="10"
                      max="100"
                      value={formData.age}
                      onChange={handleNumberChange}
                      className="input-field mt-1"
                      required
                    />
                  </div>

                  {/* Gender */}
                  <div>
                    <label htmlFor="gender" className="block text-sm font-medium text-gray-700">
                      Gender
                    </label>
                    <select
                      name="gender"
                      id="gender"
                      value={formData.gender}
                      onChange={handleChange}
                      className="input-field mt-1"
                      required
                    >
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  {/* Height */}
                  <div>
                    <label htmlFor="height_cm" className="block text-sm font-medium text-gray-700">
                      Height (cm)
                    </label>
                    <input
                      type="number"
                      name="height_cm"
                      id="height_cm"
                      min="100"
                      max="250"
                      value={formData.height_cm}
                      onChange={handleNumberChange}
                      className="input-field mt-1"
                      required
                    />
                  </div>

                  {/* Weight */}
                  <div>
                    <label htmlFor="weight_kg" className="block text-sm font-medium text-gray-700">
                      Weight (kg)
                    </label>
                    <input
                      type="number"
                      name="weight_kg"
                      id="weight_kg"
                      min="30"
                      max="200"
                      value={formData.weight_kg}
                      onChange={handleNumberChange}
                      className="input-field mt-1"
                      required
                    />
                  </div>

                  {/* Activity Level */}
                  <div>
                    <label htmlFor="activity_level" className="block text-sm font-medium text-gray-700">
                      Activity Level
                    </label>
                    <select
                      name="activity_level"
                      id="activity_level"
                      value={formData.activity_level}
                      onChange={handleChange}
                      className="input-field mt-1"
                      required
                    >
                      <option value="sedentary">Sedentary</option>
                      <option value="lightly active">Lightly Active</option>
                      <option value="moderately active">Moderately Active</option>
                      <option value="very active">Very Active</option>
                      <option value="super active">Super Active</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
            
            {step === 2 && (
              <div className="space-y-6">
                <h3 className="text-xl font-medium text-secondary-navy">Fitness Goals</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Fitness Level */}
                  <div>
                    <label htmlFor="fitness_level" className="block text-sm font-medium text-gray-700">
                      Fitness Level
                    </label>
                    <select
                      name="fitness_level"
                      id="fitness_level"
                      value={formData.fitness_level}
                      onChange={handleChange}
                      className="input-field mt-1"
                      required
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  {/* Primary Goal */}
                  <div>
                    <label htmlFor="primary_goal" className="block text-sm font-medium text-gray-700">
                      Primary Fitness Goal
                    </label>
                    <select
                      name="primary_goal"
                      id="primary_goal"
                      value={formData.primary_goal}
                      onChange={handleChange}
                      className="input-field mt-1"
                      required
                    >
                      <option value="muscle gain">Muscle Gain</option>
                      <option value="fat loss">Fat Loss</option>
                      <option value="maintenance">Maintenance</option>
                    </select>
                  </div>

                  {/* Sub Goal */}
                  <div>
                    <label htmlFor="sub_goal" className="block text-sm font-medium text-gray-700">
                      Specific Sub-Goal (Optional)
                    </label>
                    <select
                      name="sub_goal"
                      id="sub_goal"
                      value={formData.sub_goal}
                      onChange={handleChange}
                      className="input-field mt-1"
                    >
                      <option value="">Select a sub-goal</option>
                      <option value="hypertrophy">Hypertrophy</option>
                      <option value="strength">Strength</option>
                      <option value="endurance">Endurance</option>
                      <option value="recomposition">Recomposition</option>
                      <option value="upper body">Upper Body</option>
                      <option value="lower body">Lower Body</option>
                    </select>
                  </div>

                  {/* Workout Days */}
                  <div>
                    <label htmlFor="workout_days_per_week" className="block text-sm font-medium text-gray-700">
                      Workout Days Per Week
                    </label>
                    <input
                      type="range"
                      name="workout_days_per_week"
                      id="workout_days_per_week"
                      min="1"
                      max="6"
                      value={formData.workout_days_per_week}
                      onChange={handleNumberChange}
                      className="w-full mt-1"
                      required
                    />
                    <div className="text-center mt-1">{formData.workout_days_per_week} days</div>
                  </div>

                  {/* Meal Frequency */}
                  <div>
                    <label htmlFor="preferred_meal_frequency" className="block text-sm font-medium text-gray-700">
                      Preferred Meal Frequency
                    </label>
                    <select
                      name="preferred_meal_frequency"
                      id="preferred_meal_frequency"
                      value={formData.preferred_meal_frequency}
                      onChange={handleNumberChange}
                      className="input-field mt-1"
                      required
                    >
                      <option value={3}>3 meals per day</option>
                      <option value={4}>4 meals per day</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
            
            {step === 3 && (
              <div className="space-y-6">
                <h3 className="text-xl font-medium text-secondary-navy">Available Equipment</h3>
                <p className="text-secondary-grey">
                  Select all equipment you have access to for your workouts.
                </p>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {['assisted machine', 'barbell', 'bodyweight', 'cable', 'dumbbell', 'lever', 'machine', 'resistance band', 'smith machine'].map((equipment) => (
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
            )}
            
            <div className="mt-8 flex justify-between">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={prevStep}
                  className="btn-outline"
                >
                  Back
                </button>
              ) : (
                <div></div>
              )}
              
              {step < 3 ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="btn-primary"
                >
                  Next
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Creating Your Plan...' : 'Complete Setup'}
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileSetup;
