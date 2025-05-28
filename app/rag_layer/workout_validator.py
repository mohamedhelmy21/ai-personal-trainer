import json
import re
from typing import Tuple, Dict, Any, List
from app.user import UserProfile
from app.rag_layer.rag_pipeline import (
    load_rag_docs, chunk_docs, embed_and_index_chunks, retrieve_context, assemble_prompt, call_llm
)
from app.rag_layer.prompts import WORKOUT_DAY_VALIDATION_PROMPT

# Helper to clean LLM output

def clean_llm_json_output(llm_response: str) -> str:
    """
    Remove code fences (```json ... ```) from LLM output before JSON parsing.
    """
    return re.sub(r"^```(?:json)?\s*|```$", "", llm_response.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()


def validate_workout_day(day_plan: Dict[str, Any], user_profile: UserProfile, date: str = None, **kwargs) -> Tuple[Dict[str, Any], str]:
    """
    Validate and refine a single day's workout plan using RAG.
    Returns revised_day_plan (dict) and explanation (str).
    Raises Exception on error or invalid output.
    """
    from app.rag_layer.rag_pipeline import get_workout_vector_db
    vector_db = get_workout_vector_db()
    query = f"Validate this workout plan: {day_plan} for user: {user_profile.to_dict()}"
    context = retrieve_context(query, vector_db, top_k=5)
    print("[RAG][DEBUG] Retrieved context for workout validation:\n", context)
    prompt = assemble_prompt(
        WORKOUT_DAY_VALIDATION_PROMPT,
        context,
        user_profile=user_profile.to_dict(),
        date=date or "",
        day_plan=day_plan
    )
    llm_response = call_llm(prompt, model=kwargs.get("model", "gpt-4o"))
    try:
        cleaned = clean_llm_json_output(llm_response)
        result = json.loads(cleaned)
        revised_plan = result.get("revised_plan")
        if revised_plan is None:
            raise ValueError("Missing 'revised_plan' in LLM output.")
        # Only include explanations/suggestions for changed items, max 20 words
        suggestions = result.get("suggestions", [])
        for suggestion in suggestions:
            if suggestion.get("rationale"):
                suggestion["rationale"] = suggestion["rationale"][:20]
        return result, "; ".join([s.get("rationale", "") for s in suggestions if s.get("rationale")])
    except Exception as e:
        raise RuntimeError(f"Invalid LLM output or JSON parse error: {e}\nRaw output: {llm_response}")


def validate_workout_plan(full_plan: Dict[str, Any], user_profile: UserProfile, **kwargs) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates/refines a weekly workout plan, day by day.
    Returns revised_plan (dict) and explanations (list).
    Raises Exception on error or invalid output.
    """
    revised_days = []
    explanations = []
    days = full_plan.get("days") if isinstance(full_plan, dict) and "days" in full_plan else full_plan
    if not isinstance(days, list):
        raise Exception("Invalid plan format: expected a list of days or a dict with 'days' key.")
    for i, day in enumerate(days):
        date = day.get("date") if isinstance(day, dict) else None
        revised_day, explanation = validate_workout_day(day, user_profile, date=date, **kwargs)
        revised_days.append(revised_day)
        explanations.append(explanation)
    revised_plan = {"days": revised_days}
    return revised_plan, explanations

# Helper for merging days to weekly plan (customize as needed)
def merge_days_to_weekly_plan(days: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"days": days} 