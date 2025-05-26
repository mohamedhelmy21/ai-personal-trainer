# WorkoutSplitGenerator.py
from app.user import UserProfile
from typing import Dict, List

class WorkoutSplitGenerator:
    
    @staticmethod
    def generate_weekly_split(user_profile: UserProfile) -> Dict:
        days = user_profile.days_per_week
        level = user_profile.level
        goal = user_profile.goal
        subgoal = user_profile.subgoal

        split_type = None

        # Decide split based on level and training frequency
        if level == "beginner":
            if days <= 3:
                split_type = "Full-body"
            elif days == 4:
                split_type = "Upper/Lower"
            else:
                split_type = "Upper/Lower + Full-body hybrid"
        elif level == "intermediate":
            if days == 2:
                split_type = "Upper/Lower"
            elif days == 3:
                split_type = "PPL condensed"
            elif days == 4:
                split_type = "Upper/Lower"
            elif days == 5:
                split_type = "PPL x5"
            else:
                split_type = "PPL"
        elif level == "advanced":
            if days == 2:
                split_type = "Upper/Lower"
            elif days == 3:
                split_type = "PPL condensed"
            elif days == 4:
                split_type = "Upper/Lower"
            elif days == 5:
                split_type = "PPL x5"
            else:
                split_type = "PPL"

        # Just assign N training days — no rest or cardio
        training_days = days
        days_assignment = WorkoutSplitGenerator.assign_days(split_type, training_days)

        return {
            "split_type": split_type,
            "training_days": training_days,
            "days_assignment": days_assignment
        }

    @staticmethod
    def assign_days(split_type: str, training_days: int) -> List[str]:
        SPLIT_DAY_CYCLE = {
            "Full-body": ["Full-body"],
            "Upper/Lower": ["Upper", "Lower"],
            "Upper/Lower + Full-body hybrid": ["Upper", "Lower", "Full-body"],
            "PPL": ["Push", "Pull", "Legs"],
            "PPL condensed": ["Push", "Pull", "Legs"], 
            "PPL x5": ["Push", "Pull", "Legs", "Push", "Pull"]
        }

        split_cycle = SPLIT_DAY_CYCLE.get(split_type, ["Full-body"])
        cycle_length = len(split_cycle)

        assignments = []
        for i in range(training_days):
            label = f"Day {i+1}: {split_cycle[i % cycle_length]}"
            assignments.append(label)

        return assignments
