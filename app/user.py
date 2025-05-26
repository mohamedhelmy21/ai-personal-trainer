from typing import List, Optional, Dict, Tuple, Any

class UserProfile:
    """
    Unified user profile for meal and workout planning.
    Stores macros and meal_macros for later use (e.g., RAG layer).
    """
    def __init__(
        self,
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float,
        level: str,                  # beginner, intermediate, advanced
        activity_level: str,         # sedentary → super active
        available_equipment: List[str],  # e.g., ["dumbbell", "bodyweight"]
        days_per_week: int,
        goal: str,                   # e.g., "fat loss", "muscle gain", "general", "recomposition"
        subgoal: str,                # e.g., "endurance", "hypertrophy", etc.
        meal_frequency: Optional[int] = 3   # Number of meals per day, for meal planner
    ):
        self.age = age
        self.gender = gender.lower()
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.level = level.lower()
        self.activity_level = activity_level.lower()
        self.available_equipment = [e.lower() for e in available_equipment]
        self.days_per_week = max(1, min(days_per_week, 7))   # safety bound
        self.goal = goal.lower()
        self.subgoal = subgoal.lower()
        self.meal_frequency = meal_frequency if meal_frequency is not None else 3
        # Macros and meal_macros for RAG or later use
        self.macros: Optional[Dict[str, Any]] = None
        self.meal_macros: Optional[Dict[str, Any]] = None
        # Add other fields as needed by either planner

    def set_macros(self, macros: Dict[str, Any]) -> None:
        """
        Store the user's daily macros (e.g., protein, fat, carbs, tdee).
        """
        self.macros = macros

    def set_meal_macros(self, meal_macros: Dict[str, Any]) -> None:
        """
        Store the user's per-meal macros (e.g., macro breakdown per meal type).
        """
        self.meal_macros = meal_macros

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'UserProfile':
        return cls(**{k: v for k, v in d.items() if k not in ('macros', 'meal_macros')})
