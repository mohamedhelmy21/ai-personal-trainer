# AI Personal Trainer – Modular RAG API

A robust, modular API for meal and workout plan generation, validation, and refinement using Retrieval-Augmented Generation (RAG) and OpenAI.

---

## Features

- **Modular structure** for easy maintenance and extension
- **RAG backend** for validating and refining plans using external knowledge
- **FastAPI** endpoints for plan generation and validation
- **LangChain + OpenAI** for embeddings and LLM calls
- **Caching** for efficient retrievals
- **Extensible**: Stubs for Chroma, Anthropic, open-source LLMs, multi-user support

---

## Directory Structure

```
app/
  meal_planner/
  workout_planner/
  rag_layer/
  utils/
data/
  rag_docs/         # Add your RAG knowledge base docs here
  faiss_index/      # Vector DB indices
output/             # Generated plans
```

---

## Setup

1. **Install dependencies**
   ```bash
   pip install fastapi uvicorn langchain openai python-dotenv pandas chromadb
   ```

2. **Set your OpenAI API key**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```

3. **Add RAG documents**
   - Place `.txt`, `.md`, `.json` (and optionally `.csv`) files in `data/rag_docs/`.

---

## Running the API

```bash
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

---

## API Endpoints

### `/generate-meal-plan` and `/generate-workout-plan`
- Generate plans for a user.

### `/validate-meal-plan` and `/validate-workout-plan`
- Validate/refine plans using the RAG backend.
- **Request body:**
  ```json
  {
    "plan": { "days": [ ... ] },  // Must be a dict with a 'days' key (list of day dicts)
    "user": {
      "age": 30,
      "gender": "male",
      "height_cm": 180,
      "weight_kg": 75,
      "level": "beginner",
      "activity_level": "moderate",
      "available_equipment": ["dumbbell", "bench"],
      "days_per_week": 4,
      "goal": "muscle gain",
      "subgoal": "upper body",
      "meal_frequency": 3
    }
  }
  ```

---

## RAG Layer

- Loads and chunks docs from `data/rag_docs/`
- Embeds and stores in FAISS (with index invalidation)
- Retrieves relevant context for each validation
- Assembles prompt and calls OpenAI LLM via LangChain
- Returns only concise explanations for changed items

---

## Extending

- Add more docs to `data/rag_docs/` for better validation.
- Add PDF/DOCX parsing if needed.
- See `app/rag_layer/rag_pipeline.py` for extension stubs (Chroma, Anthropic, etc).

---

## Troubleshooting

- **422 Unprocessable Content:** Your request JSON does not match the expected schema.
- **500 Internal Server Error:** Check your OpenAI API key, plan format, and server logs.
- **UTF-8 decode error:** Remove or properly parse binary files from `data/rag_docs/`.

---

## License

MIT

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/) 