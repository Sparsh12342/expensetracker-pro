#!/usr/bin/env python3
"""
Simple script to run the Flask backend server
"""
import os
import sys

# Add the server directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    print("🏦 Starting Expense Tracker Backend Server...")
    print("📍 Server will be available at: http://127.0.0.1:5050")
    print("🔗 Health check: http://127.0.0.1:5050/health")
    print("=" * 50)
    
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=True,
        use_reloader=True
    )


