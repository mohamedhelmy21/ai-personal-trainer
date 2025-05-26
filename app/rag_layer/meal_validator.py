import json
from typing import Tuple, Dict, Any, List
from app.user import UserProfile
from app.rag_layer.rag_pipeline import (
    load_rag_docs, chunk_docs, embed_and_index_chunks, retrieve_context, assemble_prompt, call_llm
)
from app.rag_layer.prompts import MEAL_DAY_VALIDATION_PROMPT

# Placeholder for future RAG/LLM imports (e.g., LangChain, OpenAI)
# from langchain import ...


def validate_meal_day(day_plan: Dict[str, Any], user_profile: UserProfile, date: str = None, **kwargs) -> Tuple[Dict[str, Any], str]:
    """
    Validate and refine a single day's meal plan using RAG.
    Returns revised_day_plan (dict) and explanation (str).
    Raises Exception on error or invalid output.
    """
    docs = load_rag_docs()
    chunks = chunk_docs(docs)
    vector_db = embed_and_index_chunks(chunks)
    query = f"Validate this meal plan: {day_plan} for user: {user_profile.to_dict()}"
    context = retrieve_context(query, vector_db, top_k=5)
    prompt = assemble_prompt(
        MEAL_DAY_VALIDATION_PROMPT,
        context,
        user_profile=user_profile.to_dict(),
        date=date or "",
        day_plan=day_plan
    )
    llm_response = call_llm(prompt, model=kwargs.get("model", "gpt-4o"))
    try:
        result = json.loads(llm_response)
        revised_plan = result.get("revised_plan")
        if revised_plan is None:
            raise ValueError("Missing 'revised_plan' in LLM output.")
        # Only include explanations for changed items, max 20 words
        for meal in revised_plan:
            if meal.get("explanation") and meal["explanation"] != "No changes needed":
                meal["explanation"] = meal["explanation"][:20]
        overall_explanation = result.get("overall_explanation", "")[:20]
        return result, overall_explanation
    except Exception as e:
        raise RuntimeError(f"Invalid LLM output or JSON parse error: {e}\nRaw output: {llm_response}")


def validate_meal_plan(full_plan: Dict[str, Any], user_profile: UserProfile, macro_targets: Dict[str, Any] = None, **kwargs) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates/refines a weekly meal plan, day by day.
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
        revised_day, explanation = validate_meal_day(day, user_profile, macro_targets=macro_targets, date=date, **kwargs)
        revised_days.append(revised_day)
        explanations.append(explanation)
    revised_plan = {"days": revised_days}
    return revised_plan, explanations

# Helper for merging days to weekly plan (customize as needed)
def merge_days_to_weekly_plan(days: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"days": days} 