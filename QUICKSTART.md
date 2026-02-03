# Quick Start Guide

## For Windows Users

### 1. One-Click Setup
Double-click `setup.bat` and follow the prompts.

### 2. Run the Application
```bash
python app.py
```

### 3. Open Dashboard
Go to `http://localhost:5000` in your browser

---

## For macOS/Linux Users

### 1. Quick Setup
```bash
bash setup.sh
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Dashboard
Go to `http://localhost:5000` in your browser

---

## Test the Dashboard

Once running, try these tickers:
- **Tech**: AAPL, MSFT, TSLA, NVDA, GOOGL
- **Finance**: JPM, BAC, GS, BLK, WFC
- **Energy**: XOM, CVX, COP, SLB, MPC

Example: Type `AAPL, MSFT, TSLA` and click "Analyze"

---

## Troubleshooting

### Port 5000 Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Python Not Found
- Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH"

### Dependencies Installation Fails
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### API Connection Error
- Make sure Flask is running (`python app.py`)
- Check you're accessing `http://localhost:5000` (not https)

---

## Next Steps

1. ✅ **Customize Tickers** - Add your favorite stocks
2. ✅ **Set FRED API Key** - Get macro data (optional)
3. ✅ **Deploy** - Use Heroku, AWS, or Docker
4. ✅ **Extend** - Add more analysis metrics

---

## Support

- 📖 See `README.md` for detailed documentation
- 🏗️ See `ARCHITECTURE.md` for technical details
- 🔧 See `GITHUB.md` for GitHub setup

Happy analyzing! 📊
