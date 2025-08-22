# credit_dashboard_hackathon.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from streamlit_autorefresh import st_autorefresh

# -------------------------
# Page Layout
# -------------------------
st.set_page_config(page_title="CredTech Dashboard", layout="wide")
st.title("📊 Real-Time Explainable Credit Intelligence Dashboard")
st.markdown("Monitor credit scores, stock trends, macro factors, and news events for multiple companies.")

# -------------------------
# Sidebar Filters
# -------------------------
sector_filter = st.sidebar.multiselect("Select Sector (Demo)", ["Tech", "Finance", "Energy"], default=["Tech"])
tickers_input = st.sidebar.text_area("Enter Stock Tickers (comma separated)", "AAPL, TSLA, MSFT")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
refresh_interval = st.sidebar.slider("Auto-refresh interval (minutes)", 1, 30, 10)

# -------------------------
# Auto-refresh
# -------------------------
st_autorefresh(interval=refresh_interval*60*1000, key="dashboard_refresh")

# -------------------------
# Initialize Sentiment Analyzer
# -------------------------
analyzer = SentimentIntensityAnalyzer()

# -------------------------
# FRED Macro Data (example: Fed Rate)
# -------------------------
def fetch_fred_series(series_id="FEDFUNDS"):
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key=YOUR_FRED_API_KEY&file_type=json"
        r = requests.get(url).json()
        df = pd.DataFrame(r["observations"])
        df["value"] = pd.to_numeric(df["value"], errors='coerce')
        df["date"] = pd.to_datetime(df["date"])
        return df[["date","value"]].dropna()
    except:
        return pd.DataFrame(columns=["date","value"])

macro_data = fetch_fred_series()

# -------------------------
# Function: Event Classification
# -------------------------
def classify_event(title):
    title_lower = title.lower()
    if "debt" in title_lower or "bankruptcy" in title_lower or "restructuring" in title_lower:
        return "High Risk Event"
    elif "earnings beat" in title_lower or "growth" in title_lower or "profit" in title_lower:
        return "Positive Event"
    elif "warn" in title_lower or "decline" in title_lower:
        return "Warning Event"
    else:
        return "Neutral Event"

# -------------------------
# Function: Score Color Indicator
# -------------------------
def score_color(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


# -------------------------
# Fetch Data and Compute Scores
# -------------------------
all_data = []
for ticker in tickers:
    try:
        # Stock data
        data = yf.download(ticker, period="30d", interval="1d")
        if data.empty or len(data)<2:
            st.warning(f"No sufficient data for {ticker}, skipping...")
            continue

        # Price contribution
        price_change = float((data["Close"].iloc[-1] - data["Close"].iloc[0])/data["Close"].iloc[0])

        # News sentiment + events
        rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        feed = feedparser.parse(rss_url)
        news_scores, news_titles, news_dates, news_events = [], [], [], []
        for entry in feed.entries[:5]:
            title = entry.title
            score = analyzer.polarity_scores(title)["compound"]
            event = classify_event(title)
            news_scores.append(float(score))
            news_titles.append(title)
            news_dates.append(entry.get("published", f"Item {len(news_titles)+1}"))
            news_events.append(event)
        avg_sentiment = float(np.mean(news_scores)) if news_scores else 0

        # Macro contribution (latest value change)
        macro_factor = 0
        if not macro_data.empty:
            macro_factor = (macro_data["value"].iloc[-1] - macro_data["value"].iloc[0]) / macro_data["value"].iloc[0]

        # Credit score formula
        score = 50 + price_change*100 + avg_sentiment*20 - macro_factor*10
        score = max(0,min(100,score))

        # Daily alert
        daily_change = float((data["Close"].iloc[-1]-data["Close"].iloc[-2])/data["Close"].iloc[-2])
        alert = "🔴" if abs(daily_change) > 0.05 else ""

        all_data.append({
            "Ticker": ticker,
            "Price Contribution": round(price_change*100,2),
            "Sentiment Contribution": round(avg_sentiment*20,2),
            "Macro Contribution": round(-macro_factor*10,2),
            "Credit Score": round(score,2),
            "Score Indicator": score_color(score),
            "Alert": alert,
            "News Titles": news_titles,
            "News Scores": news_scores,
            "News Dates": news_dates,
            "News Events": news_events,
            "Stock Data": data,
            "Summary": f"{ticker}: Price {price_change*100:+.2f}%, Avg News Sentiment {avg_sentiment:+.2f}, Macro Impact {macro_factor*100:+.2f}% → Score {round(score,2)} {score_color(score)}"
        })

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")

# -------------------------
# Display Table with Feature Contributions
# -------------------------
if all_data:
    df = pd.DataFrame(all_data)
    st.subheader("Company Overview")
    st.dataframe(df[["Ticker","Price Contribution","Sentiment Contribution","Macro Contribution","Credit Score","Score Indicator","Alert"]]
                 .sort_values("Credit Score",ascending=False))

# -------------------------
# Feature Contribution Bar Chart
# -------------------------
if all_data:
    st.subheader("Feature Contributions per Company")
    for company in all_data:
        features = ["Price Contribution","Sentiment Contribution","Macro Contribution"]
        values = [company[f] for f in features]
        fig = px.bar(x=features, y=values, title=f"{company['Ticker']} Feature Breakdown", text=values)
        st.plotly_chart(fig)

# -------------------------
# Combined Stock Price Trend
# -------------------------
if all_data:
    st.subheader("Stock Price Trends")
    fig_price = px.line(title="Stock Prices Last 30 Days")
    for company in all_data:
        fig_price.add_scatter(x=company["Stock Data"].index, y=company["Stock Data"]["Close"], mode='lines', name=company["Ticker"])
    st.plotly_chart(fig_price)

# -------------------------
# Combined News Sentiment Trend
# -------------------------
if all_data:
    st.subheader("News Sentiment Trends")
    fig_sent = px.line(title="News Sentiment Last 5 Items")
    for company in all_data:
        if company["News Scores"]:
            fig_sent.add_scatter(x=company["News Dates"], y=company["News Scores"], mode='lines+markers', name=company["Ticker"])
    st.plotly_chart(fig_sent)

# -------------------------
# Individual Company Events & Summary
# -------------------------
st.subheader("Company Summaries & News")
for company in all_data:
    st.markdown(f"### {company['Ticker']} Summary")
    st.write(company["Summary"])
    if company["News Titles"]:
        for title, score, event in zip(company["News Titles"], company["News Scores"], company["News Events"]):
            sentiment_label = "Positive" if score>0.05 else "Negative" if score<-0.05 else "Neutral"
            st.write(f"- ({sentiment_label} / {event}) {title}")
    else:
        st.write("- No recent news found.")

# -------------------------
# Download CSV
# -------------------------
# -------------------------
# Download Excel
# -------------------------
import io
import pandas as pd

df_to_save = df[["Ticker","Price Contribution","Sentiment Contribution",
                 "Macro Contribution","Credit Score","Score Indicator","Alert"]]

# Create in-memory Excel file
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_to_save.to_excel(writer, index=False, sheet_name='Credit Data')

processed_data = output.getvalue()
st.download_button(
    "Download Excel Data",
    data=processed_data,
    file_name="credit_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# -------------------------
# Auto-refresh info
# -------------------------
st.info(f"This dashboard auto-refreshes every {refresh_interval} minutes for near real-time updates.")
