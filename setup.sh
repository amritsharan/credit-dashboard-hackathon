#!/bin/bash

# CredTech Dashboard - Development Setup Script

echo "================================"
echo "CredTech Dashboard Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your FRED API key"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the dashboard, run:"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
