import os
import hashlib
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.rag_layer.prompts import MEAL_DAY_VALIDATION_PROMPT, WORKOUT_DAY_VALIDATION_PROMPT
from langchain_community.vectorstores import Chroma
import chromadb
import pickle
import json
import numpy as np

# Load environment variables (for OpenAI API key)
load_dotenv()

RAG_DOCS_DIR = "data/rag_docs/"
FAISS_INDEX_DIR = "data/faiss_index/"
MEAL_INDEX_PATH = os.path.join(FAISS_INDEX_DIR, "meal_index")
WORKOUT_INDEX_PATH = os.path.join(FAISS_INDEX_DIR, "workout_index")

# --- Caching vector DBs at module level ---
_meal_vector_db = None
_workout_vector_db = None


def get_meal_vector_db():
    global _meal_vector_db
    if _meal_vector_db is None:
        docs = load_rag_docs()
        chunks = chunk_docs(docs)
        _meal_vector_db = embed_and_index_chunks(chunks, index_path=MEAL_INDEX_PATH, docs=docs)
    return _meal_vector_db

def get_workout_vector_db():
    global _workout_vector_db
    if _workout_vector_db is None:
        docs = load_rag_docs()
        chunks = chunk_docs(docs)
        _workout_vector_db = embed_and_index_chunks(chunks, index_path=WORKOUT_INDEX_PATH, docs=docs)
    return _workout_vector_db

# --- 1. Load Documents ---
def load_rag_docs(doc_dir: str = RAG_DOCS_DIR) -> List[str]:
    """
    Load all text, markdown, and JSON documents from the RAG docs directory.
    Returns a list of document strings.
    """
    docs = []
    for fname in os.listdir(doc_dir):
        fpath = os.path.join(doc_dir, fname)
        if not os.path.isfile(fpath):
            continue
        ext = fname.lower().split('.')[-1]
        try:
            if ext in ["txt", "md", "json"]:
                with open(fpath, encoding="utf-8") as f:
                    docs.append(f.read())
            elif ext == "csv":
                with open(fpath, encoding="utf-8") as f:
                    docs.append(f.read())  # or use pandas if you want to parse CSVs
            # TODO: Add PDF/DOCX parsing here if needed
            else:
                # Skip binary files for now
                continue
        except Exception as e:
            print(f"Skipping {fname}: {e}")
    return docs

# --- 2. Chunk Documents ---
def chunk_docs(docs: List[str], chunk_size: int = 800) -> List[str]:
    """
    Chunk documents by paragraph or up to chunk_size tokens/words.
    """
    import re
    chunks = []
    for doc in docs:
        paragraphs = re.split(r'\n{2,}', doc)
        for para in paragraphs:
            if len(para.split()) > chunk_size:
                # Further split long paragraphs
                words = para.split()
                for i in range(0, len(words), chunk_size):
                    chunk = ' '.join(words[i:i+chunk_size])
                    chunks.append(chunk)
            elif para.strip():
                chunks.append(para.strip())
    return chunks

# --- 3. Embed and Index Chunks with Caching and Invalidation ---
def embed_and_index_chunks(
    chunks: List[str],
    index_path: str = MEAL_INDEX_PATH,
    docs: List[str] = None,
    embedding_model_name: str = None
) -> FAISS:
    """
    Embed chunks using OpenAIEmbeddings and store/load FAISS vector DB from disk, with embedding caching.
    If index exists and hash matches, load it. Otherwise, build, cache embeddings, save index, and return.
    Embedding cache is keyed by a hash of the docs/chunks. If the docs change, cache is invalidated.
    """
    import os
    import os.path
    from datetime import datetime
    # Deterministic doc ordering for stable hash
    if docs is not None:
        docs = list(docs)
        docs.sort()  # sort docs for deterministic hash
    # Allow embedding model override via env or argument
    if embedding_model_name is None:
        embedding_model_name = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    print(f"[RAG] Using embedding model: {embedding_model_name}")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    embeddings_model = OpenAIEmbeddings(model=embedding_model_name)
    docs_hash = _get_docs_hash(docs) if docs is not None else None
    print(f"[RAG] Docs hash: {docs_hash}")
    hash_path = _hash_path(index_path)
    emb_cache_path = index_path + ".embeddings.cache"
    index_exists = os.path.exists(index_path)
    hash_exists = os.path.exists(hash_path)
    hash_matches = False
    if index_exists and hash_exists and docs_hash:
        with open(hash_path, 'r') as f:
            stored_hash = f.read().strip()
        print(f"[RAG] Stored hash: {stored_hash}")
        if stored_hash == docs_hash:
            hash_matches = True
    if index_exists and hash_matches:
        try:
            # Only load, never recompute embeddings if cache is valid!
            vector_db = FAISS.load_local(index_path, embeddings_model, allow_dangerous_deserialization=True)
            print(f"[RAG] FAISS index and doc hash match: loaded index from {index_path}")
            print(f"[RAG] [CACHE-HIT] {datetime.now().isoformat()}")
            return vector_db
        except Exception as e:
            print(f"Warning: Failed to load FAISS index, rebuilding. Error: {e}")
    # If no valid index or hash mismatch, recompute embeddings and index
    try:
        print(f"[RAG] Building embeddings and FAISS index from scratch for {index_path}")
        embeddings = embeddings_model.embed_documents(chunks)
        cache_embeddings(chunks, embeddings, emb_cache_path, mode='save')
        print(f"[RAG] Saved embeddings to cache {emb_cache_path}")
        vector_db = FAISS.from_texts(chunks, embeddings_model)
        vector_db.save_local(index_path)
        if docs_hash:
            with open(hash_path, 'w') as f:
                f.write(docs_hash)
        print(f"[RAG] [CACHE-MISS/REBUILD] {datetime.now().isoformat()}")
        return vector_db
    except Exception as e:
        raise RuntimeError(f"Embedding/indexing failed: {e}")
    # TODO: Add more efficient partial update support if only some docs change

def _get_docs_hash(docs: List[str]) -> str:
    """Compute a SHA256 hash of all document contents for index invalidation."""
    m = hashlib.sha256()
    for doc in docs:
        m.update(doc.encode('utf-8'))
    return m.hexdigest()

def _hash_path(index_path: str) -> str:
    return index_path + ".hash"

# --- 4. Retrieve Context ---
def retrieve_context(query: str, vector_db, plan_type: str, top_k: int = 3) -> str:
    """
    Retrieve top_k relevant chunks from the vector DB for the given query.
    Uses disk-based caching for retrieval results, specific to plan_type.
    """
    # Sanitize plan_type to ensure it's a valid directory name component
    safe_plan_type = "".join(c if c.isalnum() else "_" for c in plan_type.lower())
    cache_dir = os.path.join("data", "retrieval_cache", safe_plan_type)
    
    # Ensure the plan-specific cache directory exists
    os.makedirs(cache_dir, exist_ok=True)

    # The cache_retrieval_results function expects a full path for the cache file itself,
    # not just a directory. We'll create a unique filename within this directory based on the query.
    # For simplicity, let's assume cache_retrieval_results handles creating a file within cache_dir.
    # If cache_retrieval_results expects cache_path to be a file, this needs adjustment.
    # For now, passing cache_dir, assuming cache_retrieval_results appends a query-specific filename.
    # Re-evaluating: cache_retrieval_results likely takes the *directory* and manages files within it.
    # The original call was cache_retrieval_results(query, None, "data/retrieval_cache", mode='load')
    # This implies "data/retrieval_cache" was the directory.

    cached = cache_retrieval_results(query, None, cache_dir, mode='load')
    if cached is not None:
        return cached
    try:
        docs_and_scores = vector_db.similarity_search_with_score(query, k=top_k)
        context = '\n---\n'.join([doc[0].page_content for doc in docs_and_scores])
        cache_retrieval_results(query, context, cache_dir, mode='save')
        return context
    except Exception as e:
        raise RuntimeError(f"Context retrieval failed: {e}")

# --- 5. Prompt Assembly ---
def assemble_prompt(template: str, context: str, **kwargs) -> str:
    """
    Assemble a prompt using the given template, injecting context and other variables.
    """
    try:
        prompt = template.format(retrieved_context=context, **kwargs)
        return prompt
    except Exception as e:
        raise RuntimeError(f"Prompt assembly failed: {e}")

# --- 6. LLM Call ---
def call_llm(prompt: str, model: str = "gpt-4.1-mini", max_tokens: int = 2048, temperature: float = 0.2) -> str:
    """
    Call the LLM using LangChain's ChatOpenAI and return the response.
    """
    try:
        llm = ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=prompt)
        ]
        response = llm(messages)
        return response.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")

# --- Chroma Support (Stub Implementation) ---
def embed_and_index_chunks_chroma(chunks: List[str], index_path: str = None) -> Chroma:
    """
    Stub: Embed chunks using OpenAIEmbeddings and store/load Chroma vector DB from disk.
    Returns a Chroma vector DB instance. (No persistent caching yet.)
    """
    embeddings = OpenAIEmbeddings()
    # For now, use in-memory Chroma DB; add persistent_dir for real use
    chroma_db = Chroma.from_texts(chunks, embeddings, persist_directory=index_path)
    # TODO: Add persistent caching and hash-based invalidation for Chroma
    return chroma_db

# --- Anthropic/Open-Source LLM Support (TODO) ---
def call_llm_anthropic(prompt: str, model: str = "claude-3-opus", **kwargs) -> str:
    """
    TODO: Call Anthropic Claude or other open-source LLMs for RAG pipeline.
    """
    pass

# --- Open-Source Embedding Support (TODO) ---
def embed_and_index_chunks_open_source(chunks: List[str], index_path: str = None) -> None:
    """
    TODO: Use open-source embedding models (e.g., SentenceTransformers, HuggingFace) for vector DB.
    """
    pass

# --- Multi-user and Session Support (TODO) ---
def get_user_index_path(user_id: str, plan_type: str = "meal") -> str:
    """
    TODO: Return a unique FAISS index path for each user and plan type (meal/workout).
    """
    pass

# TODO: Add session-based caching and retrieval for concurrent API calls.

# --- TODOs for Future Support ---
# TODO: Add multi-user and session support for concurrent API calls.
# TODO: Add robust index invalidation/rebuilding if docs are updated (e.g., hash docs, check file mtimes, etc.)
# TODO: Add caching for embeddings and retrieval for efficiency.

# --- Embedding and Retrieval Caching (Implemented) ---
def cache_embeddings(chunks: List[str], embeddings: any, cache_path: str, mode: str = 'save') -> any:
    """
    Save or load computed embeddings to/from disk for faster reloads.
    If mode is 'save', store the embeddings. If 'load', return loaded embeddings or None if not found.
    Note: The cache_path should be keyed by the doc/chunk hash for invalidation.
    """
    if mode == 'save':
        # Assume embeddings is a numpy array or list of arrays
        with open(cache_path, 'wb') as f:
            pickle.dump(embeddings, f)
    elif mode == 'load':
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        else:
            return None
    else:
        raise ValueError("mode must be 'save' or 'load'")



def cache_retrieval_results(query: str, results: any, cache_path: str, mode: str = 'save') -> any:
    """
    Save or load retrieval results for repeated queries.
    If mode is 'save', store the results. If 'load', return loaded results or None if not found.
    """
    # Use a hash of the query to create a unique filename
    import hashlib
    query_hash = hashlib.sha256(query.encode('utf-8')).hexdigest()
    file_path = f"{cache_path}_{query_hash}.json"
    if mode == 'save':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    elif mode == 'load':
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return None
    else:
        raise ValueError("mode must be 'save' or 'load'") 