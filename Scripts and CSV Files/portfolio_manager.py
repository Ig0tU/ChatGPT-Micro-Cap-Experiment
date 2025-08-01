"""
Comprehensive Portfolio Management System with AI Integration
Centralizes all portfolio operations with built-in AI analysis
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Tuple
from llm_integration import LLMPortfolioAnalyzer
import warnings
warnings.filterwarnings('ignore')


class AIPortfolioManager:
    """
    Advanced portfolio manager with integrated AI analysis
    Handles all trading operations, risk management, and AI-powered insights
    """
    
    def __init__(self, initial_cash: float = 100.0, use_ai: bool = True):
        self.initial_cash = initial_cash
        self.use_ai = use_ai
        self.today = datetime.today().strftime('%Y-%m-%d')
        
        # Initialize AI analyzer
        if self.use_ai:
            try:
                self.ai_analyzer = LLMPortfolioAnalyzer(provider="ollama")
                print("✅ AI Analyzer initialized (Ollama)")
            except:
                try:
                    self.ai_analyzer = LLMPortfolioAnalyzer(provider="gemini")
                    print("✅ AI Analyzer initialized (Gemini)")
                except:
                    print("⚠️  AI Analyzer unavailable - continuing without AI features")
                    self.use_ai = False
    
    def load_portfolio(self, portfolio_file: str = "Scripts and CSV Files/chatgpt_portfolio_update.csv") -> pd.DataFrame:
        """Load current portfolio from CSV"""
        try:
            return pd.read_csv(portfolio_file)
        except FileNotFoundError:
            print(f"Portfolio file {portfolio_file} not found. Creating new portfolio.")
            return pd.DataFrame()
    
    def get_current_positions(self, portfolio_df: pd.DataFrame) -> Dict:
        """Extract current positions from portfolio DataFrame"""
        if portfolio_df.empty:
            return {"positions": [], "cash": self.initial_cash, "total_equity": self.initial_cash}
        
        # Get latest data for each ticker
        latest_data = portfolio_df.groupby('Ticker').last().reset_index()
        
        positions = []
        cash = 0
        total_equity = 0
        
        for _, row in latest_data.iterrows():
            if row['Ticker'] == 'TOTAL':
                cash = row.get('Cash Balance', 0)
                total_equity = row.get('Total Equity', 0)
            else:
                positions.append({
                    'ticker': row['Ticker'],
                    'shares': row.get('Shares', 0),
                    'cost_basis': row.get('Cost Basis', 0),
                    'current_price': row.get('Current Price', 0),
                    'stop_loss': row.get('Stop Loss', 0),
                    'pnl': row.get('PnL', 0)
                })
        
        return {"positions": positions, "cash": cash, "total_equity": total_equity}
    
    def fetch_market_data(self, tickers: List[str], period: str = "2d") -> Dict:
        """Fetch current market data for given tickers"""
        market_data = {}
        
        for ticker in tickers:
            try:
                data = yf.download(ticker, period=period, progress=False)
                if not data.empty:
                    current_price = float(data['Close'].iloc[-1])
                    prev_price = float(data['Close'].iloc[-2]) if len(data) > 1 else current_price
                    volume = float(data['Volume'].iloc[-1])
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    market_data[ticker] = {
                        'current_price': current_price,
                        'previous_price': prev_price,
                        'volume': volume,
                        'change_percent': change_pct
                    }
                else:
                    print(f"⚠️  No data available for {ticker}")
            except Exception as e:
                print(f"❌ Error fetching data for {ticker}: {e}")
        
        return market_data
    
    def analyze_portfolio_with_ai(self, portfolio_df: pd.DataFrame) -> Optional[str]:
        """Generate AI analysis of current portfolio"""
        if not self.use_ai:
            return None
        
        try:
            analysis = self.ai_analyzer.analyze_portfolio_performance(portfolio_df)
            
            # Save analysis
            with open(f"Scripts and CSV Files/ai_daily_analysis_{self.today}.txt", "w") as f:
                f.write(f"AI Daily Portfolio Analysis - {self.today}\n")
                f.write("="*50 + "\n")
                f.write(analysis)
            
            return analysis
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return None
    
    def research_stock_with_ai(self, ticker: str, current_price: float = None) -> Optional[str]:
        """Get AI-powered research on a specific stock"""
        if not self.use_ai:
            return None
        
        try:
            research = self.ai_analyzer.research_stock(ticker, current_price)
            
            # Save research
            with open(f"Scripts and CSV Files/ai_research_{ticker}_{self.today}.txt", "w") as f:
                f.write(f"AI Stock Research: {ticker} - {self.today}\n")
                f.write("="*50 + "\n")
                f.write(research)
            
            return research
        except Exception as e:
            print(f"AI research failed for {ticker}: {e}")
            return None
    
    def generate_trading_strategy(self, portfolio_df: pd.DataFrame, market_conditions: str = "") -> Optional[str]:
        """Generate AI-powered trading strategy"""
        if not self.use_ai:
            return None
        
        try:
            strategy = self.ai_analyzer.generate_trading_strategy(portfolio_df, market_conditions)
            
            # Save strategy
            with open(f"Scripts and CSV Files/ai_strategy_{self.today}.txt", "w") as f:
                f.write(f"AI Trading Strategy - {self.today}\n")
                f.write("="*50 + "\n")
                f.write(strategy)
            
            return strategy
        except Exception as e:
            print(f"AI strategy generation failed: {e}")
            return None
    
    def check_stop_losses(self, positions: List[Dict], market_data: Dict) -> List[Dict]:
        """Check for stop loss triggers and return sell recommendations"""
        stop_loss_triggers = []
        
        for position in positions:
            ticker = position['ticker']
            if ticker in market_data:
                current_price = market_data[ticker]['current_price']
                stop_loss = position['stop_loss']
                
                if current_price <= stop_loss:
                    stop_loss_triggers.append({
                        'ticker': ticker,
                        'current_price': current_price,
                        'stop_loss': stop_loss,
                        'shares': position['shares'],
                        'reason': 'Stop Loss Triggered'
                    })
        
        return stop_loss_triggers
    
    def calculate_portfolio_metrics(self, portfolio_df: pd.DataFrame) -> Dict:
        """Calculate comprehensive portfolio performance metrics"""
        if portfolio_df.empty:
            return {}
        
        # Get total equity over time
        totals = portfolio_df[portfolio_df['Ticker'] == 'TOTAL'].copy()
        if totals.empty:
            return {}
        
        totals['Date'] = pd.to_datetime(totals['Date'])
        totals = totals.sort_values('Date')
        
        equity_series = totals['Total Equity'].astype(float)
        
        # Calculate returns
        daily_returns = equity_series.pct_change().dropna()
        total_return = (equity_series.iloc[-1] - self.initial_cash) / self.initial_cash
        
        # Risk metrics
        volatility = daily_returns.std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (total_return * 252 - 0.045) / (volatility) if volatility > 0 else 0
        
        # Drawdown
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return {
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown * 100,
            'current_equity': float(equity_series.iloc[-1]),
            'trading_days': len(equity_series)
        }
    
    def generate_daily_report(self, portfolio_df: pd.DataFrame) -> str:
        """Generate comprehensive daily portfolio report"""
        current_positions = self.get_current_positions(portfolio_df)
        
        # Get market data for all positions
        tickers = [pos['ticker'] for pos in current_positions['positions']]
        tickers.extend(['^RUT', 'IWO', 'XBI'])  # Add benchmark tickers
        market_data = self.fetch_market_data(tickers)
        
        # Check stop losses
        stop_losses = self.check_stop_losses(current_positions['positions'], market_data)
        
        # Calculate metrics
        metrics = self.calculate_portfolio_metrics(portfolio_df)
        
        # Build report
        report = f"""
🚀 DAILY PORTFOLIO REPORT - {self.today}
{'='*60}

💰 PORTFOLIO SUMMARY:
   Current Equity: ${current_positions['total_equity']:.2f}
   Cash Balance: ${current_positions['cash']:.2f}
   Total Return: {metrics.get('total_return_pct', 0):.2f}%
   Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}

📊 CURRENT POSITIONS:
"""
        
        for position in current_positions['positions']:
            ticker = position['ticker']
            if ticker in market_data:
                data = market_data[ticker]
                report += f"""   {ticker}: {position['shares']} shares @ ${data['current_price']:.2f} 
      Change: {data['change_percent']:+.2f}% | P&L: ${position['pnl']:.2f}
"""
        
        if stop_losses:
            report += f"\n🚨 STOP LOSS ALERTS:\n"
            for sl in stop_losses:
                report += f"   {sl['ticker']}: ${sl['current_price']:.2f} ≤ ${sl['stop_loss']:.2f}\n"
        
        report += f"\n📈 BENCHMARK COMPARISON:\n"
        for ticker in ['^RUT', 'IWO', 'XBI']:
            if ticker in market_data:
                data = market_data[ticker]
                report += f"   {ticker}: ${data['current_price']:.2f} ({data['change_percent']:+.2f}%)\n"
        
        return report
    
    def run_daily_analysis(self, portfolio_file: str = "Scripts and CSV Files/chatgpt_portfolio_update.csv"):
        """Run complete daily portfolio analysis with AI integration"""
        print("🚀 AI-POWERED PORTFOLIO ANALYSIS")
        print("="*60)
        
        # Load portfolio
        portfolio_df = self.load_portfolio(portfolio_file)
        
        # Generate daily report
        daily_report = self.generate_daily_report(portfolio_df)
        print(daily_report)
        
        # AI Analysis
        if self.use_ai:
            print("\n🤖 AI PORTFOLIO ANALYSIS:")
            print("-" * 40)
            ai_analysis = self.analyze_portfolio_with_ai(portfolio_df)
            if ai_analysis:
                print(ai_analysis)
            
            print("\n📈 AI TRADING STRATEGY:")
            print("-" * 40)
            strategy = self.generate_trading_strategy(portfolio_df, "Current micro-cap market conditions")
            if strategy:
                print(strategy)
        
        # Save complete report
        complete_report = daily_report + "\n\n" + (ai_analysis or "") + "\n\n" + (strategy or "")
        with open(f"Scripts and CSV Files/daily_report_{self.today}.txt", "w") as f:
            f.write(complete_report)
        
        print(f"\n✅ Complete analysis saved to daily_report_{self.today}.txt")


def main():
    """Main execution function"""
    # Initialize AI Portfolio Manager
    manager = AIPortfolioManager(initial_cash=100.0, use_ai=True)
    
    # Run daily analysis
    manager.run_daily_analysis()


if __name__ == "__main__":
    main()