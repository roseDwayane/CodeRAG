#!/usr/bin/env python3
"""
Fix Ollama configuration issues
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_current_config():
    """Check current configuration."""
    print("🔍 Checking current configuration...")
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_provider = os.getenv("MODEL_PROVIDER", "openai")
    
    print(f"📋 Current configuration:")
    print(f"   MODEL_PROVIDER: {model_provider}")
    print(f"   OLLAMA_BASE_URL: {ollama_url}")
    
    return ollama_url, model_provider

def test_ollama_connection(url):
    """Test connection to Ollama."""
    print(f"\n🔍 Testing connection to {url}...")
    
    try:
        response = requests.get(f"{url}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Connection successful!")
            models = response.json().get("models", [])
            if models:
                print(f"📋 Available models: {[m['name'] for m in models]}")
            else:
                print("⚠️  No models found")
            return True
        else:
            print(f"❌ Connection failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection refused to {url}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def fix_env_file():
    """Fix the .env file with correct Ollama configuration."""
    print("\n🔧 Fixing .env file...")
    
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
    
    print("✅ .env file updated with correct configuration")
    
    # Reload environment variables
    load_dotenv(override=True)

def check_ollama_status():
    """Check if Ollama is running."""
    print("\n🔍 Checking Ollama status...")
    
    try:
        import subprocess
        result = subprocess.run(
            'tasklist /FI "IMAGENAME eq ollama.exe"', 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if "ollama.exe" in result.stdout:
            print("✅ Ollama process is running")
            return True
        else:
            print("❌ Ollama process is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Ollama status: {e}")
        return False

def start_ollama():
    """Start Ollama if not running."""
    print("\n🔄 Starting Ollama...")
    
    try:
        import subprocess
        subprocess.Popen(
            'ollama serve', 
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ Ollama started in background")
        print("💡 Wait a few seconds for it to fully start")
        return True
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def main():
    """Main function to fix Ollama configuration."""
    print("🔧 Fixing Ollama Configuration")
    print("=" * 50)
    
    # Check current configuration
    current_url, current_provider = check_current_config()
    
    # Test current connection
    if not test_ollama_connection(current_url):
        print(f"\n⚠️  Current configuration is not working")
        
        # Check if Ollama is running
        if not check_ollama_status():
            print("\n🔄 Ollama is not running, starting it...")
            start_ollama()
        
        # Fix .env file
        fix_env_file()
        
        # Test with correct configuration
        print("\n🔄 Testing with corrected configuration...")
        if test_ollama_connection("http://localhost:11434"):
            print("\n🎉 Configuration fixed successfully!")
        else:
            print("\n❌ Still cannot connect to Ollama")
            print("💡 Please make sure Ollama is installed and running")
    else:
        print("\n✅ Configuration is working correctly!")
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("   1. Run: python test_ollama_integration.py")
    print("   2. Run: python setup_custom_model_windows.py")
    print("   3. Or test manually: ollama list")

if __name__ == "__main__":
    main()
