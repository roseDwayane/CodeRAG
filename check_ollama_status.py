#!/usr/bin/env python3
"""
Check Ollama status and handle port conflicts
"""

import subprocess
import requests
import os
import sys

def check_ollama_process():
    """Check if Ollama process is running."""
    try:
        # Check if ollama process is running
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
        print(f"❌ Error checking Ollama process: {e}")
        return False

def check_ollama_api():
    """Check if Ollama API is responding."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama API is responding")
            models = response.json().get("models", [])
            if models:
                print(f"📋 Available models: {[m['name'] for m in models]}")
            else:
                print("⚠️  No models found")
            return True
        else:
            print(f"❌ Ollama API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama API (Connection refused)")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama API: {e}")
        return False

def check_port_usage():
    """Check what's using port 11434."""
    try:
        result = subprocess.run(
            'netstat -ano | findstr :11434', 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.stdout.strip():
            print("🔍 Port 11434 is in use:")
            print(result.stdout)
            return True
        else:
            print("✅ Port 11434 is not in use")
            return False
    except Exception as e:
        print(f"❌ Error checking port usage: {e}")
        return False

def stop_ollama():
    """Stop Ollama process."""
    try:
        print("🔄 Stopping Ollama process...")
        result = subprocess.run(
            'taskkill /F /IM ollama.exe', 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("✅ Ollama process stopped successfully")
            return True
        else:
            print(f"❌ Failed to stop Ollama: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error stopping Ollama: {e}")
        return False

def start_ollama():
    """Start Ollama in background."""
    try:
        print("🔄 Starting Ollama...")
        # Start Ollama in background
        subprocess.Popen(
            'ollama serve', 
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print("✅ Ollama started in background")
        print("💡 You can now run your setup script")
        return True
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def main():
    """Main function to check and fix Ollama status."""
    print("🔍 Checking Ollama Status")
    print("=" * 40)
    
    # Check if Ollama process is running
    process_running = check_ollama_process()
    
    # Check if API is responding
    api_responding = check_ollama_api()
    
    # Check port usage
    port_in_use = check_port_usage()
    
    print("\n" + "=" * 40)
    
    if process_running and api_responding:
        print("🎉 Ollama is running correctly!")
        print("💡 You can proceed with your setup")
        return
    
    elif process_running and not api_responding:
        print("⚠️  Ollama process is running but API is not responding")
        print("🔄 Restarting Ollama...")
        stop_ollama()
        start_ollama()
    
    elif port_in_use and not process_running:
        print("⚠️  Port 11434 is in use by another process")
        print("🔍 Check what's using the port above")
        print("💡 You may need to stop the other process manually")
    
    else:
        print("❌ Ollama is not running")
        print("🔄 Starting Ollama...")
        start_ollama()
    
    print("\n" + "=" * 40)
    print("📝 Next steps:")
    print("   1. Wait a few seconds for Ollama to start")
    print("   2. Run: python setup_custom_model_windows.py")
    print("   3. Or test manually: ollama list")

if __name__ == "__main__":
    main()
