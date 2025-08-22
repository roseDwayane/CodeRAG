#!/usr/bin/env python3
"""
Create a proper .env file for Ollama configuration
"""

import os

def create_env_file():
    """Create .env file with correct Ollama configuration."""
    print("🔧 Creating .env file with Ollama configuration...")
    
    env_content = '''# Model Provider Configuration
MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama-3.2-1b-instruct
OLLAMA_EMBEDDING_MODEL=llama-3.2-1b-instruct

# Project Directory Configuration
WATCHED_DIR=.

# FAISS Configuration
FAISS_INDEX_FILE=./coderag_index.faiss
EMBEDDING_DIM=4096
'''
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("\n📋 Configuration:")
    print("   MODEL_PROVIDER=ollama")
    print("   OLLAMA_BASE_URL=http://localhost:11434")
    print("   OLLAMA_CHAT_MODEL=llama-3.2-1b-instruct")
    print("   OLLAMA_EMBEDDING_MODEL=llama-3.2-1b-instruct")
    print("   EMBEDDING_DIM=4096")
    
    return True

def main():
    """Main function."""
    print("🚀 Creating .env file for Ollama")
    print("=" * 40)
    
    if create_env_file():
        print("\n" + "=" * 40)
        print("🎉 .env file created successfully!")
        print("\n📝 Next steps:")
        print("   1. Make sure Ollama is running: ollama serve")
        print("   2. Run: python fix_ollama_config.py")
        print("   3. Run: python test_ollama_integration.py")
        print("   4. Run: python setup_custom_model_windows.py")
    else:
        print("\n❌ Failed to create .env file")

if __name__ == "__main__":
    main()
