# 🏦 Expense Tracker - Full Stack Setup

This guide will help you run both the frontend and backend simultaneously.

## 🚀 Quick Start

### Option 1: Run Everything at Once (Recommended)

```bash
# Install all dependencies (run this once)
npm run install-all

# Start both frontend and backend simultaneously
npm run dev
```

### Option 2: Run Separately

```bash
# Terminal 1 - Backend
cd server
python run.py

# Terminal 2 - Frontend
cd react-app
npm run dev
```

## 📋 What Each Command Does

- **`npm run dev`** - Runs both frontend and backend simultaneously using concurrently
- **`npm run frontend`** - Runs only the React frontend (usually on http://localhost:5173)
- **`npm run backend`** - Runs only the Flask backend (on http://localhost:5050)
- **`npm run install-all`** - Installs all dependencies for both frontend and backend

## 🔧 Manual Setup (if needed)

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python run.py
```

### Frontend Setup

```bash
cd react-app
npm install
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend API**: http://localhost:5050
- **Health Check**: http://localhost:5050/health

## 🛠️ Troubleshooting

### Port Already in Use

If you get port conflicts:

- Backend (5050): Change port in `server/run.py`
- Frontend (5173): Vite will automatically find next available port

### Python Dependencies

Make sure you have Python 3.8+ and pip installed:

```bash
python --version
pip --version
```

### Node Dependencies

Make sure you have Node.js 16+ and npm installed:

```bash
node --version
npm --version
```

## 📁 Project Structure

```
expense-tracker/
├── react-app/          # React frontend
├── server/             # Flask backend
├── package.json        # Root package with dev scripts
└── SETUP.md           # This file
```

## 🎯 Development Workflow

1. Run `npm run dev` to start both servers
2. Frontend will automatically proxy API calls to backend
3. Both servers will auto-reload on file changes
4. Check browser console for any connection issues

Happy coding! 🚀


