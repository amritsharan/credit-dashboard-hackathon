#!/usr/bin/env python
"""Test the Flask API"""

import requests
import json

print("=" * 70)
print("Testing CredTech Dashboard Flask API")
print("=" * 70)

# Test the API
url = "http://localhost:5000/api/analyze"
payload = {"tickers": ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]}

print(f"\nRequest: POST {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("-" * 70)

try:
    response = requests.post(url, json=payload)
    data = response.json()
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response Status: {data.get('status')}")
    print(f"✅ Tickers Analyzed: {data.get('count')}")
    
    print("\n" + "=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)
    
    for ticker_data in data.get('data', []):
        ticker = ticker_data['ticker']
        score = ticker_data['score']['score']
        risk = ticker_data['score']['risk_level']
        price = ticker_data['current_price']
        sentiment = ticker_data['score']['avg_sentiment']
        price_change = ticker_data['score']['price_change_30d']
        news_count = len(ticker_data['news'])
        
        print(f"\n📊 {ticker}")
        print(f"   Score: {score}/100 ({risk} Risk)")
        print(f"   Current Price: ${price:.2f}")
        print(f"   30-Day Change: {price_change:+.2f}%")
        print(f"   Avg Sentiment: {sentiment:+.4f}")
        print(f"   News Items: {news_count}")
        
        if ticker_data['news']:
            first_news = ticker_data['news'][0]
            print(f"   Latest: {first_news['event_type']}")
            print(f"           {first_news['title'][:70]}")
    
    print("\n" + "=" * 70)
    print("Full API Response (JSON):")
    print("=" * 70)
    print(json.dumps(data, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
