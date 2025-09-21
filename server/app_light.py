from flask import Flask, request, jsonify
from flask_cors import CORS
import io, csv
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for deployment

# Health check endpoint for Vercel
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "message": "ExpenseTracker Pro API is running (Light Version)"})

# Root endpoint
@app.route("/")
def root():
    return jsonify({
        "message": "ExpenseTracker Pro API", 
        "endpoints": [
            "/health", "/upload-csv", "/api/categorize", 
            "/nlp/labels", "/nlp/refine", "/nlp/feedback", 
            "/savings/suggestions"
        ]
    })

def summarize_by_category(df: pd.DataFrame, cat_col: str):
    # Ensure numeric amounts
    df["Amount"] = pd.to_numeric(df.get("Amount", 0), errors="coerce").fillna(0.0)

    groups = df.groupby(cat_col)["Amount"]
    out = []
    for cat, series in groups:
        total = float(series.sum())
        deposits = float(series[series >= 0].sum())
        withdrawals = float(series[series < 0].sum())
        out.append({
            "Category": str(cat),
            "TransactionCount": int(series.shape[0]),
            "TotalAmount": total,
            "Withdrawals": withdrawals,
            "Deposits": deposits,
        })
    return out

@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith(".csv"):
            return jsonify({"error": "Please upload a CSV file"}), 400
        
        # Read CSV data
        csv_content = file.stream.read().decode("UTF8")
        stream = io.StringIO(csv_content, newline=None)
        
        # Convert to DataFrame
        df = pd.read_csv(stream)
        
        # Basic data processing
        if "Amount" in df.columns:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
        
        # Create basic categories if not present
        if "Category" not in df.columns:
            df["Category"] = "Uncategorized"
        
        # Add basic categorization logic
        if "Description" in df.columns:
            for idx, row in df.iterrows():
                if df.loc[idx, "Category"] == "Uncategorized":
                    description = str(row.get("Description", "")).lower()
                    amount = float(row.get("Amount", 0))
                    
                    # Simple rule-based categorization
                    if "grocery" in description or "food" in description or "restaurant" in description:
                        df.loc[idx, "Category"] = "Food & Dining"
                    elif "gas" in description or "fuel" in description or "gasoline" in description:
                        df.loc[idx, "Category"] = "Transportation"
                    elif "rent" in description or "mortgage" in description or "housing" in description:
                        df.loc[idx, "Category"] = "Housing"
                    elif "salary" in description or "payroll" in description or "income" in description:
                        df.loc[idx, "Category"] = "Income"
                    elif amount > 0:
                        df.loc[idx, "Category"] = "Income"
                    else:
                        df.loc[idx, "Category"] = "Other Expenses"
        
        # Generate summary
        summary = {
            "total_deposits": float(df[df["Amount"] >= 0]["Amount"].sum()) if "Amount" in df.columns else 0.0,
            "total_withdrawals": float(df[df["Amount"] < 0]["Amount"].sum()) if "Amount" in df.columns else 0.0,
            "num_deposits": int((df["Amount"] >= 0).sum()) if "Amount" in df.columns else 0,
            "num_withdrawals": int((df["Amount"] < 0).sum()) if "Amount" in df.columns else 0,
            "category_summary": summarize_by_category(df, "Category"),
            "entries_with_pred": [
                {
                    **row,
                    "PredictedCategory": row.get("Category", "Uncategorized")
                }
                for row in df.to_dict("records")
            ]
        }
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

@app.route("/api/categorize", methods=["POST"])
def categorize_transactions():
    try:
        data = request.get_json()
        transactions = data.get("transactions", [])
        
        # Simple categorization logic (without ML)
        categorized = []
        for transaction in transactions:
            description = transaction.get("Description", "").lower()
            amount = float(transaction.get("Amount", 0))
            
            # Simple rule-based categorization
            if "grocery" in description or "food" in description or "restaurant" in description:
                category = "Food & Dining"
            elif "gas" in description or "fuel" in description or "gasoline" in description:
                category = "Transportation"
            elif "rent" in description or "mortgage" in description or "housing" in description:
                category = "Housing"
            elif "salary" in description or "payroll" in description or "income" in description:
                category = "Income"
            elif amount > 0:
                category = "Income"
            else:
                category = "Other Expenses"
            
            transaction["Category"] = category
            categorized.append(transaction)
        
        return jsonify({"categorized_transactions": categorized})
        
    except Exception as e:
        return jsonify({"error": f"Error categorizing transactions: {str(e)}"}), 500

# NLP endpoints for frontend compatibility
@app.route("/nlp/labels", methods=["GET"])
def nlp_get_labels():
    """Return available category labels"""
    labels = [
        "Food & Dining", "Transportation", "Housing", "Entertainment", 
        "Shopping", "Healthcare", "Utilities", "Insurance", "Education",
        "Transfers", "Income", "Fees", "Travel", "Education", "Uncategorized"
    ]
    return jsonify({"labels": labels})

@app.route("/nlp/refine", methods=["POST"])
def nlp_refine():
    """Refine uncategorized transactions with basic rules"""
    try:
        data = request.get_json()
        rows = data.get("rows", [])
        
        refined = []
        for row in rows:
            description = str(row.get("Description", "")).lower()
            amount = float(row.get("Amount", 0))
            
            # Simple rule-based categorization
            if "grocery" in description or "food" in description or "restaurant" in description:
                category = "Food & Dining"
            elif "gas" in description or "fuel" in description or "gasoline" in description:
                category = "Transportation"
            elif "rent" in description or "mortgage" in description or "housing" in description:
                category = "Housing"
            elif "salary" in description or "payroll" in description or "income" in description:
                category = "Income"
            elif amount > 0:
                category = "Income"
            else:
                category = "Other Expenses"
            
            refined.append({
                **row,
                "PredictedCategory": category
            })
        
        return jsonify(refined)
        
    except Exception as e:
        return jsonify({"error": f"Error refining transactions: {str(e)}"}), 500

@app.route("/nlp/feedback", methods=["POST"])
def nlp_feedback():
    """Accept feedback for learning (simplified version)"""
    try:
        data = request.get_json()
        # In a full implementation, this would update the ML model
        # For now, just acknowledge receipt
        return jsonify({"message": "Feedback received", "status": "success"})
    except Exception as e:
        return jsonify({"error": f"Error processing feedback: {str(e)}"}), 500

@app.route("/savings/suggestions", methods=["POST"])
def savings_suggestions():
    """Generate savings suggestions (simplified version)"""
    try:
        data = request.get_json()
        categories = data.get("categories", [])
        merchants = data.get("merchants", [])
        
        # Generate basic savings suggestions
        suggestions = []
        
        for category in categories[:3]:  # Limit to top 3 categories
            suggestions.append({
                "category": category,
                "suggestion": f"Consider reducing {category} expenses by 10-15%",
                "potential_savings": 50.0,
                "confidence": 0.7
            })
        
        return jsonify({
            "suggestions": suggestions,
            "total_potential_savings": sum(s["potential_savings"] for s in suggestions)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error generating suggestions: {str(e)}"}), 500

if __name__ == "__main__":
    print("🏦 Starting Expense Tracker Backend Server...")
    print("📍 Server will be available at: http://127.0.0.1:5050")
    print("🔗 Health check: http://127.0.0.1:5050/health")
    print("=" * 50)
    
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=True
    )
