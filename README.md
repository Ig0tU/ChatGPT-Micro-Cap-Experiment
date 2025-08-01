# ChatGPT Micro-Cap Experiment
Welcome to the repo behind my 6-month live trading experiment where AI models manage a real-money micro-cap portfolio.

**🚀 Fully integrated Local LLMs and Google Gemini - Complete AI-powered analysis throughout!**

# The Concept
Every day, I kept seeing the same ad about having some A.I. pick undervalued stocks. It was obvious it was trying to get me to subscribe to some garbage, so I just rolled my eyes. 
Then I started wondering, "How well would that actually work?".

So, starting with just $100, I wanted to answer a simple but powerful question:

**Can powerful large language models actually generate alpha (or at least make smart trading decisions) using real-time data?**

## 🤖 AI Model Support

This experiment is **fully integrated** with multiple AI providers throughout the entire application:
- **Local LLMs via Ollama** (Llama 2, Mistral, CodeLlama, etc.) - **Recommended for privacy**
- **Google Gemini** - High-quality cloud-based model
- **No OpenAI dependency** - Run completely independently
- **Auto-provider selection** - Automatically uses the best available AI model
- **Comprehensive integration** - AI analysis in every component

### Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup local LLM or Gemini:**
   ```bash
   python setup_local_llm.py
   ```

3. **Configure your preferred AI model:**
   - For **Ollama**: Install Ollama and pull a model (`ollama pull llama2`)
   - For **Gemini**: Add your `GOOGLE_API_KEY` to `.env` file

4. **Run enhanced analysis:**
   ```bash
   python run_analysis.py daily
   ```

### 🎯 AI Integration Features

The AI is now **fully integrated** throughout the application:

- **📊 Daily Portfolio Analysis** - AI evaluates performance, risk, and opportunities
- **🔍 Stock Research** - Deep AI-powered research on individual stocks  
- **📈 Trading Strategy** - AI generates actionable trading recommendations
- **⚠️ Risk Management** - AI monitors stop-losses and risk factors
- **📋 Performance Reports** - Comprehensive AI analysis of returns vs benchmarks
- **🚨 Alert System** - AI analyzes significant price movements
- **📝 Automated Documentation** - All AI insights saved to files

### 🚀 Usage Examples

```bash
# Run complete daily analysis with AI insights
python run_analysis.py daily

# Get AI performance analysis
python run_analysis.py performance

# Research a specific stock with AI
python run_analysis.py research ABEO

# Check AI configuration status
python run_analysis.py status

# Use the enhanced trading script
python "Scripts and CSV Files/enhanced_trading_script.py"

# Generate performance graphs with AI analysis
python "Scripts and CSV Files/Generate_Graph.py"
```

## Each trading day:

- I provide it trading data on the stocks in it's portfolio.

- Strict stop-loss rules apply.

- Everyweek I allow it to use deep research to reevaluate it's account.

- I track and publish performance data weekly on my blog. [SubStack Link](https://substack.com/@nathanbsmith?utm_source=edit-profile-page)

  ## Research & Documentation

- [Research Index](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/blob/main/Experiment%20Details/Deep%20Research%20Index.md)

- [Q&A](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/blob/main/Experiment%20Details/Q%26A.md)

- [Prompts](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/blob/main/Experiment%20Details/Prompts.md)

- [Using Scripts](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/blob/main/Using%20Scripts.md)

-  [Markdown Research Summaries (MD)](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/tree/main/Weekly%20Deep%20Research%20(MD))
- [Weekly Deep Research Reports (PDF)](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment/tree/main/Weekly%20Deep%20Research%20(PDF))
  
# Performance Example (6/30 – 7/25)

---

![Week 4 Performance](%286-30%20-%207-25%29%20Results.png)

---
- Currently stomping on the Russell 2K.

# Features of This Repo
Live trading scripts — Used to evaluate prices and update holdings daily

LLM-powered decision engine — ChatGPT picks the trades

Performance tracking — CSVs with daily PnL, total equity, and trade history

Visualization tools — Matplotlib graphs comparing ChatGPT vs Index

Logs & trade data — Auto-saved logs for transparency

# Why This Matters
AI is being hyped across every industry, but can it really manage money without guidance?

This project is an attempt to find out, with transparency, data, and a real budget.

# Tech Stack
**Core:**
- Python 3.8+
- Pandas + yFinance for data & logic
- Matplotlib for visualizations

**AI Integration:**
- **Ollama** for local LLM models (Llama 2, Mistral, etc.)
- **Google Gemini** for cloud-based AI analysis
- **No OpenAI dependency** - completely independent

**Features:**
- 🏠 **Local AI Models** - Run everything on your own hardware
- 🔒 **Privacy-focused** - No data sent to OpenAI
- 📊 **Complete AI Integration** - AI analysis in every component
- 🎯 **Multi-model Support** - Choose your preferred AI provider
- 🤖 **Auto-provider Selection** - Automatically uses best available AI
- 📋 **Comprehensive Reports** - Daily AI-powered analysis and insights

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- For local models: [Ollama](https://ollama.ai/) installed
- For Gemini: Google API key

### Installation
```bash
# Clone the repository
git clone https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment.git
cd ChatGPT-Micro-Cap-Experiment

# Install Python dependencies
pip install -r requirements.txt

# Run setup script
python setup_local_llm.py

# Configure your AI provider in .env file
# For Ollama: Set OLLAMA_MODEL=llama2 (or your preferred model)
# For Gemini: Set GOOGLE_API_KEY=your_api_key_here
```

### Using Local Models (Recommended)
```bash
# Install Ollama (visit https://ollama.ai/)
# Then pull a model:
ollama pull llama2

# Or try other models:
ollama pull mistral
ollama pull neural-chat

# Run the enhanced trading script
python run_analysis.py daily
```

### Using Google Gemini
```bash
# Get API key from Google AI Studio
# Add to .env file: GOOGLE_API_KEY=your_key_here

# Run the enhanced trading script
python run_analysis.py daily
```

## 🎯 Complete AI Integration

The repository now features **comprehensive AI integration** across all components:

### Core AI Components:
- **`llm_integration.py`** - Core AI analysis engine
- **`ai_config.py`** - Centralized AI configuration management  
- **`portfolio_manager.py`** - AI-powered portfolio management system
- **`run_analysis.py`** - Simple CLI interface for all AI features

### Enhanced Scripts:
- **`Trading_Script.py`** - Now includes AI analysis of portfolio and significant moves
- **`enhanced_trading_script.py`** - Advanced AI-powered trading with research capabilities
- **`Generate_Graph.py`** - Performance visualization with AI performance analysis

### AI Features Throughout:
✅ **Portfolio Analysis** - Daily AI evaluation of holdings and performance  
✅ **Stock Research** - AI-powered deep research on individual stocks  
✅ **Trading Strategy** - AI generates specific buy/sell recommendations  
✅ **Risk Management** - AI monitors stop-losses and portfolio risk  
✅ **Performance Tracking** - AI analyzes returns vs benchmarks  
✅ **Market Analysis** - AI evaluates significant price movements  
✅ **Report Generation** - Comprehensive AI-powered daily reports  
✅ **Auto-Documentation** - All AI insights automatically saved to files

### Simple Usage:
```bash
# Complete daily analysis (recommended)
python run_analysis.py daily

# Quick performance check
python run_analysis.py performance

# Research any stock
python run_analysis.py research TICKER
```

# Follow Along
The experiment runs June 2025 to December 2025.
Every trading day I will update the portfolio CSV file.
If you feel inspired to do something simiar, feel free to use this as a blueprint.

Updates are posted weekly on my blog — more coming soon!

One final shameless plug: (https://substack.com/@nathanbsmith?utm_source=edit-profile-page)

## 🤝 Contributing

Interested in improving the AI analysis or adding new features? Contributions welcome!

- Add support for new local models
- Improve portfolio analysis prompts
- Enhance risk management algorithms
- Add new visualization features

Find a mistake in the logs or have advice?
Please Reach out here: nathanbsmith.business@gmail.com
