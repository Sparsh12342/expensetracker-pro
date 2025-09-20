# 🚀 Deployment Guide - ExpenseTracker Pro

This guide will help you deploy your ExpenseTracker Pro application to production using Vercel.

## 📋 Overview

The application is configured for **monorepo deployment on Vercel**:
- **Frontend**: React + TypeScript (Vercel Static Build)
- **Backend**: Python + Flask (Vercel Serverless Functions)

## 🎯 Deploy Both Frontend & Backend to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. **Click "New Project"**
3. **Import your repository**: `https://github.com/Sparsh12342/expensetracker-pro`
4. **Vercel will automatically detect both applications**:
   - **Frontend**: React app in `react-app/` directory
   - **Backend**: Python Flask app in `server/` directory
5. **Configure Project** (if needed):
   - **Framework Preset**: Vite (for frontend)
   - **Root Directory**: Leave as root (for monorepo)
6. **Click "Deploy"** - Vercel will build and deploy both apps!

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project root
cd /path/to/expensetracker-pro

# Login to Vercel
vercel login

# Deploy the entire project
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: expensetracker-pro
# - In which directory is your code located? ./
```

## ✅ Automatic Configuration

The application is pre-configured for Vercel deployment:

- **Frontend** automatically serves from the root URL
- **Backend API** automatically available at `/api/*` routes
- **CORS** configured to allow frontend-backend communication
- **Environment detection** handles local vs production automatically

## 📝 Environment Variables

No environment variables are required! The application automatically:
- Uses `/api` for backend calls in production
- Uses `http://localhost:5050` for local development
- Configures CORS automatically

## 🔍 Testing Your Deployment

1. **Check Frontend**: Visit your Vercel URL (e.g., `https://expensetracker-pro.vercel.app`)
2. **Test API**: Visit `https://your-app.vercel.app/api/health`
3. **Upload Sample Data**: Use the sample CSV to test functionality
4. **Verify Features**: Test categorization, filtering, and recommendations

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**: Check that all dependencies are in `package.json`/`requirements.txt`
2. **API Not Working**: Check Vercel function logs in the dashboard
3. **CORS Errors**: Should be automatically handled by the configuration

### Debugging

- **Vercel Logs**: Check deployment logs in Vercel dashboard
- **Function Logs**: Check serverless function logs for backend issues
- **Network Tab**: Use browser dev tools to debug API calls

## 🎉 Success!

Once deployed, your ExpenseTracker Pro will be live and accessible to users worldwide!

**Application URL**: `https://your-app.vercel.app`
- **Frontend**: Served from root
- **Backend API**: Available at `/api/*` routes

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify environment variables
3. Test locally first
4. Check the repository issues section
