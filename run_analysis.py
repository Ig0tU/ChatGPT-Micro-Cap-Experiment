#!/usr/bin/env python3
"""
Main entry point for running AI-powered portfolio analysis
Provides a simple interface to run different types of analysis
"""

import sys
import argparse
from pathlib import Path

# Add Scripts directory to path
sys.path.append(str(Path("Scripts and CSV Files")))

from portfolio_manager import AIPortfolioManager
from llm_integration import LLMPortfolioAnalyzer
from ai_config import get_ai_config
import pandas as pd


def run_daily_analysis():
    """Run daily portfolio analysis"""
    print("🚀 Running Daily Portfolio Analysis...")
    manager = AIPortfolioManager(use_ai=True)
    manager.run_daily_analysis()


def run_performance_analysis():
    """Run comprehensive performance analysis"""
    print("📊 Running Performance Analysis...")
    
    try:
        # Load portfolio data
        portfolio_df = pd.read_csv("Scripts and CSV Files/chatgpt_portfolio_update.csv")
        
        # Initialize AI analyzer
        analyzer = LLMPortfolioAnalyzer(provider="auto")
        
        print("\n" + "="*60)
        print("🤖 AI PERFORMANCE ANALYSIS")
        print("="*60)
        
        analysis = analyzer.analyze_portfolio_performance(portfolio_df)
        print(analysis)
        
        # Save analysis
        with open("Scripts and CSV Files/performance_analysis.txt", "w") as f:
            f.write(f"AI Performance Analysis\n")
            f.write("="*50 + "\n")
            f.write(analysis)
        
        print(f"\n✅ Analysis saved to performance_analysis.txt")
        
    except Exception as e:
        print(f"❌ Performance analysis failed: {e}")


def run_stock_research(ticker: str):
    """Run AI research on a specific stock"""
    print(f"🔍 Running Stock Research for {ticker}...")
    
    try:
        analyzer = LLMPortfolioAnalyzer(provider="auto")
        research = analyzer.research_stock(ticker)
        
        print(f"\n📋 RESEARCH: {ticker}")
        print("="*40)
        print(research)
        
        # Save research
        with open(f"Scripts and CSV Files/research_{ticker}.txt", "w") as f:
            f.write(f"AI Stock Research: {ticker}\n")
            f.write("="*50 + "\n")
            f.write(research)
        
        print(f"\n✅ Research saved to research_{ticker}.txt")
        
    except Exception as e:
        print(f"❌ Stock research failed: {e}")


def check_ai_status():
    """Check AI configuration and availability"""
    print("🔍 Checking AI Configuration...")
    
    config_manager = get_ai_config()
    status = config_manager.validate_setup()
    available = config_manager.get_available_providers()
    preferred = config_manager.get_preferred_provider()
    
    print("\n📋 AI PROVIDER STATUS:")
    print("-" * 30)
    
    for provider, is_available in status.items():
        status_icon = "✅" if is_available else "❌"
        print(f"{status_icon} {provider.upper()}: {'Available' if is_available else 'Not Available'}")
    
    if available:
        print(f"\n🎯 Available Providers: {', '.join(available)}")
        print(f"🏆 Preferred Provider: {preferred}")
    else:
        print("\n⚠️  No AI providers available!")
        print("Please configure Ollama or Google Gemini.")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Portfolio Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_analysis.py daily          # Run daily analysis
  python run_analysis.py performance    # Run performance analysis  
  python run_analysis.py research ABEO  # Research specific stock
  python run_analysis.py status         # Check AI configuration
        """
    )
    
    parser.add_argument(
        'command',
        choices=['daily', 'performance', 'research', 'status'],
        help='Analysis command to run'
    )
    
    parser.add_argument(
        'ticker',
        nargs='?',
        help='Stock ticker for research command'
    )
    
    args = parser.parse_args()
    
    print("🤖 AI-Powered Portfolio Analysis Tool")
    print("="*50)
    
    if args.command == 'daily':
        run_daily_analysis()
    elif args.command == 'performance':
        run_performance_analysis()
    elif args.command == 'research':
        if not args.ticker:
            print("❌ Please provide a ticker symbol for research")
            sys.exit(1)
        run_stock_research(args.ticker.upper())
    elif args.command == 'status':
        check_ai_status()


if __name__ == "__main__":
    main()