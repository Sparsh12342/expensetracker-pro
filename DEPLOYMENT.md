# 🚀 Deployment Guide - ExpenseTracker Pro

This guide will help you deploy your ExpenseTracker Pro application to production.

## 📋 Overview

The application consists of two parts:
- **Frontend**: React + TypeScript (deploy to Vercel)
- **Backend**: Python + Flask (deploy to Railway/Render)

## 🎯 Step 1: Deploy Frontend to Vercel

### Option A: Deploy via Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your repository**: `https://github.com/Sparsh12342/expensetracker-pro`
4. **Configure the project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `react-app`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Set Environment Variables**:
   - `VITE_API_URL`: Your backend URL (set after backend deployment)
6. **Click "Deploy"**

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd react-app

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variable
vercel env add VITE_API_URL production
```

## 🐍 Step 2: Deploy Backend to Railway

### Option A: Deploy to Railway (Recommended)

1. **Go to [railway.app](https://railway.app)** and sign in
2. **Click "New Project"** → **"Deploy from GitHub repo"**
3. **Select your repository**: `Sparsh12342/expensetracker-pro`
4. **Configure deployment**:
   - **Root Directory**: `server`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. **Set Environment Variables**:
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `False`
6. **Deploy**

### Option B: Deploy to Render

1. **Go to [render.com](https://render.com)** and sign in
2. **Click "New"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure**:
   - **Name**: `expensetracker-pro-backend`
   - **Root Directory**: `server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. **Deploy**

## 🔧 Step 3: Update Frontend API URL

After your backend is deployed:

1. **Copy your backend URL** (e.g., `https://your-app.railway.app`)
2. **Go to your Vercel dashboard**
3. **Navigate to your project** → **Settings** → **Environment Variables**
4. **Update `VITE_API_URL`** with your backend URL
5. **Redeploy** your frontend

## 🐳 Alternative: Deploy with Docker

### Frontend (Vercel)
Vercel automatically detects and builds from the `Dockerfile` in the `react-app` directory.

### Backend (Railway/Render)
Both Railway and Render support Docker deployments. The `server/Dockerfile` is ready to use.

## 📝 Environment Variables

### Frontend (Vercel)
- `VITE_API_URL`: Your backend API URL

### Backend (Railway/Render)
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `False`
- `PORT`: Auto-set by platform

## 🔍 Testing Your Deployment

1. **Check Frontend**: Visit your Vercel URL
2. **Test API**: Visit `https://your-backend-url/health` (if available)
3. **Upload Sample Data**: Use the sample CSV to test functionality
4. **Verify Features**: Test categorization, filtering, and recommendations

## 🛠️ Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend allows your frontend domain
2. **API Not Found**: Check that `VITE_API_URL` is set correctly
3. **Build Failures**: Check that all dependencies are in `package.json`/`requirements.txt`

### Debugging

- **Frontend Logs**: Check Vercel deployment logs
- **Backend Logs**: Check Railway/Render service logs
- **Network Tab**: Use browser dev tools to debug API calls

## 🎉 Success!

Once deployed, your ExpenseTracker Pro will be live and accessible to users worldwide!

**Frontend URL**: `https://your-app.vercel.app`
**Backend URL**: `https://your-app.railway.app`

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify environment variables
3. Test locally first
4. Check the repository issues section
