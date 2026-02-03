from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from engine import CredTechEngine
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize engine
engine = CredTechEngine()
engine.fred_api_key = os.getenv('FRED_API_KEY')

# -------------------------
# Routes
# -------------------------

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze one or more tickers
    
    Request body:
    {
        "tickers": ["AAPL", "MSFT", "TSLA"]
    }
    
    Returns:
    {
        "status": "success",
        "data": [
            {
                "ticker": "AAPL",
                "score": {...},
                "news": [...],
                "current_price": 150.25,
                "timestamp": "2026-02-03T..."
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'tickers' not in data:
            return jsonify({
                "status": "error",
                "message": "Request must contain 'tickers' array"
            }), 400
        
        tickers = data.get('tickers', [])
        
        # Validate tickers
        if not isinstance(tickers, list) or len(tickers) == 0:
            return jsonify({
                "status": "error",
                "message": "Tickers must be a non-empty array"
            }), 400
        
        # Limit to 10 tickers per request
        if len(tickers) > 10:
            tickers = tickers[:10]
        
        # Analyze
        results = engine.analyze_multiple_tickers(tickers)
        
        return jsonify({
            "status": "success",
            "data": results,
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in /api/analyze: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/ticker/<ticker>', methods=['GET'])
def analyze_single(ticker):
    """
    Analyze a single ticker
    
    Returns:
    {
        "status": "success",
        "data": {...}
    }
    """
    try:
        ticker = ticker.strip().upper()
        if not ticker or len(ticker) > 5:
            return jsonify({
                "status": "error",
                "message": "Invalid ticker format"
            }), 400
        
        results = engine.analyze_multiple_tickers([ticker])
        
        if not results:
            return jsonify({
                "status": "error",
                "message": f"No data available for ticker {ticker}"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": results[0]
        })
    
    except Exception as e:
        logger.error(f"Error in /api/ticker/{ticker}: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "CredTech Dashboard API",
        "version": "1.0.0"
    })

@app.route('/api/export', methods=['POST'])
def export_data():
    """
    Export analysis results as JSON
    (Can be extended to support CSV, Excel)
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        results = engine.analyze_multiple_tickers(tickers)
        
        return jsonify({
            "status": "success",
            "data": results,
            "export_format": "json",
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in /api/export: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------------
# Error Handlers
# -------------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Resource not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Run the Flask app
    # For production, use a WSGI server like Gunicorn
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
