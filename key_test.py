from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

from app.rag_layer.rag_pipeline import call_llm
print(call_llm("Say hello in JSON: {\"hello\": \"world\"}"))