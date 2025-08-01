import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from llm_integration import LLMPortfolioAnalyzer

# === Load and prepare ChatGPT portfolio ===
chatgpt_df = pd.read_csv("Scripts and CSV files/chatgpt_portfolio_update.csv")
chatgpt_totals = chatgpt_df[chatgpt_df['Ticker'] == 'TOTAL'].copy()
chatgpt_totals['Date'] = pd.to_datetime(chatgpt_totals['Date'])

# Add fake baseline row for June 27 (weekend)
baseline_date = pd.Timestamp("2025-06-27")
baseline_equity = 100  # Starting value
baseline_chatgpt_row = pd.DataFrame({
    "Date": [baseline_date],
    "Total Equity": [baseline_equity]   
    })
chatgpt_totals = pd.concat([baseline_chatgpt_row, chatgpt_totals], ignore_index=True).sort_values("Date")

# === Download and prepare Russell 2000 ===
start_date = baseline_date
end_date = chatgpt_totals['Date'].max()

sp500 = yf.download("^SPX", start=start_date, end=end_date + pd.Timedelta(days=1), progress=False)
sp500 = sp500.reset_index()

# Fix columns if downloaded with MultiIndex
if isinstance(sp500.columns, pd.MultiIndex):
    sp500.columns = sp500.columns.get_level_values(0)
# Real close price on June 27 (pulled from YF)
sp500_27_price = 6173.07

# Normalize to $100 baseline
sp500_scaling_factor = 100 / sp500_27_price
# create adjusted close col



sp500["SPX Value ($100 Invested)"] = sp500["Close"] * sp500_scaling_factor

# === Plot ===
plt.figure(figsize=(10, 6))
plt.style.use("seaborn-v0_8-whitegrid")
plt.plot(chatgpt_totals['Date'], chatgpt_totals["Total Equity"], label="ChatGPT ($100 Invested)", marker="o", color="blue", linewidth=2)
plt.plot(sp500['Date'], sp500["SPX Value ($100 Invested)"], label="S&P 500 ($100 Invested)", marker="o", color="orange", linestyle='--', linewidth=2)

final_date = chatgpt_totals['Date'].iloc[-1]
final_chatgpt = float(chatgpt_totals["Total Equity"].iloc[-1])
final_spx = sp500["SPX Value ($100 Invested)"].iloc[-1]

plt.text(final_date, final_chatgpt + 0.3, f"+{final_chatgpt - 100:.1f}%", color="blue", fontsize=9)
plt.text(final_date, final_spx + 0.9, f"+{final_spx - 100:.1f}%", color="orange", fontsize=9)

drawdown_date = pd.Timestamp("2025-07-11")
drawdown_value = 102.46
plt.text(drawdown_date + pd.Timedelta(days=0.5), drawdown_value - 0.5, "-7% Drawdown", color="red", fontsize=9)
plt.title("ChatGPT's Micro Cap Portfolio vs. S&P 500")
plt.xlabel("Date")
plt.ylabel("Value of $100 Investment")
plt.xticks(rotation=15)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === AI Performance Analysis ===
try:
    print("\n" + "="*60)
    print("🤖 AI PERFORMANCE ANALYSIS")
    print("="*60)
    
    analyzer = LLMPortfolioAnalyzer(provider="ollama")
    
    # Calculate key metrics for AI analysis
    final_chatgpt = float(chatgpt_totals["Total Equity"].iloc[-1])
    total_return_pct = ((final_chatgpt - 100) / 100) * 100
    spx_return_pct = ((final_spx - 100) / 100) * 100
    outperformance = total_return_pct - spx_return_pct
    
    performance_prompt = f"""
    Analyze this micro-cap portfolio performance:
    
    Portfolio Return: {total_return_pct:.2f}%
    S&P 500 Return: {spx_return_pct:.2f}%
    Outperformance: {outperformance:+.2f}%
    
    Trading Period: {len(chatgpt_totals)} days
    Final Portfolio Value: ${final_chatgpt:.2f}
    
    Provide insights on:
    1. Risk-adjusted performance assessment
    2. Key factors driving outperformance/underperformance
    3. Portfolio construction effectiveness
    4. Recommendations for improvement
    """
    
    analysis = analyzer.generate_response(performance_prompt)
    print(analysis)
    
    # Save analysis
    with open("Scripts and CSV Files/ai_performance_analysis.txt", "w") as f:
        f.write(f"AI Performance Analysis - {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
        f.write("="*50 + "\n")
        f.write(analysis)
    
except Exception as e:
    print(f"AI analysis unavailable: {e}")
    print("Continuing with standard visualization...")