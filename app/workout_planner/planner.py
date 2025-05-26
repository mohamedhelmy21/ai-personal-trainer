from typing import Dict, Union, List
import pandas as pd
from app.user import UserProfile
from app.workout_planner.split_generator import WorkoutSplitGenerator
from app.workout_planner.cardio import CardioPlanner
from app.workout_planner.builder import WorkoutBuilder
from app.workout_planner.recovery import RecoverySupport
from app.workout_planner.registry import TEMPLATE_REGISTRY


def infer_main_muscle_from_day_type(day_type: str) -> str:
    """
    Map day type to main muscle group.
    """
    mapping = {
        "Push": "shoulders",
        "Pull": "back",
        "Legs": "legs",
        "Upper": "chest",
        "Lower": "legs",
        "Full-body": "full body",
        "Cardio": "legs"  # For dynamic drills
    }
    return mapping.get(day_type, "full body")

class WeeklyPlanBuilder:



    @staticmethod
    def generate_weekly_plan(
        user_profile: UserProfile,
        exercise_dataset: pd.DataFrame,
        template_registry: Dict[str, List[str]]
    ) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Generate a weekly workout plan for the user profile.
        Returns a dictionary mapping day labels to plan details.
        Raises Exception if unable to generate a valid plan.
        """
        # Step 1: Get weekly training day assignments
        split_info = WorkoutSplitGenerator.generate_weekly_split(user_profile)
        days_assignment = split_info["days_assignment"]

        # Step 2: Attach cardio plan (adds cardio only where applicable)
        enriched_days = CardioPlanner.attach_cardio(user_profile, days_assignment)

        # Step 3: Build each day
        weekly_plan = {}

        for day_index, (day_label, meta) in enumerate(enriched_days.items()):
            day_type = meta["type"]
            cardio_info = meta["cardio"]

            if day_type.lower() == "rest":
                weekly_plan[day_label] = "Rest Day"

            elif day_type.lower() == "cardio":
                weekly_plan[day_label] = cardio_info or "LISS 30 mins"

            else:
                # Step 3.1: Generate strength workout
                workout = WorkoutBuilder.generate_day_workout(
                    day_type, user_profile, exercise_dataset, template_registry
                )

                # Step 3.2: Attach warm-up
                main_muscle = infer_main_muscle_from_day_type(day_type)
                warmup_block, needs_in_set_warmup = RecoverySupport.get_warmup(
                    main_muscle=main_muscle,
                    difficulty=user_profile.level,
                    equipment=user_profile.available_equipment,
                    include_liss=True
                )

                if needs_in_set_warmup and workout:
                    workout[0]["note"] = "Perform first set as warm-up (reduced effort)."

                # Step 3.3: Attach cooldown
                cooldown_block = RecoverySupport.get_stretch(
                    main_muscle=main_muscle,
                    difficulty=user_profile.level,
                    equipment=user_profile.available_equipment,
                    day_group=day_type
                )

                # Step 3.4: Attach cardio add-on if any
                if cardio_info:
                    workout.append({"name": f"[Cardio Add-On] {cardio_info}", "sets": "", "reps": ""})

                # Step 3.5: Compose final day
                weekly_plan[day_label] = {
                    "type": day_type,
                    "warmup": warmup_block,
                    "workout": workout,
                    "cooldown": cooldown_block
                }

        return weekly_plan



