import json
from typing import Dict, Any, List, Tuple
from app.rag_layer.rag_pipeline import retrieve_context, call_llm, get_meal_vector_db, get_workout_vector_db
from app.rag_layer.meal_validator import validate_meal_plan
from app.rag_layer.workout_validator import validate_workout_plan
from app.rag_layer.prompts import CHATBOT_SYSTEM_PROMPT, CHATBOT_QA_PROMPT, CHATBOT_PATCH_PROMPT, CHATBOT_CLARIFY_PROMPT
from app.user import UserProfile
import jsonpatch

# In-memory chat history per session
_CHAT_HISTORY: Dict[str, List[Dict[str, str]]] = {}
_PENDING_PATCHES: Dict[str, List[Dict[str, Any]]] = {} # For storing proposed JSON patches

def get_history(session_id: str) -> List[Dict[str, str]]:
    return _CHAT_HISTORY.get(session_id, [])

def save_history(session_id: str, history: List[Dict[str, str]]):
    _CHAT_HISTORY[session_id] = history

def trim_history(history: List[Dict[str, str]], max_len: int = 20) -> List[Dict[str, str]]:
    return history[-max_len:]

def save_pending_patch(session_id: str, patch: List[Dict[str, Any]]):
    _PENDING_PATCHES[session_id] = patch

def get_pending_patch(session_id: str) -> List[Dict[str, Any]] | None:
    return _PENDING_PATCHES.get(session_id)

def clear_pending_patch(session_id: str):
    _PENDING_PATCHES.pop(session_id, None)

def _format_value_for_summary(value: Any) -> str:
    """Helper to format values for the diff summary, truncating long ones."""
    if isinstance(value, (dict, list)):
        s = json.dumps(value, indent=2)
        if len(s) > 200:  # Max length for a complex value string
            return s[:197] + "..."
        return s
    # For simple types, json.dumps adds quotes to strings, which is good.
    return json.dumps(value)

def make_diff_summary(original_plan: Dict, patch: List[Dict]) -> str:
    if not patch:
        return "No changes proposed."
    
    summary_parts = []
    for op_idx, op in enumerate(patch):
        path = op.get('path')
        op_type = op.get('op')
        
        if not path or not op_type: # Basic validation of the patch operation structure
            summary_parts.append(f"- Change {op_idx+1}: Malformed operation (missing path or op type): {_format_value_for_summary(op)}")
            continue

        new_value_from_op = op.get('value') # Used by 'add' and 'replace'

        original_value_str = "(original value not found or path is new)" # Default
        original_value_exists = False
        if op_type in ['replace', 'remove']: # These ops imply the path should exist in original_plan
            try:
                pointer = jsonpatch.JsonPointer(path)
                original_value = pointer.resolve(original_plan)
                original_value_str = _format_value_for_summary(original_value)
                original_value_exists = True
            except (jsonpatch.JsonPointerException, KeyError):
                # Path doesn't exist in original_plan, or is invalid.
                pass 
        
        op_summary_prefix = f"Change {op_idx+1}: "
        current_op_summary = ""

        if op_type == 'add':
            current_op_summary = f"Add/Set at '{path}': {_format_value_for_summary(new_value_from_op)}"
            try:
                # Check if path existed to clarify if it's a pure add or a replace via 'add' op
                pointer = jsonpatch.JsonPointer(path)
                original_value_for_add_path = pointer.resolve(original_plan)
                current_op_summary += f" (replacing existing value: {_format_value_for_summary(original_value_for_add_path)})"
            except (jsonpatch.JsonPointerException, KeyError):
                 pass # Path didn't exist, so it's a pure add to a new location/key.
        
        elif op_type == 'replace':
            if 'value' not in op: # 'value' key must be present for 'replace' op per RFC 6902
                 current_op_summary = f"Malformed 'replace' at '{path}' (missing 'value'). Original value at path: {original_value_str if original_value_exists else '(path did not exist or was invalid)'}."
            else:
                current_op_summary = f"Change at '{path}' from {original_value_str} to {_format_value_for_summary(new_value_from_op)}"
        
        elif op_type == 'remove':
            current_op_summary = f"Remove from '{path}'. Value removed: {original_value_str}"
            
        else: # 'move', 'copy', 'test' - not expected from our LLM prompt which asks for add, remove, replace
            current_op_summary = f"Unsupported operation '{op_type}' at '{path}'. Details: {_format_value_for_summary(op)}"
            
        summary_parts.append(op_summary_prefix + current_op_summary)
        
    if not summary_parts: # Should not happen if patch is not empty and ops are valid
         return "No specific changes identified in the patch, or the patch was empty/malformed."
    return "\n".join(summary_parts)

def detect_intent_with_llm(message: str, plan_type: str, user_profile: Dict[str, Any], plan: Dict[str, Any], history: List[Dict[str, str]], pending_patch_exists: bool) -> str:
    plan_snippet = json.dumps(plan)[:1000]
    history_snippet = json.dumps(history[-3:]) # Show last 3 turns for context

    if pending_patch_exists:
        # If a patch is pending, the primary goal is to see if the user is confirming/denying it,
        # or providing a new edit/question which would supersede the pending patch.
        prompt = (
            f"You are an AI assistant. A set of changes to the user's {plan_type} plan has been proposed, and you asked for their confirmation."
            f"User profile: {json.dumps(user_profile)}\n"
            f"Chat History (last 3 turns, including your confirmation question): {history_snippet}\n"
            f"User's current message: \"{message}\"\n\n"
            "Classify the user's message. Respond with ONLY one word: 'confirm_edit', 'cancel_edit', 'new_edit', 'clarify', or 'info'.\n"
            "- 'confirm_edit': If the user explicitly agrees to the proposed changes (e.g., 'yes', 'ok', 'proceed', 'looks good').\n"
            "- 'cancel_edit': If the user explicitly rejects the proposed changes (e.g., 'no', 'cancel', 'don't do it').\n"
            "- 'new_edit': If the user ignores the confirmation and requests a *different* specific change to their plan.\n"
            "- 'clarify': If the user's response to the confirmation is ambiguous or asks for clarification on the proposed changes, but isn't a clear yes/no/new_edit.\n"
            "- 'info': If the user asks a general question or makes a statement unrelated to the confirmation or a new edit.\n\n"
            "Intent (confirm_edit, cancel_edit, new_edit, clarify, info):"
        )
        # Max tokens might need to be slightly larger for 'confirm_edit' or 'cancel_edit'
        response_text = call_llm(prompt, model="gpt-4.1", temperature=0.0, max_tokens=15) 
        response_lower = response_text.lower().strip()

        if "confirm_edit" in response_lower:
            return "confirm_edit"
        elif "cancel_edit" in response_lower:
            return "cancel_edit"
        elif "new_edit" in response_lower: # If user wants a new edit, treat as 'edit'
            return "edit" 
        # Clarify and info remain as specific intents if they occur during confirmation flow
        elif "clarify" in response_lower:
            return "clarify"
        elif "info" in response_lower:
            return "info"
        else:
            # Fallback: if unsure during confirmation, assume it's a new query or needs clarification
            # This might need more sophisticated handling or a default to 'clarify_confirmation'
            print(f"Unexpected confirmation intent response: {response_text}. Defaulting to 'info'.")
            return "info"
    else:
        # Original intent detection logic when no patch is pending
        prompt = (
            f"You are an AI assistant helping a user with their {plan_type} plan.\n"
            f"User profile: {json.dumps(user_profile)}\n"
            f"Current {plan_type} plan (snippet): {plan_snippet}\n"
            f"Chat History (last 3 turns): {history_snippet}\n"
            f"User message: \"{message}\"\n\n"
            "Based on the User message, classify their primary intent. Respond with ONLY one word: 'edit', 'info', or 'clarify'.\n"
            "- 'edit': If the user clearly states a specific change they want to make to their plan.\n"
            "- 'info': If the user is asking a question or seeking information not directly requesting a plan modification.\n"
            "- 'clarify': If the user's message seems to request an edit, but is ambiguous or lacks details.\n\n"
            "Intent (edit, info, or clarify):"
        )
        response_text = call_llm(prompt, model="gpt-4.1", temperature=0.0, max_tokens=10)
        response_lower = response_text.lower().strip()

        if "edit" in response_lower:
            return "edit"
        elif "clarify" in response_lower:
            return "clarify"
        elif "info" in response_lower:
            return "info"
        else:
            print(f"Unexpected intent response: {response_text}. Defaulting to 'info'.")
            return "info"

def extract_json_patch(reply: str) -> List[Dict[str, Any]] | None:
    """Extracts a JSON patch (list of operations) from the LLM's reply string.
    Ensures the returned patch is a list of dictionaries, or None if not found/invalid.
    """
    try:
        # Attempt to find a JSON array first, as patches are arrays.
        array_start_idx = reply.find('[')
        array_end_idx = reply.rfind(']') + 1

        if array_start_idx != -1 and array_end_idx > array_start_idx:
            potential_patch_str = reply[array_start_idx:array_end_idx]
            try:
                decoded_json = json.loads(potential_patch_str)
                if isinstance(decoded_json, list):
                    # Ensure all elements are dictionaries (patch operations)
                    if all(isinstance(op, dict) for op in decoded_json):
                        return decoded_json # Valid patch (could be empty list [])
                    else:
                        # It's a list, but not of dicts (e.g., list of strings)
                        return None 
            except json.JSONDecodeError:
                # String looked like an array but wasn't valid JSON.
                pass # Fall through to try object or return None

        # As a fallback, LLM might return a single patch operation as a JSON object.
        # The prompt asks for an array, but this handles slight deviations.
        obj_start_idx = reply.find('{')
        obj_end_idx = reply.rfind('}') + 1
        if obj_start_idx != -1 and obj_end_idx > obj_start_idx:
            potential_obj_str = reply[obj_start_idx:obj_end_idx]
            try:
                decoded_json = json.loads(potential_obj_str)
                if isinstance(decoded_json, dict):
                    # Check if it looks like a single patch operation (e.g., has 'op' and 'path')
                    if 'op' in decoded_json and 'path' in decoded_json:
                        return [decoded_json] # Wrap the single operation in a list
            except json.JSONDecodeError:
                # Not a valid JSON object.
                pass 
        
        return None # No valid JSON array or qualifying single object found
    except Exception: # Catch-all for any other unexpected errors during extraction
        return None

def add_to_history(session_id: str, role: str, content: str):
    """Adds a message to the chat history for the given session_id."""
    if session_id not in _CHAT_HISTORY:
        _CHAT_HISTORY[session_id] = []
    
    history = _CHAT_HISTORY[session_id]
    history.append({"role": role, "content": content})
    _CHAT_HISTORY[session_id] = trim_history(history)
    # No return needed as it modifies global directly

def chat(session_id: str, user_profile: Dict[str, Any], plan: Dict[str, Any], message: str, plan_type: str) -> Tuple[str, Dict[str, Any], List[Dict[str, str]]]:
    if hasattr(user_profile, 'model_dump_json'):
        user_profile_dict = json.loads(user_profile.model_dump_json())
    elif isinstance(user_profile, dict):
        user_profile_dict = user_profile
    else:
        user_profile_dict = {}

    add_to_history(session_id, "user", message)
    current_history = get_history(session_id)

    pending_patch = get_pending_patch(session_id)
    intent = detect_intent_with_llm(message, plan_type, user_profile_dict, plan, current_history, pending_patch_exists=bool(pending_patch))

    reply = ""
    updated_plan = plan # Default to original plan, changed only on confirmed edit
    context = None # Initialize context to be used by 'info' intent

    if pending_patch:
        if intent == "confirm_edit":
            try:
                # Apply the patch
                # Create a deep copy to ensure 'plan' is not modified if validation fails
                temp_plan_for_patching = json.loads(json.dumps(plan)) # Ensure a true deep copy for patching
                temp_updated_plan = jsonpatch.apply_patch(temp_plan_for_patching, pending_patch)
                
                # Validate the patched plan (Task 1.6)
                user_profile_obj = user_profile
                if not isinstance(user_profile, UserProfile):
                    try:
                        user_profile_obj = UserProfile(**user_profile_dict)
                    except Exception:
                        if 'user' in user_profile_dict:
                            user_profile_obj = UserProfile(**user_profile_dict['user'])
                        else:
                            # This case should be handled based on expected structure or raise error
                            print("[ERROR] Could not instantiate UserProfile for validation.") 
                            raise ValueError("Invalid user_profile structure for validation")
                
                if plan_type == "meal":
                    validated_plan, explanations = validate_meal_plan(temp_updated_plan, user_profile_obj)
                else:
                    validated_plan, explanations = validate_workout_plan(temp_updated_plan, user_profile_obj)
                
                updated_plan = validated_plan # Adopt the validated plan
                summary = "Plan updated and validated successfully!"
                if explanations:
                    if isinstance(explanations, list):
                        summary += "\n" + "\n".join([str(e) for e in explanations])
                    else:
                        summary += f"\n{explanations}"
                reply = summary
            except jsonpatch.JsonPatchException as e:
                reply = f"[ERROR: Failed to apply the proposed changes: {e}. The plan remains unchanged. Please try rephrasing your request.]"
                updated_plan = plan # Revert to original plan
            except Exception as e:
                reply = f"[ERROR: Plan validation failed after applying changes: {e}. The plan remains unchanged.]"
                updated_plan = plan # Revert to original plan
            finally:
                clear_pending_patch(session_id)
        elif intent == "cancel_edit":
            reply = "Okay, I won't make those changes. The plan remains unchanged."
            clear_pending_patch(session_id)
            updated_plan = plan
        elif intent == "edit": # New edit request while a patch was pending
            clear_pending_patch(session_id)
            # Fall through to the main 'edit' block below. 
            # RAG context will be fetched in the main block if needed (e.g., if intent somehow changed to 'info').
            pass # Let it fall through to the main intent handling for 'edit'
        elif intent == "clarify" or intent == "info":
            # User asked something else, keep patch pending and answer the question/clarification
            # The 'clarify' and 'info' blocks below will handle this.
            pass # Let it fall through to the main intent handling
        else: # Should not happen if intent detection is robust
            reply = "I'm not sure how to proceed with your response regarding the pending changes. The changes have not been applied. Could you please say 'yes' or 'no', or ask a new question?"
            # Keep patch pending for next interaction
            updated_plan = plan

    # Main intent processing block (handles cases where no patch was pending, or if it fell through from above)
    if not reply: # Only process if reply hasn't been set by pending_patch logic
        # Retrieve RAG context only if the intent requires it (currently 'info')
        if intent == "info":
            if plan_type == "meal":
                context = retrieve_context(message, get_meal_vector_db(), top_k=3)
            else:
                context = retrieve_context(message, get_workout_vector_db(), top_k=3)

        if intent == "clarify":
            prompt = CHATBOT_CLARIFY_PROMPT.format(
                user_profile=json.dumps(user_profile_dict),
                plan_type=plan_type,
                plan_snippet=json.dumps(plan)[:800],
                user_message=message
            )
            reply = call_llm(prompt, model="gpt-4o")
            updated_plan = plan 
        elif intent == "info":
            prompt = CHATBOT_QA_PROMPT.format(
                user_profile=json.dumps(user_profile_dict),
                plan_type=plan_type,
                plan_snippet=json.dumps(plan)[:800],
                retrieved_context=context,
                user_message=message
            )
            reply = call_llm(prompt, model="gpt-4o")
            updated_plan = plan
        elif intent == "edit":
            # This block is now also reached if intent was 'edit' during a pending_patch scenario (after clearing the old patch)
            prompt = CHATBOT_PATCH_PROMPT.format(
                user_profile=json.dumps(user_profile_dict),
                plan_type=plan_type,
                plan_json=json.dumps(plan),
                user_message=message
            )
            patch_str = call_llm(prompt, model="gpt-4o")
            patch = extract_json_patch(patch_str)

            if patch:
                plan_for_diff_summary = json.loads(json.dumps(plan))
                diff_summary = make_diff_summary(plan_for_diff_summary, patch)
                save_pending_patch(session_id, patch)
                reply = f"Okay, I can make the following changes:\n{diff_summary}\n\nDo you want to apply these changes? (yes/no)"
                updated_plan = plan 
            elif patch_str.strip() == "[]":
                reply = "I understand you're looking to make a change, but I couldn't determine the exact modification from your request, or it's not a change I can make. Could you please provide more details or rephrase?"
                updated_plan = plan
                clear_pending_patch(session_id)
            else:
                reply = "I had trouble understanding that as a plan modification. Could you try rephrasing? If you're asking a question, I can help with that too!"
                updated_plan = plan
                clear_pending_patch(session_id)
        else: # Fallback for intents not handled by pending_patch logic or main blocks
            if not pending_patch: # Only if not already handled by pending_patch's own 'else'
                reply = "I'm not sure how to handle that request. Could you try rephrasing?"
            # If pending_patch exists and intent was weird, the pending_patch 'else' above already set a reply.
            updated_plan = plan

    add_to_history(session_id, "assistant", reply)
    final_history = get_history(session_id)
    
    return reply, updated_plan, final_history
