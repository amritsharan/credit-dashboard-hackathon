#!/usr/bin/env python
"""Quick test to verify real data is being fetched"""

from engine import CredTechEngine

print("=" * 60)
print("Testing CredTech Dashboard - Real Data Fetch")
print("=" * 60)

engine = CredTechEngine()

# Test with multiple tickers
tickers = ['AAPL', 'MSFT', 'TSLA']
print(f"\nAnalyzing: {', '.join(tickers)}")
print("-" * 60)

results = engine.analyze_multiple_tickers(tickers)

if results:
    print(f"✅ SUCCESS! Fetched {len(results)} tickers\n")
    
    for ticker_data in results:
        print(f"📊 {ticker_data['ticker']}")
        print(f"   Credit Score: {ticker_data['score']['score']}/100")
        print(f"   Risk Level: {ticker_data['score']['risk_level']}")
        print(f"   Current Price: ${ticker_data['current_price']:.2f}")
        print(f"   30-day Change: {ticker_data['score']['price_change_30d']:+.2f}%")
        print(f"   Sentiment: {ticker_data['score']['avg_sentiment']:+.3f}")
        print(f"   Latest News: {len(ticker_data['news'])} items")
        if ticker_data['news']:
            print(f"   Top News: {ticker_data['news'][0]['title'][:60]}...")
        print()
else:
    print("❌ FAILED - No data fetched")
    print("\nPossible issues:")
    print("1. Internet connection problem")
    print("2. API rate limiting")
    print("3. Invalid ticker symbols")
