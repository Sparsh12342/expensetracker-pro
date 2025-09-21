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

@app.route("/api/upload", methods=["POST"])
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
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        
        # Convert to DataFrame
        df = pd.read_csv(stream)
        
        # Basic data processing
        if "Amount" in df.columns:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
        
        # Create basic categories if not present
        if "Category" not in df.columns:
            df["Category"] = "Uncategorized"
        
        # Generate summary
        summary = {
            "total_deposits": float(df[df["Amount"] >= 0]["Amount"].sum()) if "Amount" in df.columns else 0.0,
            "total_withdrawals": float(df[df["Amount"] < 0]["Amount"].sum()) if "Amount" in df.columns else 0.0,
            "num_deposits": int((df["Amount"] >= 0).sum()) if "Amount" in df.columns else 0,
            "num_withdrawals": int((df["Amount"] < 0).sum()) if "Amount" in df.columns else 0,
            "category_summary": summarize_by_category(df, "Category"),
            "entries_with_pred": df.to_dict("records")
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

if __name__ == "__main__":
    app.run(debug=True)
