# 🏦 AWS Expense Tracker

A comprehensive expense tracking application with intelligent transaction categorization, spending analysis, and personalized savings recommendations.

## ✨ Features

### 📊 **Interactive Data Visualization**
- **Dynamic Pie Charts**: Click categories to filter transactions
- **Spending/Earning Toggle**: Switch between expense and income views
- **Real-time Filtering**: Instant updates when selecting categories
- **Red/Green Color Coding**: Visual distinction for spending vs earning

### 🤖 **AI-Powered Analysis**
- **Machine Learning Categorization**: Automatic transaction classification
- **BERT-based Refinement**: Advanced NLP for uncategorized transactions
- **Confidence Scoring**: ML model confidence levels for predictions
- **Learning from Feedback**: Improves accuracy over time

### 💡 **Smart Recommendations**
- **Personalized Merchant Suggestions**: Category-specific alternatives
- **Savings Opportunities**: Detailed analysis with potential savings
- **Merchant Analysis**: Spending patterns and optimization tips
- **Dynamic Recommendations**: Updates based on your spending habits

### 📱 **User-Friendly Interface**
- **Sample Data**: 1000 realistic transactions for testing
- **Instruction Video**: Built-in tutorial for easy onboarding
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Glass-morphism design with smooth animations

### 📈 **Comprehensive Analytics**
- **Category Breakdown**: Detailed spending analysis by category
- **Transaction History**: Complete transaction tracking
- **Spending Trends**: Visual representation of spending patterns
- **Savings Insights**: Personalized recommendations for saving money

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ (for React frontend)
- **Python** 3.8+ (for backend services)
- **Git** (for cloning the repository)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sparsh12342/AWSExpenseTracker.git
cd AWSExpenseTracker
```

2. **Set up the React Frontend**
```bash
cd react-app
npm install
npm run dev
```

3. **Set up the Python Backend**
```bash
cd server
pip install -r requirements.txt
python app.py
```

4. **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5050

## 📋 How to Use

### 1. **Upload Your Data**
- Click "📄 Download Sample CSV" to get 1000 sample transactions
- Upload your own CSV file with columns: Date, Description, Amount, Category
- Or add transactions manually using the form

### 2. **Watch the Tutorial**
- Click "🎥 Watch Instruction Video" for a complete walkthrough
- Learn about all features and how to use them effectively

### 3. **Explore Your Data**
- **Click pie chart categories** to filter transactions
- **Toggle spending/earning** to switch between views
- **Use the Savings Analyzer** for personalized recommendations

### 4. **Get Insights**
- View detailed spending analysis by category
- Check merchant-specific recommendations
- Discover savings opportunities

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Components**: Modular React components for each feature
- **State Management**: React hooks for data management
- **Styling**: CSS-in-JS with glass-morphism design
- **Charts**: Recharts library for data visualization

### Backend (Python + Flask)
- **API Endpoints**: RESTful API for data processing
- **Machine Learning**: Scikit-learn and BERT for categorization
- **Data Processing**: Pandas for data manipulation
- **Recommendations**: Custom algorithms for savings suggestions

## 📁 Project Structure

```
AWSExpenseTracker/
├── react-app/                 # Frontend React application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── constants.ts       # Application constants
│   │   ├── types.ts          # TypeScript type definitions
│   │   └── App.tsx           # Main application component
│   ├── public/
│   │   ├── sample_transactions_1000.csv  # Sample data
│   │   └── video.mp4         # Instruction video
│   └── package.json          # Frontend dependencies
├── server/                    # Backend Python services
│   ├── app.py                # Flask API server
│   ├── spending_analyzer.py  # Spending analysis engine
│   ├── nlp_refiner.py       # NLP categorization
│   ├── bert_refiner.py      # BERT-based refinement
│   ├── savings.py           # Savings recommendations
│   └── requirements.txt     # Python dependencies
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the server directory:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=localhost
API_PORT=5050
```

### CSV Format
Your CSV file should have these columns:
- **Date**: Transaction date (YYYY-MM-DD)
- **Description**: Transaction description
- **Amount**: Transaction amount (positive for income, negative for expenses)
- **Category**: Transaction category (optional, will be auto-categorized if missing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Scikit-learn** for machine learning capabilities
- **Transformers** for BERT-based NLP
- **Recharts** for data visualization
- **React** for the frontend framework
- **Flask** for the backend API

## 📞 Support

If you encounter any issues or have questions:
1. Check the instruction video for usage guidance
2. Use the sample CSV data to test features
3. Open an issue on GitHub for bug reports
4. Create a discussion for feature requests

---

**Made with ❤️ for better financial management**