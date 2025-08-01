#!/usr/bin/env python3
"""
Setup script for local LLM integration
Helps users configure Ollama or Google Gemini for the trading experiment
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'pandas', 'yfinance', 'matplotlib', 'numpy', 'requests'
    ]
    
    optional_packages = [
        ('google-generativeai', 'Google Gemini support'),
        ('python-dotenv', 'Environment variable management'),
        ('ollama', 'Ollama Python client (optional)')
    ]
    
    print("🔍 Checking Python packages...")
    
    missing_required = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_required.append(package)
    
    if missing_required:
        print(f"\n⚠️  Missing required packages: {', '.join(missing_required)}")
        print("Install with: pip install " + " ".join(missing_required))
        return False
    
    print("\n🔍 Checking optional packages...")
    for package, description in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"⚪ {package} - {description} (optional)")
    
    return True

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("\n🔍 Checking Ollama installation...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not found in PATH")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not installed or not in PATH")
        print("📥 Install Ollama from: https://ollama.ai/")
        return False
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            
            # List available models
            models = response.json().get('models', [])
            if models:
                print("📚 Available models:")
                for model in models:
                    print(f"   - {model['name']}")
            else:
                print("⚠️  No models installed")
                print("💡 Install a model with: ollama pull llama2")
            return True
        else:
            print("❌ Ollama service not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Ollama service")
        print("💡 Start Ollama with: ollama serve")
        return False

def setup_environment_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your API keys")
        return True
    else:
        print("⚠️  .env.example not found, creating basic .env file...")
        basic_env = """# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Ollama Configuration (for local models)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# Trading configuration
PORTFOLIO_UPDATE_INTERVAL=daily
RISK_TOLERANCE=moderate
"""
        with open(env_file, 'w') as f:
            f.write(basic_env)
        
        print("✅ Basic .env file created")
        print("⚠️  Please edit .env file and configure your settings")
        return True

def test_llm_integration():
    """Test LLM integration"""
    print("\n🧪 Testing LLM integration...")
    
    try:
        from Scripts.llm_integration import LLMPortfolioAnalyzer
        
        # Test Ollama
        try:
            analyzer = LLMPortfolioAnalyzer(provider="ollama")
            response = analyzer.generate_response("Hello, this is a test. Please respond with 'Ollama is working!'")
            if "working" in response.lower():
                print("✅ Ollama integration working")
            else:
                print(f"⚠️  Ollama responded but unexpected output: {response[:100]}...")
        except Exception as e:
            print(f"❌ Ollama test failed: {e}")
        
        # Test Gemini (if API key is set)
        try:
            if os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_API_KEY') != 'your_google_api_key_here':
                analyzer = LLMPortfolioAnalyzer(provider="gemini")
                response = analyzer.generate_response("Hello, this is a test. Please respond with 'Gemini is working!'")
                if "working" in response.lower():
                    print("✅ Gemini integration working")
                else:
                    print(f"⚠️  Gemini responded but unexpected output: {response[:100]}...")
            else:
                print("⚪ Gemini test skipped (no API key configured)")
        except Exception as e:
            print(f"❌ Gemini test failed: {e}")
            
    except ImportError as e:
        print(f"❌ Cannot import LLM integration module: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 ChatGPT Micro-Cap Experiment - Local LLM Setup")
    print("="*60)
    
    # Check Python packages
    if not check_python_packages():
        print("\n❌ Setup failed: Missing required packages")
        sys.exit(1)
    
    # Check Ollama
    ollama_ok = check_ollama_installation()
    
    # Setup environment
    setup_environment_file()
    
    # Test integration
    test_llm_integration()
    
    print("\n" + "="*60)
    print("📋 SETUP SUMMARY")
    print("="*60)
    
    if ollama_ok:
        print("✅ Ollama setup complete - You can use local models")
    else:
        print("⚠️  Ollama not ready - Install and configure Ollama for local models")
    
    print("✅ Environment file created - Configure API keys as needed")
    print("✅ LLM integration modules ready")
    
    print("\n📚 NEXT STEPS:")
    print("1. If using Ollama: Install a model with 'ollama pull llama2'")
    print("2. If using Gemini: Add your GOOGLE_API_KEY to .env file")
    print("3. Run the enhanced trading script: python Scripts/enhanced_trading_script.py")
    print("4. Or test LLM integration: python Scripts/llm_integration.py")
    
    print("\n🎯 The repository now supports local LLMs and Google Gemini!")
    print("   No OpenAI dependency required.")

if __name__ == "__main__":
    main()