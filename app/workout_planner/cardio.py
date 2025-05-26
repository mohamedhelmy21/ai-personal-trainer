from typing import Dict, List
from app.user import UserProfile

class CardioPlanner:

    @staticmethod
    def attach_cardio(user_profile: UserProfile, days_assignment: List[str]) -> Dict[str, Dict]:
        plan = {}
        goal = user_profile.goal
        subgoal = user_profile.subgoal
        activity_level = user_profile.activity_level
        total_days = len(days_assignment)

        # Determine cardio strategy based on goal + subgoal
        cardio_schedule = CardioPlanner.get_cardio_plan(goal, subgoal)
        cardio_days = cardio_schedule["frequency"]
        cardio_type = cardio_schedule["type"]

        cardio_assigned = 0

        for i, assignment in enumerate(days_assignment):
            day_label, split_type = assignment.split(": ", 1)
            cardio = None

            # Skip cardio on leg day if possible
            if "leg" in split_type.lower() or "lower" in split_type.lower():
                plan[day_label] = {"type": split_type, "cardio": None}
                continue

            # Add cardio as an add-on to appropriate training days
            if cardio_assigned < cardio_days:
                cardio = f"{cardio_type} {'15' if cardio_type == 'HIIT' else '30'} mins"
                cardio_assigned += 1

            plan[day_label] = {"type": split_type, "cardio": cardio}

        return plan

    @staticmethod
    def get_cardio_plan(goal: str, subgoal: str) -> Dict[str, str]:
        goal = goal.lower()
        subgoal = subgoal.lower()

        if goal == "fat loss":
            if subgoal == "endurance":
                return {"type": "HIIT", "frequency": 3}
            elif subgoal == "recomposition":
                return {"type": "LISS", "frequency": 2}
            else:
                return {"type": "LISS", "frequency": 2}
        elif goal == "maintain":
            return {"type": "LISS", "frequency": 1}
        elif goal == "muscle gain":
            if subgoal in ["hypertrophy", "strength"]:
                return {"type": "LISS", "frequency": 1}
        return {"type": "LISS", "frequency": 0}
