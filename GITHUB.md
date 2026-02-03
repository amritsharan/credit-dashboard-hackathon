# CredTech Dashboard - GitHub Configuration

This is the GitHub configuration file. Use these commands to get started:

## Installation

1. Clone the repository:
```bash
git clone https://github.com/amritsharan/credit-dashboard-hackathon.git
cd credit-dashboard-hackathon
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Add your FRED API key to `.env` (optional, for macro data):
- Get a free key at: https://fredaccount.stlouisfed.org/login/secure/

6. Run the Flask application:
```bash
python app.py
```

7. Open your browser and go to `http://localhost:5000`

## For Production (Using Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

- `GET /` - Serve the dashboard UI
- `POST /api/analyze` - Analyze multiple tickers
- `GET /api/ticker/<ticker>` - Analyze a single ticker
- `POST /api/export` - Export analysis data
- `GET /api/health` - Health check

### Example API Request

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "MSFT", "TSLA"]}'
```

## Architecture

- **Backend**: Flask + Python
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Data Sources**: yfinance, Yahoo Finance RSS, FRED API
- **Analysis**: VADER sentiment analysis, financial metrics calculation

## Bug Fixes from Original

1. **Fixed FRED API error handling** - Now gracefully handles missing API key
2. **Fixed division by zero** - Added checks for macro data calculations
3. **Fixed missing data handling** - Validates stock data before processing
4. **Fixed news parsing errors** - Better error handling for RSS feeds
5. **Fixed uncaught exceptions** - Added try-catch blocks throughout
6. **Fixed score normalization** - Clipped scores to 0-100 range
7. **Added input validation** - Validates tickers before processing
8. **Added rate limiting** - Limited to 10 tickers per request
9. **Added proper logging** - Logger tracks all major operations
10. **Removed Streamlit dependency** - Now uses Flask for better control

## Bugs Found & Fixed

### Critical Bugs
1. **FRED API Key Hardcoded as String** - "YOUR_FRED_API_KEY" was never replaced, causing API calls to fail
2. **Division by Zero Risk** - Macro data changes could cause division by zero if values are identical
3. **Missing Data Not Handled** - Code assumes news exists, crashes if no news available
4. **Exception Swallowed** - General except clauses caught all errors without logging
5. **Score Calculation Unbounded** - Scores could exceed 100 or go below 0

### Major Issues
6. **No Input Validation** - Accepts any ticker format, can cause API errors
7. **Poor Error Messages** - Users get generic errors with no actionable info
8. **Missing Rate Limiting** - Could send unlimited requests to APIs
9. **No Timeout Configuration** - API calls could hang indefinitely
10. **Hard to Test** - Everything mixed in Streamlit UI, can't test logic separately

### Design Issues
11. **UI Tightly Coupled** - Business logic mixed with Streamlit UI code
12. **No API Layer** - Can't use the analysis from other applications
13. **No Logging** - Difficult to debug production issues
14. **Stateless** - Can't track analysis history or cache results
