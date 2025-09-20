#!/usr/bin/env python3
"""
Train NLP model using the actual stmt.csv data with rule-based categorization
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import FeatureUnion
from scipy import sparse
import joblib

# Add the server directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def categorize_transaction(description, amount):
    """Rule-based categorization based on common patterns in bank statements"""
    desc_lower = str(description).lower()
    # Handle comma-separated numbers
    try:
        amount = float(str(amount).replace(',', '')) if amount else 0.0
    except (ValueError, TypeError):
        amount = 0.0
    
    # Income patterns
    if any(word in desc_lower for word in ["payroll", "salary", "direct deposit", "deposit", "refund"]):
        return "Income"
    
    # Transfer patterns
    if any(word in desc_lower for word in ["transfer", "venmo", "zelle", "paypal"]):
        return "Transfers"
    
    # Dining patterns
    if any(word in desc_lower for word in [
        "starbucks", "chipotle", "mcdonalds", "pizza", "restaurant", "dining", 
        "burger", "taco", "subway", "kfc", "pizza hut", "dominos", "moe's", 
        "blaze pizza", "chick-fil-a", "popeyes", "taco bell", "five guys",
        "honeygrow", "tribos", "olde queens", "golden rail", "huey's", "scarlet pub",
        "the ale n wich", "smashville", "tacoria", "nirvanis", "schnur meyer",
        "spicy moon", "paris baguette", "anita gelato", "mexi cafe", "thai kitchen",
        "cook cafe", "r u hungry", "hidden grounds", "woody's cafe", "veganized",
        "mr. tacos", "the baked bear", "shokudo", "evelyns", "n thai palace",
        "playa bowls", "insomnia cookies", "tuta ice cream", "cafe west", "16 handles"
    ]):
        return "Dining"
    
    # Shopping patterns
    if any(word in desc_lower for word in [
        "amazon", "target", "walmart", "macy's", "best buy", "costco", "marshalls",
        "ulta", "sephora", "forever21", "foot locker", "party city", "zara",
        "box lunch", "lids", "dollartree", "hmart", "delta", "perfume club",
        "new hair culture", "proskatenj", "sp nj skateshop", "fan treaspro"
    ]):
        return "Shopping"
    
    # Groceries patterns
    if any(word in desc_lower for word in [
        "grocery", "whole foods", "trader joe", "safeway", "kroger", "shoprite",
        "stop & shop", "acme", "wal-mart", "wal mart", "costco", "butler food",
        "knights deli", "easton deli", "jaike's fine foods", "dollar brunswick"
    ]):
        return "Groceries"
    
    # Transportation patterns
    if any(word in desc_lower for word in [
        "uber", "lyft", "gas", "fuel", "metro", "subway", "toll", "parking",
        "exxon", "shell", "bp", "chevron", "lukoil", "njt", "mta", "parkmobile",
        "veo", "jetblue", "delta", "flight", "airline"
    ]):
        return "Transportation"
    
    # Health patterns
    if any(word in desc_lower for word in [
        "pharmacy", "cvs", "walgreens", "doctor", "dental", "medical", "health",
        "gym", "fitness", "hospital", "clinic", "drug", "medicine"
    ]):
        return "Health"
    
    # Entertainment patterns
    if any(word in desc_lower for word in [
        "netflix", "spotify", "hulu", "prime video", "cinema", "movie", "theater",
        "concert", "entertainment", "rutgers cinema", "amc", "yestercades"
    ]):
        return "Entertainment"
    
    # Utilities patterns
    if any(word in desc_lower for word in [
        "electric", "water", "gas bill", "utility", "internet", "wifi", "phone",
        "cable", "new brunswick municipal", "canteen vending"
    ]):
        return "Utilities"
    
    # Education patterns
    if any(word in desc_lower for word in [
        "rutgers", "university", "college", "school", "tuition", "education",
        "bookstore", "oak hall", "graduation", "cap gown"
    ]):
        return "Education"
    
    # Subscriptions patterns
    if any(word in desc_lower for word in [
        "subscription", "monthly", "annual", "recurring", "openai", "chatgpt",
        "linkedin", "premium", "membership"
    ]):
        return "Subscriptions"
    
    # Fees patterns
    if any(word in desc_lower for word in [
        "fee", "charge", "penalty", "overdraft", "atm", "service charge"
    ]):
        return "Fees"
    
    # Travel patterns
    if any(word in desc_lower for word in [
        "hotel", "airbnb", "travel", "vacation", "trip", "booking", "expedia"
    ]):
        return "Travel"
    
    # Housing patterns
    if any(word in desc_lower for word in [
        "rent", "landlord", "lease", "mortgage", "housing", "apartment"
    ]):
        return "Housing"
    
    # Default to uncategorized
    return "Uncategorized"

def train_model_from_csv(csv_path):
    """Train the NLP model using the CSV data"""
    
    # Read the CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} transactions from {csv_path}")
    
    # Clean the data
    df = df.dropna(subset=['Description', 'Amount'])
    df = df[df['Description'].str.strip() != '']
    
    # Apply rule-based categorization
    print("Applying rule-based categorization...")
    df['Category'] = df.apply(lambda row: categorize_transaction(row['Description'], row['Amount']), axis=1)
    
    # Show category distribution
    category_counts = df['Category'].value_counts()
    print("\nCategory distribution:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} transactions")
    
    # Prepare training data
    descriptions = df['Description'].fillna("").astype(str)
    # Handle comma-separated amounts
    amounts = df['Amount'].astype(str).str.replace(',', '').astype(float, errors='ignore').fillna(0.0)
    categories = df['Category']
    
    # Create vectorizer
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_features=10000
    )
    
    # Fit vectorizer
    X_text = vectorizer.fit_transform(descriptions)
    
    # Create amount features
    def amount_bucket(x):
        v = x.values.reshape(-1, 1)
        bins = np.digitize(v, [-100, -25, -5, 5, 25, 100])
        n = v.shape[0]; k = 8
        rows = np.repeat(np.arange(n), 1)
        cols = bins.flatten().clip(0, k-1)
        data = np.ones(n)
        return sparse.csr_matrix((data, (rows, cols)), shape=(n, k))
    
    X_amount = amount_bucket(amounts)
    
    # Combine features
    X = sparse.hstack([X_text, X_amount], format="csr")
    y = categories.values
    
    # Train classifier
    print("\nTraining classifier...")
    clf = SGDClassifier(loss="log_loss", random_state=42, max_iter=1000)
    clf.fit(X, y)
    
    # Save the model
    model_dir = os.path.join(os.path.dirname(csv_path), "models")
    os.makedirs(model_dir, exist_ok=True)
    
    vec_path = os.path.join(model_dir, "tfidf.pkl")
    clf_path = os.path.join(model_dir, "sgd.pkl")
    labels_path = os.path.join(model_dir, "labels.pkl")
    
    joblib.dump(vectorizer, vec_path)
    joblib.dump(clf, clf_path)
    joblib.dump(list(category_counts.index), labels_path)
    
    print(f"\nModel saved to {model_dir}")
    print("Files created:")
    print(f"  - {vec_path}")
    print(f"  - {clf_path}")
    print(f"  - {labels_path}")
    
    # Test the model
    print("\nTesting model accuracy...")
    predictions = clf.predict(X)
    accuracy = (predictions == y).mean()
    print(f"Training accuracy: {accuracy:.2%}")
    
    return vectorizer, clf, list(category_counts.index)

if __name__ == "__main__":
    # Train using the stmt.csv file
    csv_path = os.path.join(os.path.dirname(__file__), "..", "stmt.csv")
    if os.path.exists(csv_path):
        train_model_from_csv(csv_path)
    else:
        print(f"CSV file not found at {csv_path}")
        print("Please make sure stmt.csv is in the project root directory")
