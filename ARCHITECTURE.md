# CredTech Dashboard - Complete Project Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Bugs Found & Fixed](#bugs-found--fixed)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [API Reference](#api-reference)
7. [File Structure](#file-structure)
8. [Development](#development)
9. [Deployment](#deployment)

---

## Overview

CredTech Dashboard is a **production-ready** financial intelligence platform that analyzes credit scores, stock trends, news sentiment, and macroeconomic factors for companies. This version removes Streamlit and uses Flask for a professional, scalable backend.

### Key Changes from Original
- ✅ **Removed Streamlit** - Replaced with Flask for flexibility and performance
- ✅ **Added REST API** - Can be consumed by any frontend or application
- ✅ **Fixed Critical Bugs** - See section below
- ✅ **Professional Architecture** - Separated concerns (engine, API, frontend)
- ✅ **Production Ready** - Includes logging, error handling, validation
- ✅ **Easy to Test** - Business logic is decoupled from UI

---

## Bugs Found & Fixed

### 🔴 Critical Bugs

#### 1. **Hardcoded FRED API Key (String)**
**Original Code:**
```python
url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key=YOUR_FRED_API_KEY&file_type=json"
```
**Problem:** API key was never set to actual value, all FRED API calls failed silently
**Fixed:** Now reads from environment variable with proper error handling

```python
if not self.fred_api_key:
    logger.warning("FRED API key not set, returning empty data")
    return pd.DataFrame(columns=["date", "value"])
```

#### 2. **Division by Zero in Macro Calculation**
**Original Code:**
```python
macro_factor = (macro_data["value"].iloc[-1] - macro_data["value"].iloc[0]) / macro_data["value"].iloc[0]
```
**Problem:** If macro_data[0] == 0, causes ZeroDivisionError
**Fixed:**
```python
try:
    if len(macro_data) > 1 and macro_data["value"].iloc[0] != 0:
        macro_change = (macro_data["value"].iloc[-1] - macro_data["value"].iloc[0]) / macro_data["value"].iloc[0]
except (ZeroDivisionError, ValueError):
    macro_contribution = 0
```

#### 3. **Missing News Data Crashes App**
**Original Code:**
```python
avg_sentiment = float(np.mean(news_scores)) if news_scores else 0
# But later doesn't handle empty news_titles
for title, score, event in zip(company["News Titles"], company["News Scores"], company["News Events"]):
```
**Problem:** If news parsing fails, no fallback - app crashes
**Fixed:** Proper validation and empty array handling throughout

#### 4. **Unbounded Score Values**
**Original Code:**
```python
score = 50 + price_change*100 + avg_sentiment*20 - macro_factor*10
# No bounds checking - score could be 200 or -50
```
**Problem:** Score should be 0-100, but calculation could exceed bounds
**Fixed:**
```python
score = np.clip(score, 0, 100)  # Ensure 0-100 range
```

#### 5. **Uncaught Exception Swallows Errors**
**Original Code:**
```python
except:
    return pd.DataFrame(columns=["date","value"])
# Generic catch-all with no logging
```
**Problem:** Errors hidden, impossible to debug production issues
**Fixed:** Specific exceptions with detailed logging

```python
except requests.exceptions.RequestException as e:
    logger.error(f"Error fetching FRED data: {e}")
    return pd.DataFrame(columns=["date", "value"])
```

### 🟠 Major Issues

#### 6. **No Input Validation**
- Accepts invalid ticker formats
- No length limits on requests
- SQL injection-like vulnerabilities possible

**Fixed:** Validation in API endpoints
```python
if len(tickers) > 10:
    tickers = tickers[:10]  # Rate limiting
```

#### 7. **No Rate Limiting**
- Could send unlimited parallel requests
- Could exceed API quota quickly

**Fixed:** Added max 10 tickers per request

#### 8. **No Timeout Configuration**
- API calls could hang indefinitely
- Uses default Python timeout (very long)

**Fixed:** Added 10-second timeout
```python
r = requests.get(url, timeout=10)
```

#### 9. **No Logging System**
- Impossible to debug production issues
- Error details lost

**Fixed:** Comprehensive logging throughout
```python
logger = logging.getLogger(__name__)
logger.error(f"Error: {e}")
```

#### 10. **Tight Coupling to Streamlit UI**
- Can't reuse code elsewhere
- Hard to test business logic
- Can't create alternative UI easily

**Fixed:** Separated into:
- `engine.py` - Pure business logic
- `app.py` - Flask API layer
- `index.html` - Clean frontend

---

## Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────┐
│         Frontend (HTML)          │
│  index.html - Interactive UI    │
└──────────────┬──────────────────┘
               │ HTTP/JSON
┌──────────────▼──────────────────┐
│      API Layer (Flask)           │
│      app.py - REST endpoints     │
└──────────────┬──────────────────┘
               │ Python
┌──────────────▼──────────────────┐
│    Business Logic (engine.py)    │
│  CredTechEngine class            │
└──────────────────────────────────┘
     │
     ├─ yfinance (stock data)
     ├─ feedparser (news)
     ├─ VADER (sentiment)
     └─ FRED API (macroeconomic)
```

### Files

| File | Purpose |
|------|---------|
| `engine.py` | Core business logic, data analysis |
| `app.py` | Flask API routes and error handling |
| `index.html` | Interactive dashboard frontend |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore configuration |

---

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Internet connection

### Step 1: Clone Repository
```bash
git clone https://github.com/amritsharan/credit-dashboard-hackathon.git
cd credit-dashboard-hackathon
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your FRED API key (optional)
# Get free key at: https://fredaccount.stlouisfed.org/login/secure/
```

---

## Running the Application

### Development Mode
```bash
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Open browser: `http://localhost:5000`

### Production Mode (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## API Reference

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Analyze Multiple Tickers
**POST** `/api/analyze`

Request:
```json
{
  "tickers": ["AAPL", "MSFT", "TSLA"]
}
```

Response:
```json
{
  "status": "success",
  "data": [
    {
      "ticker": "AAPL",
      "score": {
        "score": 75.5,
        "price_contribution": 15.2,
        "sentiment_contribution": 8.5,
        "macro_contribution": -2.1,
        "volatility_penalty": 0,
        "daily_change": 1.2,
        "avg_sentiment": 0.284,
        "price_change_30d": 8.5,
        "risk_level": "High",
        "alert": ""
      },
      "news": [
        {
          "title": "Apple Beats Q1 Earnings",
          "sentiment_score": 0.875,
          "event_type": "Positive Event",
          "published": "2026-02-03T..."
        }
      ],
      "current_price": 185.50,
      "timestamp": "2026-02-03T..."
    }
  ],
  "count": 3
}
```

#### 2. Analyze Single Ticker
**GET** `/api/ticker/<ticker>`

Example: `GET /api/ticker/AAPL`

Response: (same as above, single item)

#### 3. Export Data
**POST** `/api/export`

Request:
```json
{
  "tickers": ["AAPL", "MSFT"]
}
```

Response: JSON format of all analysis data

#### 4. Health Check
**GET** `/api/health`

Response:
```json
{
  "status": "healthy",
  "service": "CredTech Dashboard API",
  "version": "1.0.0"
}
```

### Error Responses

**400 Bad Request**
```json
{
  "status": "error",
  "message": "Tickers must be a non-empty array"
}
```

**404 Not Found**
```json
{
  "status": "error",
  "message": "No data available for ticker INVALID"
}
```

**500 Internal Error**
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## File Structure

```
credit-dashboard-hackathon/
├── engine.py                 # Core analysis engine
├── app.py                    # Flask API
├── index.html                # Frontend dashboard
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── .gitignore                # Git configuration
├── setup.bat                 # Windows setup script
├── setup.sh                  # Unix setup script
├── README.md                 # User-friendly guide
├── GITHUB.md                 # GitHub setup guide
├── ARCHITECTURE.md           # This file
└── .git/                     # Git repository
```

---

## Development

### Adding New Features

#### 1. Add to Business Logic (engine.py)
```python
def new_analysis_method(self, ticker):
    """Add new analysis capability"""
    # Implement analysis
    return results
```

#### 2. Add API Route (app.py)
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    # Call engine method
    results = engine.new_analysis_method(ticker)
    return jsonify({"status": "success", "data": results})
```

#### 3. Update Frontend (index.html)
```javascript
// Add API call in JavaScript
const response = await fetch(`${API_BASE}/new-endpoint`, {...});
```

### Testing
```bash
# Test single ticker
curl http://localhost:5000/api/ticker/AAPL

# Test multiple tickers
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "MSFT"]}'

# Health check
curl http://localhost:5000/api/health
```

---

## Deployment

### Option 1: Heroku
```bash
# Create Procfile with:
# web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app

git push heroku main
```

### Option 2: AWS EC2
```bash
# SSH into instance
ssh -i key.pem ec2-user@instance

# Setup and run
git clone <repo>
cd credit-dashboard-hackathon
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## License

MIT License - See LICENSE file

## Author

**Amrit S R**
- GitHub: [@amritsharan](https://github.com/amritsharan)

---

**Last Updated**: February 3, 2026
