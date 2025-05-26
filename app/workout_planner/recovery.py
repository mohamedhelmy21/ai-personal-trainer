from app.workout_planner.protocols import WARMUP_PROTOCOL, STRETCHING_PROTOCOL
from typing import List, Dict, Tuple
import random


class RecoverySupport:

    FALLBACK_GROUPS = {
    "push": ["chest", "shoulders", "arms"],
    "pull": ["back", "arms"],
    "legs": ["legs"],
    "upper": ["chest", "shoulders", "triceps", "back", "biceps"], 
    "lower": ["legs"],
    "core": ["abdominals", "lower back"]
}

    @staticmethod
    def get_warmup(main_muscle: str, difficulty: str, equipment: List[str], include_liss: bool = True) -> Tuple[List[Dict[str, str]], bool]:
        warmup_block = []
        needs_in_set_warmup = False

        # Phase 1 — LISS (only if flag is True)
        if include_liss:
            for option in WARMUP_PROTOCOL["general_liss"]:
                if any(eq in equipment for eq in option["equipment"]):
                    warmup_block.append({
                        "phase": "liss_cardio",
                        "name": option["name"],
                        "prescription": option["duration"]
                    })
                    break

        # Phase 2 — Dynamic mobility
        mobility_drills = [
            d for d in WARMUP_PROTOCOL["dynamic_mobility"]
            if d["main_muscle"] == main_muscle and d["difficulty"] == difficulty
        ]

        if mobility_drills:
            for drill in mobility_drills[:2]:
                warmup_block.append({
                    "phase": "dynamic_mobility",
                    "name": drill["name"],
                    "prescription": drill["prescription"]
                })
        else:
            needs_in_set_warmup = True

        return warmup_block, needs_in_set_warmup

    @staticmethod
    def get_stretch(
        main_muscle: str,
        difficulty: str,
        equipment: List[str],
        day_group: str = None
    ) -> List[Dict[str, str]]:
        stretch_block = []

        main_muscle = main_muscle.lower()
        difficulty = difficulty.lower()
        equipment = [e.lower() for e in equipment]

        def has_required_equipment(stretch):
            required = stretch.get("equipment", [])
            return (
                not required
                or any(eq in equipment for eq in required)
            )

        # Step 1: Exact match
        candidates = [
            s for s in STRETCHING_PROTOCOL
            if s["main_muscle"] == main_muscle
            and s["difficulty"] == difficulty
            and has_required_equipment(s)
        ]

        # Step 2: Relax difficulty
        if not candidates:
            candidates = [
                s for s in STRETCHING_PROTOCOL
                if s["main_muscle"] == main_muscle
                and has_required_equipment(s)
            ]

        # Step 3: Use fallback group
        if not candidates and day_group:
            related = RecoverySupport.FALLBACK_GROUPS.get(day_group.lower(), [])
            candidates = [
                s for s in STRETCHING_PROTOCOL
                if s["main_muscle"] in related
                and has_required_equipment(s)
            ]

        # Step 4: Return random sample
        if not candidates:
            return []

        for s in random.sample(candidates, min(len(candidates), 3)):
            stretch_block.append({
                "name": s["name"],
                "prescription": s["prescription"]
            })

        return stretch_block


