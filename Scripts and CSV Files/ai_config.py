"""
AI Configuration and Management System
Centralized configuration for all AI/LLM integrations
"""

import os
from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AIConfig:
    """Configuration class for AI providers"""
    provider: str
    model: str
    api_key: Optional[str] = None
    host: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60

class AIConfigManager:
    """Manages AI configuration across the application"""
    
    def __init__(self):
        self.load_environment()
        self.configs = self._initialize_configs()
    
    def load_environment(self):
        """Load environment variables from .env file"""
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    
    def _initialize_configs(self) -> Dict[str, AIConfig]:
        """Initialize AI provider configurations"""
        return {
            'ollama': AIConfig(
                provider='ollama',
                model=os.getenv('OLLAMA_MODEL', 'llama2'),
                host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
                temperature=0.7,
                max_tokens=2000
            ),
            'gemini': AIConfig(
                provider='gemini',
                model=os.getenv('GEMINI_MODEL', 'gemini-pro'),
                api_key=os.getenv('GOOGLE_API_KEY'),
                temperature=0.7,
                max_tokens=2000
            )
        }
    
    def get_config(self, provider: str) -> Optional[AIConfig]:
        """Get configuration for specific AI provider"""
        return self.configs.get(provider.lower())
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        available = []
        
        # Check Ollama
        try:
            import requests
            response = requests.get(f"{self.configs['ollama'].host}/api/tags", timeout=5)
            if response.status_code == 200:
                available.append('ollama')
        except:
            pass
        
        # Check Gemini
        if self.configs['gemini'].api_key and self.configs['gemini'].api_key != 'your_google_api_key_here':
            try:
                import google.generativeai as genai
                available.append('gemini')
            except ImportError:
                pass
        
        return available
    
    def get_preferred_provider(self) -> Optional[str]:
        """Get the preferred AI provider based on availability"""
        available = self.get_available_providers()
        
        # Preference order: ollama (local) -> gemini (cloud)
        for provider in ['ollama', 'gemini']:
            if provider in available:
                return provider
        
        return None
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate AI setup and return status"""
        status = {}
        
        # Check Ollama
        try:
            import requests
            response = requests.get(f"{self.configs['ollama'].host}/api/tags", timeout=5)
            status['ollama'] = response.status_code == 200
        except:
            status['ollama'] = False
        
        # Check Gemini
        try:
            import google.generativeai as genai
            api_key = self.configs['gemini'].api_key
            status['gemini'] = bool(api_key and api_key != 'your_google_api_key_here')
        except ImportError:
            status['gemini'] = False
        
        return status

# Global configuration instance
ai_config = AIConfigManager()

def get_ai_config() -> AIConfigManager:
    """Get global AI configuration manager"""
    return ai_config