from flask import Flask, request, jsonify
from flask_cors import CORS
import io, csv
import pandas as pd
import numpy as np

# Handle both relative and absolute imports
try:
    # Try relative imports first (when running as package)
    from .nlp_refiner import predict_descriptions, learn_feedback, labels as nlp_labels
    from .savings import get_savings_suggestions
    from .machinelearningclassification import predict_categories
    from .spending_analyzer import SpendingAnalyzer
    from .web_scraper import WebScraper
    # Temporarily disable BERT for faster Vercel deployment
    # from .bert_refiner import refine_uncategorized_with_bert, get_bert_model_info
    BERT_AVAILABLE = False
except ImportError:
    # Fall back to absolute imports (when running directly)
    from nlp_refiner import predict_descriptions, learn_feedback, labels as nlp_labels
    from savings import get_savings_suggestions
    from machinelearningclassification import predict_categories
    from spending_analyzer import SpendingAnalyzer
    from web_scraper import WebScraper
    # Temporarily disable BERT for faster Vercel deployment
    # from bert_refiner import refine_uncategorized_with_bert, get_bert_model_info
    BERT_AVAILABLE = False

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for Vercel deployment

# Health check endpoint for Vercel
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "message": "ExpenseTracker Pro API is running"})

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

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/bert/info")
def bert_info():
    """Get information about the BERT model"""
    try:
        if BERT_AVAILABLE:
            info = get_bert_model_info()
        else:
            info = {"status": "BERT temporarily disabled for faster deployment"}
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/upload-csv")
def upload_csv():
    """
    Accepts a CSV with columns like: Date, Description, Amount, Category
    Runs ML to predict categories and returns:
      - category_summary (based on ML predictions)
      - entries_with_pred (rows + PredictedCategory)
    """
    if "file" not in request.files:
        return jsonify({"error": "file field required"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)

    if not rows:
        return jsonify({"category_summary": [], "entries_with_pred": []})

    # Detect header (very lightweight check)
    header = rows[0]
    lower = [str(h or "").strip().lower() for h in header]
    looks_like_header = len(lower) >= 3 and ("date" in lower[0] and "amount" in lower[2])

    data_rows = rows[1:] if looks_like_header else rows
    columns = header if looks_like_header else ["Date", "Description", "Amount", "Category"]

    df = pd.DataFrame(data_rows, columns=columns).fillna("")

    # Run your ML predictions
    preds = predict_categories(df)  # must be length == len(df)
    df["PredictedCategory"] = preds.astype(str).fillna("Uncategorized")

    # Apply BERT refinement to uncategorized transactions
    print("🤖 Applying BERT refinement to uncategorized transactions...")
    if BERT_AVAILABLE:
        df = refine_uncategorized_with_bert(df, confidence_threshold=0.15)
    # Skip BERT refinement for faster deployment

    # Build ML-based summary
    category_summary = summarize_by_category(df, "PredictedCategory")

    # Return also per-row predictions (handy for a table)
    entries_with_pred = df[["Date", "Description", "Amount", "PredictedCategory"]].to_dict(orient="records")
    
    # Add confidence scores if available
    if "Confidence" in df.columns:
        for i, entry in enumerate(entries_with_pred):
            entry["Confidence"] = df.iloc[i].get("Confidence", None)

    return jsonify({
        "category_summary": category_summary,
        "entries_with_pred": entries_with_pred,
    })

@app.post("/nlp/refine")
def nlp_refine():
    """
    Body: { rows: [{Description, Amount}], threshold?: 0.45 }
    Returns: [{ PredictedCategory, Confidence }]
    """
    payload = request.get_json(silent=True) or {}
    rows = payload.get("rows", [])
    threshold = float(payload.get("threshold", 0.45))

    df = pd.DataFrame(rows).fillna("")
    
    # First try the existing NLP refiner
    out = predict_descriptions(df)  # PredictedCategory + Confidence
    
    # If below threshold -> keep as 'Uncategorized'
    below = out["Confidence"] < threshold
    out.loc[below, "PredictedCategory"] = "Uncategorized"
    
    # Apply BERT refinement to remaining uncategorized transactions
    if below.any():
        print("🤖 Applying BERT refinement to low-confidence predictions...")
        if BERT_AVAILABLE:
            out = refine_uncategorized_with_bert(out, confidence_threshold=0.15)
        # Skip BERT refinement for faster deployment

    return jsonify(out.to_dict(orient="records"))

@app.post("/nlp/feedback")
def nlp_feedback():
    """
    Body: { samples: [{Description, Amount, CorrectCategory}] }
    Updates the online model (partial_fit) and persists artifacts.
    """
    payload = request.get_json(silent=True) or {}
    samples = pd.DataFrame(payload.get("samples", [])).fillna("")
    if samples.empty:
        return jsonify({"updated": 0})
    learn_feedback(samples)
    return jsonify({"updated": int(samples.shape[0])})

@app.get("/nlp/labels")
def nlp_get_labels():
    return jsonify({"labels": nlp_labels()})

@app.post("/savings/suggestions")
def savings_suggestions():
    try:
        payload = request.get_json(silent=True) or {}
        categories = payload.get("categories", []) or []
        merchants = payload.get("merchants", []) or []
        max_items = int(payload.get("max_items", 12))
        items = get_savings_suggestions(categories, merchants, max_items=max_items)
        return jsonify({"items": items})
    except Exception as e:
        print("savings error:", e)
        return jsonify({"items": []})

@app.route("/savings/analyze", methods=["POST"])
def analyze_spending():
    """Analyze spending patterns and find savings opportunities"""
    try:
        payload = request.get_json(silent=True) or {}
        transactions = payload.get("transactions", [])
        
        print(f"Received {len(transactions)} transactions for analysis")
        print(f"Sample transaction: {transactions[0] if transactions else 'None'}")
        
        if not transactions:
            return jsonify({"error": "No transactions provided"})
        
        # Convert to DataFrame
        df = pd.DataFrame(transactions)
        print(f"DataFrame shape: {df.shape}")
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"DataFrame head:\n{df.head()}")
        
        # Initialize analyzer and scraper
        analyzer = SpendingAnalyzer()
        scraper = WebScraper()
        
        # Analyze spending patterns
        spending_analysis = analyzer.analyze_spending_patterns(df)
        print(f"Spending analysis result: {spending_analysis}")
        
        # Generate savings report
        savings_report = analyzer.generate_savings_report(spending_analysis)
        print(f"Savings report result: {savings_report}")
        
        # Get comprehensive savings with web scraping
        comprehensive_savings = scraper.get_comprehensive_savings(spending_analysis)
        print(f"Comprehensive savings result: {comprehensive_savings}")
        
        # Combine results and convert numpy types to native Python types
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif hasattr(obj, 'tolist'):  # numpy array
                return obj.tolist()
            else:
                return obj
        
        result = {
            "spending_analysis": convert_numpy_types(spending_analysis),
            "savings_report": convert_numpy_types(savings_report),
            "comprehensive_savings": convert_numpy_types(comprehensive_savings),
            "total_potential_savings": float(savings_report.get("total_potential_savings", 0) + comprehensive_savings.get("total_potential_savings", 0))
        }
        
        return jsonify(result)
        
    except Exception as e:
        print("Spending analysis error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)})

@app.route("/savings/find-alternatives", methods=["POST"])
def find_alternatives():
    """Find cheaper alternatives for specific products/merchants"""
    try:
        payload = request.get_json(silent=True) or {}
        product_name = payload.get("product_name", "")
        current_price = float(payload.get("current_price", 0))
        merchant = payload.get("merchant", "")
        
        if not product_name or current_price <= 0:
            return jsonify({"error": "Product name and current price required"})
        
        scraper = WebScraper()
        alternatives = scraper.find_cheaper_alternatives(product_name, current_price)
        
        return jsonify(alternatives)
        
    except Exception as e:
        print("Alternatives search error:", e)
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Run as a script (useful during development)
    app.run(host="127.0.0.1", port=5050, debug=False)
