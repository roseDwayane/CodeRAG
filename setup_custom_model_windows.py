#!/usr/bin/env python3
"""
Windows-compatible setup script for custom Llama-3.2-1B-Instruct-GGUF model
"""

import os
import subprocess
import sys

def create_modelfile():
    """Create the Modelfile for the custom model."""
    modelfile_content = '''FROM hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>"""

PARAMETER stop "<|end|>"
PARAMETER stop "<|user|>"
PARAMETER stop "<|system|>"
'''
    
    with open('Modelfile', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("✅ Modelfile created successfully")

def create_env_file():
    """Create .env file with the correct configuration."""
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
    
    print("✅ .env file created successfully")

def check_ollama_installation():
    """Check if Ollama is installed and running."""
    try:
        # Use shell=True for better Windows compatibility
        result = subprocess.run('ollama --version', shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Ollama is installed: {version}")
            return True
        else:
            print("❌ Ollama is not properly installed")
            return False
    except Exception as e:
        print(f"❌ Ollama is not installed or not in PATH: {e}")
        print("   Please install Ollama from https://ollama.ai/")
        return False

def create_model():
    """Create the custom model using Ollama."""
    try:
        print("🔄 Creating custom model...")
        # Use shell=True for better Windows compatibility
        result = subprocess.run(
            'ollama create llama-3.2-1b-instruct -f Modelfile', 
            shell=True,
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("✅ Custom model created successfully")
            # Show any output from the creation process
            if result.stdout.strip():
                print(f"📝 Output: {result.stdout.strip()}")
            return True
        else:
            stderr = result.stderr.strip()
            if stderr:
                print(f"❌ Failed to create model: {stderr}")
            else:
                print("❌ Failed to create model: (no error message)")
            return False
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        return False

def test_model():
    """Test the created model."""
    try:
        print("🔄 Testing model...")
        # Use shell=True for better Windows compatibility
        result = subprocess.run(
            'ollama run llama-3.2-1b-instruct "Hello"', 
            shell=True,
            capture_output=True, 
            text=True, 
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("✅ Model test successful")
            response = result.stdout.strip()
            if response:
                print(f"📝 Response: {response}")
            else:
                print("📝 Response: (empty response, this is normal for first run)")
            return True
        else:
            stderr = result.stderr.strip()
            if stderr:
                print(f"❌ Model test failed: {stderr}")
            else:
                print("❌ Model test failed: (no error message)")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Model test timed out (this is normal for first run)")
        return True
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Llama-3.2-1B-Instruct-GGUF for CodeRAG (Windows)")
    print("=" * 60)
    
    # Check Ollama installation
    if not check_ollama_installation():
        print("\n💡 Please install Ollama first:")
        print("   Visit: https://ollama.ai/")
        print("   Make sure to add Ollama to your PATH")
        return
    
    # Create Modelfile
    create_modelfile()
    
    # Create .env file
    create_env_file()
    
    # Create model
    if create_model():
        # Test model
        test_model()
        
        print("\n" + "=" * 60)
        print("🎉 Setup completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Start Ollama server: ollama serve")
        print("   2. Test the integration: python test_ollama_integration.py")
        print("   3. Run CodeRAG: python main.py")
        print("   4. Start UI: streamlit run app.py")
        print("\n🔧 Configuration:")
        print("   - Model name: llama-3.2-1b-instruct")
        print("   - Provider: Ollama")
        print("   - Embedding dimension: 4096")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
