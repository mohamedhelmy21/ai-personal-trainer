import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/layout/Header';
import Layout from '../components/layout/Layout';
import { useUser } from '../context/UserContext';
import { UserProfile } from '../types/user';

const Profile: React.FC = () => {
  const { user, setUser, logout } = useUser();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<UserProfile | null>(user);
  const [loading, setLoading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData(user);
    }
  }, [user]);

  if (!formData) {
    return (
      <>
        <Header />
        <Layout>
          <div className="max-w-3xl mx-auto">
            <div className="bg-white shadow-sm rounded-lg p-6">
              <h1 className="text-2xl font-bold text-secondary-navy mb-6">Profile</h1>
              <p className="text-secondary-grey">Loading profile data...</p>
            </div>
          </div>
        </Layout>
      </>
    );
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev!,
      [name]: value
    }));
  };

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev!,
      [name]: Number(value)
    }));
  };

  const handleEquipmentChange = (equipment: string) => {
    setFormData(prev => {
      const currentEquipment = [...prev!.available_equipment];
      if (currentEquipment.includes(equipment)) {
        return {
          ...prev!,
          available_equipment: currentEquipment.filter(item => item !== equipment)
        };
      } else {
        return {
          ...prev!,
          available_equipment: [...currentEquipment, equipment]
        };
      }
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Save user profile
    setTimeout(() => {
      if (formData) {
        setUser(formData);
      }
      setLoading(false);
      
      // Show success message
      alert('Profile updated successfully!');
    }, 1000);
  };

  const handleRerunOnboarding = () => {
    navigate('/profile-setup');
  };

  const handleLogout = () => {
    setShowConfirm(true);
  };

  const confirmLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      <Header />
      <Layout>
        <div className="max-w-3xl mx-auto">
          <div className="bg-white shadow-sm rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-secondary-navy">Profile Settings</h1>
              <div className="flex space-x-3">
                <button
                  onClick={handleRerunOnboarding}
                  className="btn-outline"
                >
                  Rerun Onboarding
                </button>
                <button
                  onClick={handleLogout}
                  className="btn-secondary"
                >
                  Logout
                </button>
              </div>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
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
                    value={formData.sub_goal || ''}
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

              {/* Available Equipment */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Available Equipment
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
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

              {/* Password Change Section */}
              <div className="border-t pt-6">
                <h2 className="text-lg font-medium text-secondary-navy mb-4">Change Password</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="current_password" className="block text-sm font-medium text-gray-700">
                      Current Password
                    </label>
                    <input
                      type="password"
                      id="current_password"
                      className="input-field mt-1"
                      placeholder="Enter current password"
                    />
                  </div>
                  <div>
                    <label htmlFor="new_password" className="block text-sm font-medium text-gray-700">
                      New Password
                    </label>
                    <input
                      type="password"
                      id="new_password"
                      className="input-field mt-1"
                      placeholder="Enter new password"
                    />
                  </div>
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => alert('Password change feature is mocked for demo')}
                  >
                    Update Password
                  </button>
                </div>
              </div>

              {/* Notification Preferences */}
              <div className="border-t pt-6">
                <h2 className="text-lg font-medium text-secondary-navy mb-4">Notification Preferences</h2>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <input
                      id="workout_reminders"
                      type="checkbox"
                      className="h-4 w-4 text-primary-blue focus:ring-primary-blue border-gray-300 rounded"
                      defaultChecked
                    />
                    <label htmlFor="workout_reminders" className="ml-2 block text-sm text-gray-700">
                      Workout Reminders
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="meal_reminders"
                      type="checkbox"
                      className="h-4 w-4 text-primary-blue focus:ring-primary-blue border-gray-300 rounded"
                      defaultChecked
                    />
                    <label htmlFor="meal_reminders" className="ml-2 block text-sm text-gray-700">
                      Meal Reminders
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="progress_updates"
                      type="checkbox"
                      className="h-4 w-4 text-primary-blue focus:ring-primary-blue border-gray-300 rounded"
                      defaultChecked
                    />
                    <label htmlFor="progress_updates" className="ml-2 block text-sm text-gray-700">
                      Weekly Progress Updates
                    </label>
                  </div>
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Layout>

      {/* Logout Confirmation Modal */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-secondary-navy mb-4">Confirm Logout</h3>
            <p className="text-secondary-grey mb-6">Are you sure you want to log out of your FitGenie account?</p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowConfirm(false)}
                className="btn-outline"
              >
                Cancel
              </button>
              <button
                onClick={confirmLogout}
                className="btn-primary"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Profile;
