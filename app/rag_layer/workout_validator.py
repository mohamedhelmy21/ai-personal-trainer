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
    llm_response = call_llm(prompt, model=kwargs.get("model", "gpt-4.1-mini"))
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


def validate_workout_plan(full_plan_input: Dict[str, Any], user_profile: UserProfile, **kwargs) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates/refines a weekly workout plan, day by day.
    Accepts plan as: 
        1. {'days': [day_obj1, day_obj2, ...]}
        2. [day_obj1, day_obj2, ...] (though type hint is Dict, handles robustly)
        3. {'Day 1': day_obj1, 'Day 2': day_obj2, ...}
    Returns revised_plan (dict or list, matching input style as much as possible while adhering to Dict return hint) and explanations (list).
    Raises Exception on error or invalid output.
    """
    explanations = []
    days_iterable: List[Dict[str, Any]] = []
    input_format_type = None  # To remember how to reconstruct the plan

    if isinstance(full_plan_input, dict) and "days" in full_plan_input:
        days_list = full_plan_input.get("days")
        if not isinstance(days_list, list):
            raise Exception("Invalid plan format: 'days' key found but its value is not a list.")
        days_iterable = days_list
        input_format_type = "dict_with_days_key"
    elif isinstance(full_plan_input, list):
        # This case handles if a raw list is passed, despite type hint being Dict.
        # The function will still return a Dict as per its signature.
        if not all(isinstance(d, dict) for d in full_plan_input):
            raise Exception("Invalid plan format: Expected a list of day objects (dictionaries).")
        days_iterable = full_plan_input
        input_format_type = "list_of_days"
    elif isinstance(full_plan_input, dict):
        if not all(isinstance(v, dict) for v in full_plan_input.values()):
            raise Exception("Invalid plan format: Expected a dictionary of day objects, but values are not all dictionaries.")
        days_iterable = list(full_plan_input.values()) # Process the day objects
        input_format_type = "dict_of_day_objects"
    else:
        raise Exception("Invalid plan format: Expected a list of days, a dict with 'days' key, or a dict of day objects.")

    # Handle empty plans gracefully based on detected input type
    if not days_iterable:
        if input_format_type == "dict_with_days_key":
            return {"days": []}, []
        elif input_format_type == "list_of_days":
            return {"days": []}, [] # Adhere to Dict return type
        elif input_format_type == "dict_of_day_objects" and not full_plan_input: # e.g. {} was passed
            return {}, []
        else: # Should not be reached if logic is sound, but as a safeguard
            raise Exception("Invalid or empty plan format: No days found to process.")

    revised_day_objects_list = []
    for i, day_plan_to_validate in enumerate(days_iterable):
        if not isinstance(day_plan_to_validate, dict):
            # This check is crucial if days_iterable came from full_plan_input.values()
            # or if the list under "days" key contained non-dict items.
            raise Exception(f"Invalid day format at index {i} (plan type: {input_format_type}): expected a dictionary, got {type(day_plan_to_validate)}.")
        
        date = day_plan_to_validate.get("date") # date is optional within a day object
        revised_day_obj, explanation = validate_workout_day(day_plan_to_validate, user_profile, date=date, **kwargs)
        revised_day_objects_list.append(revised_day_obj)
        explanations.append(explanation)

    # Reconstruct the plan in its original format as best as possible while respecting Dict return type
    final_revised_plan: Dict[str, Any]
    if input_format_type == "dict_with_days_key" or input_format_type == "list_of_days":
        # If input was list_of_days, we wrap in {'days': ...} to match return type.
        final_revised_plan = {"days": revised_day_objects_list}
    elif input_format_type == "dict_of_day_objects":
        original_day_keys = list(full_plan_input.keys())
        if len(original_day_keys) != len(revised_day_objects_list):
            # This implies an internal logic error or inconsistent day processing
            raise Exception("Internal error: Mismatch between original day keys and processed day objects during reconstruction.")
        final_revised_plan = {key: day_obj for key, day_obj in zip(original_day_keys, revised_day_objects_list)}
    else:
        # This case should ideally not be reached if input_format_type is always set.
        raise Exception("Internal error: Unknown input_format_type during plan reconstruction.")
        
    return final_revised_plan, explanations

# Helper for merging days to weekly plan (customize as needed)
def merge_days_to_weekly_plan(days: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"days": days} 