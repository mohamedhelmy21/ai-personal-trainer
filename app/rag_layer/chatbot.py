import json
from typing import Dict, Any, List, Tuple
from app.rag_layer.rag_pipeline import retrieve_context, call_llm, get_meal_vector_db, get_workout_vector_db
from app.rag_layer.meal_validator import validate_meal_plan
from app.rag_layer.workout_validator import validate_workout_plan
from app.rag_layer.prompts import CHATBOT_SYSTEM_PROMPT, CHATBOT_QA_PROMPT, CHATBOT_PATCH_PROMPT

# In-memory chat history per session
_CHAT_HISTORY: Dict[str, List[Dict[str, str]]] = {}

def get_history(session_id: str) -> List[Dict[str, str]]:
    return _CHAT_HISTORY.get(session_id, [])

def save_history(session_id: str, history: List[Dict[str, str]]):
    _CHAT_HISTORY[session_id] = history

def trim_history(history: List[Dict[str, str]], max_len: int = 20) -> List[Dict[str, str]]:
    return history[-max_len:]

def detect_intent_with_llm(message: str, plan_type: str, user_profile: Dict[str, Any], plan: Dict[str, Any], history: List[Dict[str, str]]) -> str:
    prompt = (
        f"User profile: {json.dumps(user_profile)}\n"
        f"Plan type: {plan_type}\n"
        f"Plan: {json.dumps(plan)[:600]}\n"
        f"History: {history}\n"
        f"User message: {message}\n"
        "Classify the user intent as one of: 'edit' (explicit request to change the plan), 'clarify' (complaint, suggestion, pain, or advice request), or 'info' (general question). Only return 'edit', 'clarify', or 'info'."
    )
    response = call_llm(prompt, model="gpt-4.1", temperature=0.0, max_tokens=1)
    if "edit" in response.lower():
        return "edit"
    elif "clarify" in response.lower():
        return "clarify"
    else:
        return "info"

def extract_json_patch(reply: str) -> Any:
    try:
        # Find first JSON object or array in reply
        start = reply.find('{')
        end = reply.rfind('}') + 1
        if start == -1 or end == -1:
            start = reply.find('[')
            end = reply.rfind(']') + 1
        patch = json.loads(reply[start:end])
        return patch
    except Exception:
        return None

def chat(session_id: str, user_profile: Dict[str, Any], plan: Dict[str, Any], message: str, plan_type: str) -> Tuple[str, Dict[str, Any], List[Dict[str, str]]]:
    history = get_history(session_id)
    history = trim_history(history + [{"role": "user", "content": message}])

    # Step 1: Detect intent
    intent = detect_intent_with_llm(message, plan_type, user_profile, plan, history)

    # Step 2: Retrieve RAG context
    if plan_type == "meal":
        vector_db = get_meal_vector_db()
    else:
        vector_db = get_workout_vector_db()
    context = retrieve_context(message, vector_db, top_k=3)

    if intent == "info":
        prompt = CHATBOT_QA_PROMPT.format(
            user_profile=json.dumps(user_profile),
            plan_type=plan_type,
            plan_snippet=json.dumps(plan)[:800],
            retrieved_context=context,
            user_message=message
        )
        reply = call_llm(prompt, model="gpt-4o")
        updated_plan = plan
    elif intent == "clarify":
        prompt = CHATBOT_CLARIFY_PROMPT.format(
            user_profile=json.dumps(user_profile),
            plan_type=plan_type,
            plan_snippet=json.dumps(plan)[:800],
            retrieved_context=context,
            user_message=message
        )
        reply = call_llm(prompt, model="gpt-4o")
        updated_plan = plan
    else:
        # 'edit' intent: get LLM to generate a full updated plan
        prompt = CHATBOT_PATCH_PROMPT.format(
            user_profile=json.dumps(user_profile),
            plan_type=plan_type,
            plan_json=json.dumps(plan),
            user_message=message
        )
        reply = call_llm(prompt, model="gpt-4o")
        patch = extract_json_patch(reply)
        updated_plan = patch if patch else plan
        # Ensure plan is dict with 'days' key for validator
        if isinstance(updated_plan, list):
            updated_plan = {"days": updated_plan}
        elif isinstance(updated_plan, dict) and "days" not in updated_plan:
            # If it's a single day dict, wrap in a list
            updated_plan = {"days": [updated_plan]}
        # RAG-validation after edit
        try:
            # Convert user_profile dict to UserProfile object for validation
            from app.user import UserProfile
            user_profile_obj = UserProfile(**user_profile)
            if plan_type == "meal":
                validated_plan, explanations = validate_meal_plan(updated_plan, user_profile_obj)
                updated_plan = validated_plan
            else:
                validated_plan, explanations = validate_workout_plan(updated_plan, user_profile_obj)
                updated_plan = validated_plan
            # Optionally, append explanations to reply
            if explanations:
                if isinstance(explanations, list):
                    reply += "\n" + "\n".join([str(e) for e in explanations])
                else:
                    reply += f"\n{explanations}"
        except Exception as e:
            reply += f"\n[ERROR: Plan validation failed: {e}]"

    # Update assistant reply in history and save
    history = trim_history(history + [{"role": "assistant", "content": reply}])
    save_history(session_id, history)
    return reply, updated_plan, history
