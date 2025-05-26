import random
import pandas as pd
from typing import List, Dict
from app.user import UserProfile
from typing import Union

class WorkoutBuilder:

    LEVEL_MAP = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3
    }

    REPS_SETS_MAP = {
        "hypertrophy": {"reps": "8-12", "sets": 3},
        "strength": {"reps": "4-6", "sets": 4},
        "recomposition": {"reps": "10-15", "sets": 3},
        "endurance": {"reps": "12-20", "sets": 2},
        "general": {"reps": "8-12", "sets": 3}
    }

    @staticmethod
    def generate_day_workout(
        day_type: str,
        user_profile: UserProfile,
        exercise_dataset: pd.DataFrame,
        template_registry: Dict[str, List[str]]
    ) -> List[Dict[str, str]]:
        
        user_equipment = [e.lower() for e in user_profile.available_equipment]
        user_level = WorkoutBuilder.LEVEL_MAP.get(user_profile.level, 1)
        subgoal = user_profile.subgoal.lower()
        goal_params = WorkoutBuilder.REPS_SETS_MAP.get(subgoal, {"reps": "8-12", "sets": 3})

        workout = []
        template_group = template_registry.get(day_type, [])
        template_exercises = random.choice(template_group) if isinstance(template_group[0], list) else template_group


        for base_name in template_exercises:
            # Filter valid exercises
            selected = WorkoutBuilder.find_primary_match(exercise_dataset, base_name, user_profile)

            if selected is not None:
                workout.append({
                    "name": f"{selected['equipment_clean']} {selected['exercise_name']}".lower(),
                    "sets": goal_params["sets"],
                    "reps": goal_params["reps"]
                })
            else:
                fallback = WorkoutBuilder.find_muscle_based_alternative(exercise_dataset, base_name, user_profile)

                if fallback:
                    workout.append({
                        "name": f"{fallback} (fallback)",
                        "sets": goal_params["sets"],
                        "reps": goal_params["reps"]
                    })
                else:
                    # Last resort — relax difficulty
                    relaxed = WorkoutBuilder.find_primary_match(exercise_dataset, base_name, user_profile, boost_difficulty=True)
                    if relaxed is not None:
                        workout.append({
                            "name": f"{relaxed['equipment_clean']} {relaxed['exercise_name']} (difficulty adjusted)".lower(),
                            "sets": goal_params["sets"],
                            "reps": goal_params["reps"]
                        })
                    else:
                        workout.append({
                            "name": f"{base_name} (no match found)",
                            "sets": goal_params["sets"],
                            "reps": goal_params["reps"]
                        })


        return workout
    
    @staticmethod
    def find_muscle_based_alternative(
        exercise_dataset: pd.DataFrame,
        base_name: str,
        user_profile: UserProfile
    ) -> str:
        user_equipment = [e.lower() for e in user_profile.available_equipment]
        user_level = WorkoutBuilder.LEVEL_MAP.get(user_profile.level, 1)

        # Try to locate base exercise metadata
        reference_rows = exercise_dataset[
            exercise_dataset["base_name"].str.lower() == base_name.lower()
        ]

        if reference_rows.empty:
            return None

        reference = reference_rows.iloc[0]
        main_muscle = reference["main_muscle_clean"]
        is_compound = reference["is_compound"]
        target_muscles = set(str(reference.get("target_muscle_list", "")).lower().split(","))

        # Filter alternatives
        def exact_target_match(row):
            row_targets = set(str(row.get("target_muscle_list", "")).lower().split(","))
            return row_targets == target_muscles

        filtered = exercise_dataset[
            (exercise_dataset["main_muscle_clean"] == main_muscle) &
            (exercise_dataset["equipment_clean"].str.lower().isin(user_equipment)) &
            (exercise_dataset["difficulty_level"].map(WorkoutBuilder.LEVEL_MAP.get).fillna(0) <= user_level) &
            (exercise_dataset["is_compound"] == is_compound)
        ]

        filtered = filtered[filtered.apply(exact_target_match, axis=1)]

        if not filtered.empty:
            selected = filtered.sample(1).iloc[0]
            # Reject bodyweight fallback if user has more than just bodyweight
            if (
                selected["equipment_clean"].lower() == "bodyweight"
                and any(eq for eq in user_equipment if eq != "bodyweight")
            ):
                return None

            return f"{selected['equipment_clean']} {selected['exercise_name']}".lower()


        return None

    
    @staticmethod
    def find_primary_match(
        exercise_dataset: pd.DataFrame,
        base_name: str,
        user_profile: UserProfile,
        boost_difficulty: bool = False
    ) -> Union[pd.Series, None]:
        user_equipment = [e.lower() for e in user_profile.available_equipment]
        user_level = WorkoutBuilder.LEVEL_MAP.get(user_profile.level, 1)
        max_level = user_level + 1 if boost_difficulty else user_level

        # Get base exercise metadata
        reference = exercise_dataset[
            exercise_dataset["base_name"].str.lower() == base_name.lower()
        ]
        if reference.empty:
            return None

        reference_row = reference.iloc[0]
        target_muscles = set(str(reference_row.get("target_muscle_list", "")).lower().split(","))

        # Get all matches that match equipment and difficulty
        matches = exercise_dataset[
            (exercise_dataset["base_name"].str.lower() == base_name.lower()) &
            (exercise_dataset["equipment_clean"].str.lower().isin(user_equipment)) &
            (exercise_dataset["difficulty_level"].map(WorkoutBuilder.LEVEL_MAP.get).fillna(0) <= max_level)
        ]

        # Now apply stricter filter based on target muscles
        def exact_match(row):
            row_targets = set(str(row.get("target_muscle_list", "")).lower().split(","))
            return row_targets == target_muscles

        filtered = matches[matches.apply(exact_match, axis=1)]

        if not filtered.empty:
            return filtered.sample(1).iloc[0]
        return None



