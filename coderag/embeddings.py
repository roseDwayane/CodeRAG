import numpy as np
from coderag.config import (
    MODEL_PROVIDER, 
    OPENAI_API_KEY, 
    OPENAI_EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL
)

def generate_embeddings(text):
    """Generate embeddings using either OpenAI or Ollama based on configuration."""
    if MODEL_PROVIDER.lower() == "ollama":
        return _generate_ollama_embeddings(text)
    else:
        return _generate_openai_embeddings(text)

def _generate_openai_embeddings(text):
    """Generate embeddings using OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=[text]  # Input should be a list of strings
        )
        # Extract the embedding from the response
        embeddings = response.data[0].embedding
        return np.array(embeddings).astype('float32').reshape(1, -1)
    except Exception as e:
        print(f"Error generating embeddings with OpenAI: {e}")
        return None

def _generate_ollama_embeddings(text):
    """Generate embeddings using Ollama API."""
    try:
        import requests
        import json
        
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        payload = {
            "model": OLLAMA_EMBEDDING_MODEL,
            "prompt": text
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        embeddings = result.get("embedding", [])
        
        if not embeddings:
            print("No embeddings returned from Ollama")
            return None
            
        return np.array(embeddings).astype('float32').reshape(1, -1)
    except Exception as e:
        print(f"Error generating embeddings with Ollama: {e}")
        return None