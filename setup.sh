#!/bin/bash

# AWS Expense Tracker Setup Script
echo "🏦 Setting up AWS Expense Tracker..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Download from: https://python.org/"
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup React Frontend
echo "📦 Setting up React frontend..."
cd react-app
if [ ! -d "node_modules" ]; then
    npm install
    echo "✅ Frontend dependencies installed!"
else
    echo "✅ Frontend dependencies already installed!"
fi
cd ..

# Setup Python Backend
echo "🐍 Setting up Python backend..."
cd server

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
echo "✅ Backend dependencies installed!"

cd ..

echo ""
echo "🎉 Setup complete! Here's how to run the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd server && source venv/bin/activate && python app.py"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   cd react-app && npm run dev"
echo ""
echo "3. Open your browser to: http://localhost:5173"
echo ""
echo "📚 Don't forget to:"
echo "   - Watch the instruction video for a complete walkthrough"
echo "   - Download the sample CSV to test all features"
echo "   - Upload your own transaction data to get personalized insights"
echo ""
echo "🚀 Happy expense tracking!"
