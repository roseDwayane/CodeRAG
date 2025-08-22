#!/usr/bin/env python3
"""
Fix embedding dimension mismatch issues
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_embedding_dimension():
    """Test the actual embedding dimension of the current model."""
    print("🔍 Testing embedding dimension...")
    
    try:
        # Get the current model from environment
        model = os.getenv("OLLAMA_EMBEDDING_MODEL", "llama-3.2-1b-instruct")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        print(f"📋 Testing model: {model}")
        
        # Test embedding generation
        url = f"{base_url}/api/embeddings"
        payload = {
            "model": model,
            "prompt": "test"
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            embedding = result.get("embedding", [])
            dimension = len(embedding)
            
            print(f"✅ Embedding dimension: {dimension}")
            return dimension
        else:
            print(f"❌ Failed to get embedding: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing embedding dimension: {e}")
        return None

def check_available_models():
    """Check what models are available and their dimensions."""
    print("\n🔍 Checking available models...")
    
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print("📋 Available models:")
                for model in models:
                    print(f"   - {model['name']}")
                return [m['name'] for m in models]
            else:
                print("⚠️  No models found")
                return []
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return []

def test_model_dimensions():
    """Test embedding dimensions for all available models."""
    print("\n🔍 Testing dimensions for all models...")
    
    models = check_available_models()
    if not models:
        print("❌ No models available to test")
        return {}
    
    results = {}
    
    for model_name in models:
        print(f"\n📋 Testing {model_name}...")
        try:
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            url = f"{base_url}/api/embeddings"
            payload = {
                "model": model_name,
                "prompt": "test"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                embedding = result.get("embedding", [])
                dimension = len(embedding)
                results[model_name] = dimension
                print(f"✅ {model_name}: {dimension} dimensions")
            else:
                print(f"❌ {model_name}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {model_name}: Error - {e}")
    
    return results

def update_env_file(correct_dimension):
    """Update .env file with correct embedding dimension."""
    print(f"\n🔧 Updating .env file with dimension {correct_dimension}...")
    
    env_content = f'''# Model Provider Configuration
MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama-3.2-1b-instruct
OLLAMA_EMBEDDING_MODEL=llama-3.2-1b-instruct

# Project Directory Configuration
WATCHED_DIR=.

# FAISS Configuration
FAISS_INDEX_FILE=./coderag_index.faiss
EMBEDDING_DIM={correct_dimension}
'''
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env file updated successfully!")
    
    # Reload environment variables
    load_dotenv(override=True)

def clear_faiss_index():
    """Clear the FAISS index to force recreation with correct dimension."""
    print("\n🧹 Clearing FAISS index...")
    
    try:
        import os
        
        # Remove FAISS index files
        files_to_remove = [
            "coderag_index.faiss",
            "metadata.npy",
            "./coderag_index.faiss",
            "./metadata.npy"
        ]
        
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
        
        print("✅ FAISS index cleared successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error clearing FAISS index: {e}")
        return False

def main():
    """Main function to fix embedding dimension issues."""
    print("🔧 Fixing Embedding Dimension Issues")
    print("=" * 50)
    
    # Test current model dimension
    current_dimension = test_embedding_dimension()
    
    if current_dimension is None:
        print("\n❌ Cannot test embedding dimension")
        print("💡 Please make sure Ollama is running and models are available")
        return
    
    # Test all available models
    model_dimensions = test_model_dimensions()
    
    if not model_dimensions:
        print("\n❌ No models available for testing")
        return
    
    print(f"\n📊 Model dimensions summary:")
    for model, dim in model_dimensions.items():
        print(f"   {model}: {dim} dimensions")
    
    # Find the best model to use
    current_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "llama-3.2-1b-instruct")
    
    if current_model in model_dimensions:
        correct_dimension = model_dimensions[current_model]
        print(f"\n🎯 Using model: {current_model} ({correct_dimension} dimensions)")
    else:
        # Use the first available model
        first_model = list(model_dimensions.keys())[0]
        correct_dimension = model_dimensions[first_model]
        print(f"\n⚠️  Current model not found, using: {first_model} ({correct_dimension} dimensions)")
        current_model = first_model
    
    # Update .env file
    update_env_file(correct_dimension)
    
    # Clear FAISS index
    clear_faiss_index()
    
    print("\n" + "=" * 50)
    print("🎉 Embedding dimension issue fixed!")
    print(f"📋 Configuration:")
    print(f"   Model: {current_model}")
    print(f"   Dimension: {correct_dimension}")
    print("\n📝 Next steps:")
    print("   1. Run: python main.py (to rebuild index)")
    print("   2. Run: python test_ollama_integration.py")
    print("   3. Start UI: streamlit run app.py")

if __name__ == "__main__":
    main()
