import os
import json
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from ai_config import get_ai_config

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI not available. Install with: pip install google-generativeai")

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("python-dotenv not available. Install with: pip install python-dotenv")


class LLMPortfolioAnalyzer:
    """
    Portfolio analyzer using local LLMs (via Ollama) or Google Gemini
    No OpenAI dependency required
    """
    
    def __init__(self, provider: str = "ollama", model: str = None):
        """
        Initialize the LLM analyzer
        
        Args:
            provider: "ollama" for local models or "gemini" for Google Gemini
            model: Model name (e.g., "llama2", "mistral" for Ollama or "gemini-pro" for Gemini)
        """
        # Use AI config manager for better configuration handling
        self.config_manager = get_ai_config()
        
        # Auto-select provider if not specified or unavailable
        if provider == "auto":
            provider = self.config_manager.get_preferred_provider()
            if not provider:
                raise ValueError("No AI providers available. Please configure Ollama or Gemini.")
        
        self.provider = provider.lower()
        
        # Get configuration for the provider
        self.config = self.config_manager.get_config(self.provider)
        if not self.config:
            raise ValueError(f"Configuration not found for provider: {self.provider}")
        
        self.model = model or self.config.model
        
        if self.provider == "gemini":
            self._setup_gemini()
        elif self.provider == "ollama":
            self._setup_ollama()
        else:
            raise ValueError("Provider must be 'ollama' or 'gemini'")
    
    def _setup_gemini(self):
        """Setup Google Gemini"""
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI not installed")
        
        api_key = self.config.api_key
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(self.model)
    
    def _setup_ollama(self):
        """Setup Ollama for local models"""
        self.ollama_host = self.config.host
        
        # Test Ollama connection
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConnectionError("Cannot connect to Ollama")
        except requests.exceptions.RequestException:
            raise ConnectionError(
                "Ollama not accessible. Make sure Ollama is running on "
                f"{self.ollama_host} and the model '{self.model}' is installed."
            )
    
    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama"""
        url = f"{self.ollama_host}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=data, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {e}")
    
    def _call_gemini(self, prompt: str) -> str:
        """Make API call to Google Gemini"""
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using the configured LLM"""
        if self.provider == "ollama":
            return self._call_ollama(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)
    
    def analyze_portfolio_performance(self, portfolio_data: pd.DataFrame) -> str:
        """Analyze portfolio performance using LLM"""
        
        # Prepare portfolio summary
        total_rows = portfolio_data[portfolio_data['Ticker'] == 'TOTAL']
        if total_rows.empty:
            return "No portfolio data available for analysis"
        
        latest_total = total_rows.iloc[-1]
        initial_value = 100  # Starting value
        current_value = latest_total['Total Equity']
        total_return = ((current_value - initial_value) / initial_value) * 100
        
        # Get individual stock performance
        stock_performance = []
        for ticker in portfolio_data['Ticker'].unique():
            if ticker != 'TOTAL':
                stock_data = portfolio_data[portfolio_data['Ticker'] == ticker]
                if not stock_data.empty:
                    latest_stock = stock_data.iloc[-1]
                    stock_performance.append({
                        'ticker': ticker,
                        'current_price': latest_stock.get('Current Price', 'N/A'),
                        'pnl': latest_stock.get('PnL', 'N/A'),
                        'action': latest_stock.get('Action', 'N/A')
                    })
        
        prompt = f"""
        As a professional portfolio analyst, analyze the following micro-cap portfolio performance:
        
        Portfolio Summary:
        - Initial Investment: $100
        - Current Value: ${current_value:.2f}
        - Total Return: {total_return:.2f}%
        - Cash Balance: ${latest_total.get('Cash Balance', 0):.2f}
        
        Individual Stock Performance:
        {json.dumps(stock_performance, indent=2)}
        
        Please provide:
        1. Overall portfolio assessment
        2. Risk analysis
        3. Recommendations for position management
        4. Market outlook considerations
        5. Potential catalysts to watch
        
        Keep the analysis concise but insightful, focusing on actionable insights for micro-cap investing.
        """
        
        return self.generate_response(prompt)
    
    def research_stock(self, ticker: str, current_price: float = None) -> str:
        """Research a specific stock using LLM knowledge"""
        
        prompt = f"""
        As a professional equity research analyst, provide a comprehensive analysis of {ticker}:
        
        {"Current Price: $" + str(current_price) if current_price else ""}
        
        Please analyze:
        1. Business model and competitive position
        2. Recent financial performance and key metrics
        3. Upcoming catalysts and events to watch
        4. Risk factors and potential headwinds
        5. Valuation assessment
        6. Investment thesis (bull/bear cases)
        
        Focus on micro-cap specific considerations such as:
        - Liquidity concerns
        - Institutional ownership
        - Regulatory risks
        - Growth potential vs. execution risk
        
        Provide a balanced, data-driven analysis suitable for investment decision-making.
        """
        
        return self.generate_response(prompt)
    
    def generate_trading_strategy(self, portfolio_data: pd.DataFrame, market_conditions: str = "") -> str:
        """Generate trading strategy recommendations"""
        
        prompt = f"""
        As a professional portfolio strategist specializing in micro-cap stocks, develop a trading strategy based on:
        
        Current Portfolio Status:
        {self._format_portfolio_for_prompt(portfolio_data)}
        
        Market Conditions: {market_conditions}
        
        Provide strategic recommendations for:
        1. Position sizing and risk management
        2. Entry/exit criteria for current holdings
        3. Potential new opportunities in micro-cap space
        4. Stop-loss and profit-taking levels
        5. Portfolio rebalancing considerations
        
        Consider the unique characteristics of micro-cap investing:
        - Higher volatility and risk
        - Limited liquidity
        - Greater potential for asymmetric returns
        - Importance of catalyst-driven events
        
        Provide specific, actionable recommendations with clear rationale.
        """
        
        return self.generate_response(prompt)
    
    def _format_portfolio_for_prompt(self, portfolio_data: pd.DataFrame) -> str:
        """Format portfolio data for LLM prompt"""
        if portfolio_data.empty:
            return "No portfolio data available"
        
        latest_data = portfolio_data.groupby('Ticker').last().reset_index()
        
        formatted = []
        for _, row in latest_data.iterrows():
            if row['Ticker'] != 'TOTAL':
                formatted.append(f"- {row['Ticker']}: {row.get('Shares', 'N/A')} shares @ ${row.get('Current Price', 'N/A')}, P&L: ${row.get('PnL', 'N/A')}")
        
        return "\n".join(formatted) if formatted else "No individual stock positions"


def main():
    """Example usage of the LLM Portfolio Analyzer"""
    
    # Auto-select best available provider
    try:
        analyzer = LLMPortfolioAnalyzer(provider="auto")
        print(f"✅ AI analyzer initialized successfully ({analyzer.provider})")
    except Exception as e:
        print(f"❌ AI setup failed: {e}")
        print("Please ensure either Ollama is running or GOOGLE_API_KEY is set")
        return
    
    # Load portfolio data
    try:
        portfolio_df = pd.read_csv("chatgpt_portfolio_update.csv")
        
        # Generate portfolio analysis
        print("\n" + "="*50)
        print("PORTFOLIO ANALYSIS")
        print("="*50)
        analysis = analyzer.analyze_portfolio_performance(portfolio_df)
        print(analysis)
        
        # Research a specific stock
        print("\n" + "="*50)
        print("STOCK RESEARCH: ABEO")
        print("="*50)
        research = analyzer.research_stock("ABEO", 6.80)
        print(research)
        
    except FileNotFoundError:
        print("Portfolio CSV file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()