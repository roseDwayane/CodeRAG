from coderag.config import (
    MODEL_PROVIDER,
    OPENAI_API_KEY, 
    OPENAI_CHAT_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL
)
from coderag.search import search_code

SYSTEM_PROMPT = """
You are an expert coding assistant. Your task is to help users with their question. Use the retrieved code context to inform your responses, but feel free to suggest better solutions if appropriate.
"""

PRE_PROMPT = """
Based on the user's query and the following code context, provide a helpful response. If improvements can be made, suggest them with explanations.

User Query: {query}

Retrieved Code Context:
{code_context}

Your response:
"""

def execute_rag_flow(user_query):
    try:
        # Perform code search
        search_results = search_code(user_query)
        
        if not search_results:
            return "No relevant code found for your query."
        
        # Prepare code context
        code_context = "\n\n".join([
            f"File: {result['filename']}\n{result['content']}"
            for result in search_results[:3]  # Limit to top 3 results
        ])
        
        # Construct the full prompt
        full_prompt = PRE_PROMPT.format(query=user_query, code_context=code_context)
        
        # Generate response using configured provider
        if MODEL_PROVIDER.lower() == "ollama":
            response = _generate_ollama_response(full_prompt)
        else:
            response = _generate_openai_response(full_prompt)
        
        return response
    
    except Exception as e:
        return f"Error in RAG flow execution: {e}"

def _generate_openai_response(full_prompt):
    """Generate response using OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating OpenAI response: {e}"

def _generate_ollama_response(full_prompt):
    """Generate response using Ollama API."""
    try:
        import requests
        import json
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": OLLAMA_CHAT_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\n\n{full_prompt}",
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 4000
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        return f"Error generating Ollama response: {e}"