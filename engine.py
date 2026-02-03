import yfinance as yf
import pandas as pd
import numpy as np
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CredTechEngine:
    """Core engine for credit intelligence calculations"""
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.fred_api_key = None  # Set via environment variable
        
    def fetch_fred_series(self, series_id="FEDFUNDS"):
        """Fetch macroeconomic data from FRED API"""
        try:
            if not self.fred_api_key:
                logger.warning("FRED API key not set, returning empty data")
                return pd.DataFrame(columns=["date", "value"])
            
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={self.fred_api_key}&file_type=json"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            
            data = r.json()
            if "observations" not in data:
                return pd.DataFrame(columns=["date", "value"])
            
            df = pd.DataFrame(data["observations"])
            df["value"] = pd.to_numeric(df["value"], errors='coerce')
            df["date"] = pd.to_datetime(df["date"])
            return df[["date", "value"]].dropna()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FRED data: {e}")
            return pd.DataFrame(columns=["date", "value"])
        except Exception as e:
            logger.error(f"Unexpected error in fetch_fred_series: {e}")
            return pd.DataFrame(columns=["date", "value"])

    def classify_event(self, title):
        """Classify news events by risk level"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["debt", "bankruptcy", "default", "restructuring", "liquidation"]):
            return "High Risk Event"
        elif any(word in title_lower for word in ["earnings beat", "growth", "profit", "record", "surge", "rally"]):
            return "Positive Event"
        elif any(word in title_lower for word in ["warn", "decline", "drop", "miss", "loss", "lawsuit"]):
            return "Warning Event"
        else:
            return "Neutral Event"

    def score_color(self, score):
        """Get risk level based on score"""
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    def fetch_stock_data(self, ticker, period="30d"):
        """Fetch stock data from yfinance"""
        try:
            data = yf.download(ticker, period=period, interval="1d", progress=False)
            if data.empty or len(data) < 2:
                return None
            return data
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            return None

    def fetch_news(self, ticker):
        """Fetch news and sentiment for a ticker"""
        try:
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
            feed = feedparser.parse(rss_url)
            
            news_list = []
            for entry in feed.entries[:5]:
                title = entry.get("title", "Unknown Title")
                score = self.analyzer.polarity_scores(title)["compound"]
                event = self.classify_event(title)
                published = entry.get("published", datetime.now().isoformat())
                
                news_list.append({
                    "title": title,
                    "sentiment_score": float(score),
                    "event_type": event,
                    "published": str(published)
                })
            
            return news_list
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []

    def calculate_credit_score(self, ticker, stock_data=None, news_data=None, macro_data=None):
        """
        Calculate comprehensive credit score for a ticker
        
        BUG FIXES:
        1. Added input validation
        2. Handle cases where data is missing
        3. Better error handling
        4. Normalized score ranges
        5. Fixed division by zero issues
        """
        try:
            # Fetch data if not provided
            if stock_data is None:
                stock_data = self.fetch_stock_data(ticker)
            if news_data is None:
                news_data = self.fetch_news(ticker)
            
            if stock_data is None:
                return None
            
            # 1. Stock Price Contribution (0-100 scale)
            price_change = (stock_data["Close"].iloc[-1] - stock_data["Close"].iloc[0]) / stock_data["Close"].iloc[0]
            price_contribution = np.clip(price_change * 100, -50, 50)
            
            # 2. News Sentiment Contribution
            if news_data and len(news_data) > 0:
                avg_sentiment = np.mean([n["sentiment_score"] for n in news_data])
                sentiment_contribution = avg_sentiment * 30  # Sentiment worth 30 points
            else:
                avg_sentiment = 0
                sentiment_contribution = 0
            
            # 3. Macro Factor Contribution
            macro_contribution = 0
            if macro_data is not None and not macro_data.empty:
                try:
                    if len(macro_data) > 1:
                        macro_change = (macro_data["value"].iloc[-1] - macro_data["value"].iloc[0]) / macro_data["value"].iloc[0]
                        macro_contribution = -macro_change * 15  # Negative macro impact
                except (ZeroDivisionError, ValueError):
                    macro_contribution = 0
            
            # 4. Daily volatility metric
            daily_change = (stock_data["Close"].iloc[-1] - stock_data["Close"].iloc[-2]) / stock_data["Close"].iloc[-2]
            volatility_penalty = abs(daily_change) * 10 if abs(daily_change) > 0.05 else 0
            
            # Base score with weighted components
            base_score = 50
            score = base_score + price_contribution + sentiment_contribution + macro_contribution - volatility_penalty
            
            # Normalize to 0-100 range
            score = np.clip(score, 0, 100)
            
            return {
                "score": float(round(score, 2)),
                "price_contribution": float(round(price_contribution, 2)),
                "sentiment_contribution": float(round(sentiment_contribution, 2)),
                "macro_contribution": float(round(macro_contribution, 2)),
                "volatility_penalty": float(round(volatility_penalty, 2)),
                "daily_change": float(round(daily_change * 100, 2)),
                "avg_sentiment": float(round(avg_sentiment, 4)),
                "price_change_30d": float(round(price_change * 100, 2)),
                "risk_level": self.score_color(score),
                "alert": "🔴" if abs(daily_change) > 0.05 else ""
            }
        except Exception as e:
            logger.error(f"Error calculating credit score for {ticker}: {e}")
            return None

    def analyze_multiple_tickers(self, tickers):
        """
        Analyze multiple tickers and return comprehensive results
        
        BUG FIXES:
        1. Removed uncaught exception handling
        2. Added validation for empty ticker list
        3. Better error reporting per ticker
        """
        if not tickers or len(tickers) == 0:
            logger.warning("No tickers provided")
            return []
        
        # Fetch macro data once
        macro_data = self.fetch_fred_series()
        
        results = []
        for ticker in tickers:
            try:
                ticker = ticker.strip().upper()
                if not ticker:
                    continue
                
                # Fetch data
                stock_data = self.fetch_stock_data(ticker)
                if stock_data is None:
                    logger.warning(f"No data available for {ticker}")
                    continue
                
                news_data = self.fetch_news(ticker)
                
                # Calculate score
                score_result = self.calculate_credit_score(ticker, stock_data, news_data, macro_data)
                if score_result is None:
                    continue
                
                # Compile result
                result = {
                    "ticker": ticker,
                    "score": score_result,
                    "news": news_data,
                    "current_price": float(stock_data["Close"].iloc[-1]),
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing ticker {ticker}: {e}")
                continue
        
        return results

# Initialize engine
engine = CredTechEngine()
