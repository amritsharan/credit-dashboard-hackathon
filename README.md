# 📊 CredTech Dashboard - Real-Time Explainable Credit Intelligence

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://credtech-dashboard.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Monitor credit scores, stock trends, macroeconomic factors, and real-time news events for multiple companies in one intelligent dashboard.**

## 🌟 Overview

CredTech Dashboard is a sophisticated, real-time financial intelligence platform that combines machine learning, financial data analysis, and sentiment analysis to provide explainable credit intelligence scores. Perfect for financial analysts, risk managers, and investment professionals.

### Key Highlights
- 🚀 **Real-Time Data**: Live stock prices, macro indicators, and news feeds
- 🧠 **Explainable AI**: Understand which factors contribute to credit scores
- 📈 **Multi-Ticker Support**: Monitor multiple companies simultaneously
- 🔄 **Auto-Refresh**: Stay updated with configurable auto-refresh intervals
- 📊 **Interactive Visualizations**: Plotly charts for trend analysis
- 📥 **Excel Export**: Download scores and metrics with professional formatting
- 🎯 **Event Classification**: Automatic categorization of financial news

## 🎯 Features

### 1. **Real-Time Credit Scoring**
   - Composite credit scores based on multiple factors
   - Stock performance contribution analysis
   - News sentiment impact on creditworthiness

### 2. **Stock Trend Monitoring**
   - 30-day price history tracking
   - Percentage change calculations
   - Interactive price trend charts

### 3. **News & Sentiment Analysis**
   - Automated news feed parsing from Yahoo Finance
   - VADER sentiment analysis for news headlines
   - Event classification:
     - 🔴 **High Risk Events** (bankruptcy, debt restructuring)
     - 🟢 **Positive Events** (earnings beat, growth)
     - 🟡 **Warning Events** (declines, warnings)
     - ⚪ **Neutral Events**

### 4. **Macroeconomic Integration**
   - Federal Reserve data integration (FRED API)
   - Interest rate trends
   - Macro factor influence on credit scores

### 5. **Feature Attribution**
   - Transparent credit score breakdown
   - Contribution percentages for each factor
   - Visual feature importance charts

### 6. **Data Export**
   - Excel spreadsheet generation
   - Color-coded risk indicators
   - Professional formatting for reports

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/amritsharan/credit-dashboard-hackathon.git
cd credit-dashboard-hackathon
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys (Optional)
For full macroeconomic data integration, set your FRED API key:
```bash
# Create a .env file in the project root
FRED_API_KEY=your_fred_api_key_here
```

Get your free API key at [FRED API](https://fredaccount.stlouisfed.org/login/secure/)

### Step 4: Run the Dashboard
```bash
streamlit run credit_dashboard.py
```

The dashboard will open at `http://localhost:8501`

## 📖 Usage Guide

### Basic Workflow
1. **Select Sectors**: Choose industry sectors for context (Tech, Finance, Energy)
2. **Enter Tickers**: Input stock symbols (comma-separated): `AAPL, TSLA, MSFT`
3. **Configure Refresh**: Set auto-refresh interval (1-30 minutes)
4. **Monitor Dashboard**: View real-time scores and trends
5. **Export Data**: Download metrics to Excel for reporting

### Dashboard Sections

#### 📊 Credit Score Cards
- Individual company credit scores (0-100)
- Color-coded risk levels:
  - 🟢 **High** (70+): Strong creditworthiness
  - 🟡 **Medium** (40-69): Moderate risk
  - 🔴 **Low** (<40): High risk

#### 📈 Trend Charts
- Combined price and sentiment trends
- Feature contribution visualization
- Macro factor influence graphs

#### 📰 News & Events
- Latest relevant news articles
- Sentiment scores
- Event classifications
- Publication timestamps

## 📋 Requirements

```
streamlit              # Web app framework
yfinance              # Financial data fetching
pandas                # Data manipulation
numpy                 # Numerical computing
plotly                # Interactive visualizations
feedparser            # RSS feed parsing
vaderSentiment        # Sentiment analysis
requests              # HTTP library
xlsxwriter            # Excel file creation
streamlit-autorefresh # Auto-refresh functionality
```

## 🏗️ Project Architecture

```
credit-dashboard-hackathon/
├── credit_dashboard.py        # Main application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── assets/                    # (Optional) Images/logos
```

### Core Components

1. **Data Fetching**: Integrates with yfinance, Yahoo Finance RSS, and FRED API
2. **Sentiment Analysis**: Uses VADER for news headline analysis
3. **Score Calculation**: Weighted composite scoring algorithm
4. **Visualization**: Plotly Express for interactive charts
5. **Data Export**: XlsxWriter for professional Excel reports

## 🔧 Configuration Options

### Sidebar Settings
- **Sector Filter**: Multi-select industry categories
- **Stock Tickers**: Comma-separated ticker symbols
- **Auto-Refresh Interval**: 1-30 minute refresh cycles

### Customizable Parameters
- Credit score weights
- Sentiment score thresholds
- Risk event keywords
- Date ranges for historical analysis

## 📊 Data Sources

| Source | Data Type | Usage |
|--------|-----------|-------|
| **Yahoo Finance** | Stock prices, news | Price trends, sentiment |
| **FRED API** | Macro indicators | Interest rates, economic factors |
| **RSS Feeds** | News headlines | Event detection, sentiment |

## 🚀 Deployment

### Option 1: Streamlit Cloud (Free)
```bash
# Push to GitHub, then deploy at https://streamlit.io/cloud
```

### Option 2: AWS, Azure, or Docker
The app can be containerized and deployed to any cloud platform supporting Python.

## 📈 Example Use Cases

- **Risk Managers**: Monitor credit exposure across portfolio companies
- **Investors**: Screen companies by explainable credit scores
- **Analysts**: Track macro-sentiment relationships
- **Traders**: Detect market-moving news events in real-time
- **Researchers**: Study correlation between news sentiment and credit metrics

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Alternative sentiment models (FinBERT, RoBERTa)
- Additional credit factors (financial ratios, cash flow)
- Machine learning credit score predictions
- Multi-language news support
- Advanced charting and technical indicators

## ⚠️ Disclaimer

This dashboard is for educational and research purposes. It should not be used as the sole basis for financial decisions. Always consult with financial professionals before making investment decisions.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Amrit S R**
- GitHub: [@amritsharan](https://github.com/amritsharan)
- Project: [credit-dashboard-hackathon](https://github.com/amritsharan/credit-dashboard-hackathon)

## 🔗 Live Demo

Try the live dashboard: [CredTech Dashboard on Streamlit](https://credtech-dashboard.streamlit.app/)

## 📞 Support & Feedback

Have questions or suggestions? 
- Open an [Issue](https://github.com/amritsharan/credit-dashboard-hackathon/issues)
- Submit a [Pull Request](https://github.com/amritsharan/credit-dashboard-hackathon/pulls)
- Reach out on GitHub Discussions

---

<div align="center">

**Made with ❤️ for financial intelligence and data transparency**

⭐ If you find this useful, please consider giving it a star!

</div>

