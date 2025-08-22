#!/usr/bin/env python3
"""
Test script to verify Ollama integration with CodeRAG
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ollama_connection():
    """Test basic Ollama connection and model availability."""
    try:
        import requests
        
        # Test Ollama server connection
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        response = requests.get(f"{base_url}/api/tags")
        
        if response.status_code == 200:
            print("✅ Ollama server is running")
            models = response.json().get("models", [])
            if models:
                print(f"📋 Available models: {[m['name'] for m in models]}")
                
                # Check for our custom model
                custom_model = "llama-3.2-1b-instruct"
                model_names = [m['name'] for m in models]
                if custom_model in model_names:
                    print(f"✅ Custom model '{custom_model}' is available")
                else:
                    print(f"⚠️  Custom model '{custom_model}' not found")
                    print("   Run: python setup_custom_model.py")
            else:
                print("⚠️  No models found. You may need to create a model first.")
                print("   Run: python setup_custom_model.py")
        else:
            print(f"❌ Failed to connect to Ollama server: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False
    
    return True

def test_embeddings():
    """Test embedding generation with Ollama."""
    try:
        from coderag.embeddings import generate_embeddings
        
        # Temporarily set provider to ollama
        os.environ["MODEL_PROVIDER"] = "ollama"
        
        test_text = "This is a test for Ollama embeddings"
        embeddings = generate_embeddings(test_text)
        
        if embeddings is not None:
            print(f"✅ Embeddings generated successfully. Shape: {embeddings.shape}")
            return True
        else:
            print("❌ Failed to generate embeddings")
            return False
            
    except Exception as e:
        print(f"❌ Error testing embeddings: {e}")
        return False

def test_chat():
    """Test chat completion with Ollama."""
    try:
        from prompt_flow import _generate_ollama_response
        
        # Temporarily set provider to ollama
        os.environ["MODEL_PROVIDER"] = "ollama"
        
        test_prompt = "Hello, can you help me with a simple coding question?"
        response = _generate_ollama_response(test_prompt)
        
        if response and not response.startswith("Error"):
            print("✅ Chat completion successful")
            print(f"📝 Response preview: {response[:100]}...")
            return True
        else:
            print(f"❌ Chat completion failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing chat: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Ollama Integration with CodeRAG")
    print("=" * 50)
    
    # Check if MODEL_PROVIDER is set to ollama
    provider = os.getenv("MODEL_PROVIDER", "openai")
    if provider.lower() != "ollama":
        print(f"⚠️  MODEL_PROVIDER is set to '{provider}', not 'ollama'")
        print("   This test will temporarily override it for testing purposes.")
    
    print()
    
    # Run tests
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Embeddings Generation", test_embeddings),
        ("Chat Completion", test_chat)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ollama integration is working correctly.")
        print("\n📝 To use Ollama with CodeRAG:")
        print("   1. Set MODEL_PROVIDER=ollama in your .env file")
        print("   2. Make sure your Ollama model is available")
        print("   3. Update EMBEDDING_DIM if needed for your model")
        print("   4. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check your Ollama setup.")
        print("\n💡 Troubleshooting tips:")
        print("   - Make sure Ollama is running: ollama serve")
        print("   - Pull a model: ollama pull llama2")
        print("   - Check Ollama URL in .env file")
        print("   - Verify model names in .env file")

if __name__ == "__main__":
    main()
