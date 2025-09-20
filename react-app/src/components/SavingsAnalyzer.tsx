import React, { useState, useEffect } from "react";
import DetailedSavingsPage from "./DetailedSavingsPage";

interface Transaction {
  Date: string;
  Description: string;
  Amount: number;
  Category?: string;
}

interface SavingsOpportunity {
  category?: string;
  merchant?: string;
  current_spending: number;
  transaction_count: number;
  alternatives: Alternative[];
  potential_savings: number;
}

interface Alternative {
  alternative: string;
  estimated_savings: number;
  savings_percentage: number;
  reason: string;
  category: string;
}

interface SpendingAnalysis {
  top_categories: Record<string, any>;
  merchant_analysis: Array<{
    merchant: string;
    total_spent: number;
    transaction_count: number;
    avg_amount: number;
    sample_descriptions: string[];
  }>;
  total_expenses: number;
  avg_transaction: number;
  total_transactions: number;
}

interface DetailedRecommendation {
  merchant: string;
  current_spending: number;
  transaction_count: number;
  avg_per_visit: number;
  alternatives: string[];
  potential_savings: number;
  savings_percentage: number;
  reasoning: string;
  specific_suggestion: string;
  sample_descriptions: string[];
}

interface SavingsReport {
  total_potential_savings: number;
  savings_opportunities: SavingsOpportunity[];
  detailed_recommendations: DetailedRecommendation[];
  summary: {
    total_expenses: number;
    total_potential_savings: number;
    savings_percentage: number;
    opportunities_count: number;
    detailed_recommendations_count: number;
  };
}

interface ComprehensiveSavings {
  total_potential_savings: number;
  savings_breakdown: SavingsOpportunity[];
  deals_found: any[];
  recommendations: string[];
}

interface SavingsAnalyzerProps {
  transactions: Transaction[];
  onClose: () => void;
  onCategoryClick?: (category: string) => void;
}

const SavingsAnalyzer: React.FC<SavingsAnalyzerProps> = ({
  transactions,
  onClose,
  onCategoryClick,
}) => {
  // Group transactions by their actual categories for reliable filtering
  const transactionsByCategory = React.useMemo(() => {
    const grouped: Record<string, Transaction[]> = {};
    transactions.forEach((transaction) => {
      const category = transaction.Category || "Uncategorized";
      if (!grouped[category]) {
        grouped[category] = [];
      }
      grouped[category].push(transaction);
    });
    return grouped;
  }, [transactions]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysis, setAnalysis] = useState<{
    spending_analysis: SpendingAnalysis;
    savings_report: SavingsReport;
    comprehensive_savings: ComprehensiveSavings;
    total_potential_savings: number;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showDetailedPage, setShowDetailedPage] = useState(false);

  const analyzeSpending = async () => {
    console.log("Starting analysis with transactions:", transactions.length);
    setLoading(true);
    setProgress(0);
    setError(null);

    const requestData = {
      transactions: transactions.map((t) => ({
        Date: t.Date,
        Description: t.Description,
        Amount: t.Amount,
      })),
    };

    console.log("Sending request to backend:", requestData);
    setProgress(20);

    try {
      const response = await fetch("http://localhost:5050/savings/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      console.log("Response status:", response.status);
      console.log("Response ok:", response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Response error text:", errorText);
        throw new Error(
          `HTTP error! status: ${response.status} - ${errorText}`
        );
      }

      setProgress(70);
      const data = await response.json();
      console.log("Savings analysis response:", data);
      setProgress(100);
      console.log("Setting analysis data:", data);
      setAnalysis(data);
    } catch (err) {
      console.error("Analysis error:", err);
      setError(
        err instanceof Error ? err.message : "Failed to analyze spending"
      );
    } finally {
      setLoading(false);
      console.log("Analysis complete, loading set to false");
    }
  };

  useEffect(() => {
    console.log("SavingsAnalyzer mounted with transactions:", transactions);
    if (transactions.length > 0) {
      analyzeSpending();
    }
  }, [transactions]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const cardStyle: React.CSSProperties = {
    border: "2px solid #333",
    borderRadius: 16,
    padding: 20,
    background: "#fff",
    boxShadow: "0 4px 16px rgba(0, 0, 0, 0.1)",
    marginBottom: 20,
    minHeight: "400px",
    color: "#000",
  };

  const headerStyle: React.CSSProperties = {
    margin: "0 0 20px 0",
    fontSize: 24,
    fontWeight: 600,
    color: "#333",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  };

  const buttonStyle: React.CSSProperties = {
    background: "#007bff",
    border: "1px solid #007bff",
    borderRadius: 8,
    padding: "8px 16px",
    color: "white",
    cursor: "pointer",
    fontSize: 14,
  };

  const loadingStyle: React.CSSProperties = {
    textAlign: "center",
    padding: "40px 20px",
    color: "#333",
    fontSize: 16,
  };

  const errorStyle: React.CSSProperties = {
    textAlign: "center",
    padding: "40px 20px",
    color: "#ff6b6b",
    fontSize: 16,
  };

  console.log(
    "SavingsAnalyzer render - loading:",
    loading,
    "error:",
    error,
    "analysis:",
    !!analysis
  );

  if (loading) {
    return (
      <div style={cardStyle}>
        <div style={headerStyle}>
          <span>💰 Savings Analysis</span>
          <button style={buttonStyle} onClick={onClose}>
            ✕ Close
          </button>
        </div>
        <div style={loadingStyle}>
          🔍 Analyzing your spending patterns and finding savings
          opportunities...
        </div>

        {/* Back Button for Loading State */}
        <div style={{ textAlign: "center", marginTop: 20 }}>
          <button
            style={{
              ...buttonStyle,
              background: "linear-gradient(135deg, #ff6b6b, #ee5a52)",
              color: "white",
              fontWeight: "600",
              padding: "12px 24px",
              fontSize: "16px",
            }}
            onClick={onClose}
          >
            ← Back to Main View
          </button>
        </div>

        {/* Progress Bar */}
        <div style={{ marginTop: 20, width: "100%" }}>
          <div
            style={{
              width: "100%",
              height: 8,
              backgroundColor: "#e0e0e0",
              borderRadius: 4,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progress}%`,
                height: "100%",
                backgroundColor: "#4CAF50",
                borderRadius: 4,
                transition: "width 0.3s ease",
              }}
            />
          </div>
          <div
            style={{
              textAlign: "center",
              marginTop: 8,
              fontSize: 14,
              color: "#666",
            }}
          >
            {progress}% Complete
          </div>
        </div>
        <div
          style={{
            marginTop: 20,
            padding: 10,
            background: "#f8f9fa",
            borderRadius: 8,
          }}
        >
          <strong>Debug Info:</strong>
          <br />
          Transactions: {transactions.length}
          <br />
          Loading: {loading.toString()}
          <br />
          Error: {error || "None"}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={cardStyle}>
        <div style={headerStyle}>
          <span>💰 Savings Analysis</span>
          <button style={buttonStyle} onClick={onClose}>
            ✕ Close
          </button>
        </div>
        <div style={errorStyle}>❌ Error: {error}</div>
        <div
          style={{
            display: "flex",
            gap: 10,
            justifyContent: "center",
            marginTop: 20,
          }}
        >
          <button style={buttonStyle} onClick={analyzeSpending}>
            Try Again
          </button>
          <button
            style={{
              ...buttonStyle,
              background: "linear-gradient(135deg, #ff6b6b, #ee5a52)",
              color: "white",
              fontWeight: "600",
              padding: "12px 24px",
              fontSize: "16px",
            }}
            onClick={onClose}
          >
            ← Back to Main View
          </button>
        </div>
        <div
          style={{
            marginTop: 20,
            padding: 10,
            background: "#f8f9fa",
            borderRadius: 8,
          }}
        >
          <strong>Debug Info:</strong>
          <br />
          Transactions: {transactions.length}
          <br />
          Loading: {loading.toString()}
          <br />
          Error: {error}
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div style={cardStyle}>
        <div style={headerStyle}>
          <span>💰 Savings Analysis</span>
          <button style={buttonStyle} onClick={onClose}>
            ✕ Close
          </button>
        </div>
        <div style={loadingStyle}>
          No analysis available. Click "Analyze Spending" to get started.
        </div>
        <div
          style={{
            display: "flex",
            gap: 10,
            justifyContent: "center",
            marginTop: 20,
          }}
        >
          <button style={buttonStyle} onClick={analyzeSpending}>
            Analyze Spending
          </button>
          <button
            style={{
              ...buttonStyle,
              background: "linear-gradient(135deg, #ff6b6b, #ee5a52)",
              color: "white",
              fontWeight: "600",
              padding: "12px 24px",
              fontSize: "16px",
            }}
            onClick={onClose}
          >
            ← Back to Main View
          </button>
        </div>
        <div
          style={{
            marginTop: 20,
            padding: 10,
            background: "#f8f9fa",
            borderRadius: 8,
          }}
        >
          <strong>Debug Info:</strong>
          <br />
          Transactions: {transactions.length}
          <br />
          Loading: {loading.toString()}
          <br />
          Error: {error || "None"}
        </div>
      </div>
    );
  }

  // Check if analysis has meaningful data
  const hasData =
    analysis &&
    (analysis.spending_analysis?.total_expenses > 0 ||
      analysis.savings_report?.savings_opportunities?.length > 0 ||
      analysis.savings_report?.detailed_recommendations?.length > 0 ||
      analysis.comprehensive_savings?.recommendations?.length > 0 ||
      analysis.total_potential_savings > 0);

  console.log("hasData check:", {
    hasAnalysis: !!analysis,
    totalExpenses: analysis?.spending_analysis?.total_expenses,
    savingsOpportunities:
      analysis?.savings_report?.savings_opportunities?.length,
    detailedRecommendations:
      analysis?.savings_report?.detailed_recommendations?.length,
    comprehensiveRecommendations:
      analysis?.comprehensive_savings?.recommendations?.length,
    totalPotentialSavings: analysis?.total_potential_savings,
    hasData,
  });

  return (
    <div style={cardStyle}>
      <div style={headerStyle}>
        <span>💰 Savings Analysis</span>
        <button style={buttonStyle} onClick={onClose}>
          ✕ Close
        </button>
      </div>

      {!hasData ? (
        <div
          style={{
            padding: "20px",
            textAlign: "center",
            background: "#f8f9fa",
            borderRadius: "8px",
            marginBottom: "20px",
          }}
        >
          <h3 style={{ color: "#333", marginBottom: "10px" }}>
            ⚠️ No Analysis Data
          </h3>
          <p style={{ color: "#666", marginBottom: "15px" }}>
            The analysis returned empty results. This might be because:
          </p>
          <ul
            style={{ textAlign: "left", color: "#666", marginBottom: "15px" }}
          >
            <li>The spending analyzer needs more transaction data</li>
            <li>There was an issue with the backend analysis</li>
            <li>The transactions don't match expected patterns</li>
          </ul>
          <div
            style={{
              background: "#e9ecef",
              padding: "10px",
              borderRadius: "4px",
              fontSize: "12px",
              fontFamily: "monospace",
            }}
          >
            <strong>Debug Info:</strong>
            <br />
            Total Expenses: {analysis?.spending_analysis?.total_expenses || 0}
            <br />
            Opportunities:{" "}
            {analysis?.savings_report?.savings_opportunities?.length || 0}
            <br />
            Recommendations:{" "}
            {analysis?.savings_report?.detailed_recommendations?.length || 0}
          </div>
        </div>
      ) : (
        <div
          style={{
            padding: "20px",
            textAlign: "center",
            background: "#e8f5e8",
            borderRadius: "8px",
            marginBottom: "20px",
          }}
        >
          <h3 style={{ color: "#2d5a2d", marginBottom: "10px" }}>
            ✅ Analysis Complete!
          </h3>
          <p style={{ color: "#4a6741" }}>
            Found spending insights and savings opportunities.
          </p>
        </div>
      )}

      {/* Summary */}
      <div style={{ marginBottom: 30 }}>
        <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>📊 Summary</h3>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: 15,
          }}
        >
          <div
            style={{
              background: "rgba(255, 255, 255, 0.1)",
              padding: 15,
              borderRadius: 8,
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Total Expenses
            </div>
            <div style={{ fontSize: 20, fontWeight: 600, color: "#ff6b6b" }}>
              {formatCurrency(analysis.spending_analysis.total_expenses)}
            </div>
          </div>
          <div
            style={{
              background: "rgba(255, 255, 255, 0.1)",
              padding: 15,
              borderRadius: 8,
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Potential Savings
            </div>
            <div style={{ fontSize: 20, fontWeight: 600, color: "#51cf66" }}>
              {formatCurrency(analysis.total_potential_savings)}
            </div>
          </div>
          <div
            style={{
              background: "rgba(255, 255, 255, 0.1)",
              padding: 15,
              borderRadius: 8,
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Savings %
            </div>
            <div style={{ fontSize: 20, fontWeight: 600, color: "#51cf66" }}>
              {(
                (analysis.total_potential_savings /
                  analysis.spending_analysis.total_expenses) *
                100
              ).toFixed(1)}
              %
            </div>
          </div>
          <div
            style={{
              background: "rgba(255, 255, 255, 0.1)",
              padding: 15,
              borderRadius: 8,
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Opportunities
            </div>
            <div style={{ fontSize: 20, fontWeight: 600, color: "#87CEEB" }}>
              {analysis.savings_report.summary.opportunities_count}
            </div>
          </div>
        </div>
      </div>

      {/* Actual Transaction Categories (More Reliable) */}
      <div style={{ marginBottom: 30 }}>
        <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>
          📊 Your Actual Transaction Categories
        </h3>
        <div style={{ display: "grid", gap: 10 }}>
          {Object.entries(transactionsByCategory)
            .sort(([, a], [, b]) => {
              const totalA = a.reduce((sum, t) => sum + Math.abs(t.Amount), 0);
              const totalB = b.reduce((sum, t) => sum + Math.abs(t.Amount), 0);
              return totalB - totalA;
            })
            .slice(0, 8)
            .map(([category, categoryTransactions]) => {
              const totalSpent = categoryTransactions.reduce(
                (sum, t) => sum + Math.abs(t.Amount),
                0
              );
              const avgAmount = totalSpent / categoryTransactions.length;

              return (
                <div
                  key={category}
                  style={{
                    background: "rgba(255, 255, 255, 0.1)",
                    padding: 15,
                    borderRadius: 8,
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    cursor: onCategoryClick ? "pointer" : "default",
                    transition: "all 0.2s ease",
                    border: "2px solid transparent",
                  }}
                  onClick={() => {
                    if (onCategoryClick) {
                      onCategoryClick(category);
                      onClose(); // Close the savings analyzer after clicking
                    }
                  }}
                  onMouseEnter={(e) => {
                    if (onCategoryClick) {
                      e.currentTarget.style.background =
                        "rgba(255, 255, 255, 0.2)";
                      e.currentTarget.style.border = "2px solid #87CEEB";
                      e.currentTarget.style.transform = "translateY(-2px)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (onCategoryClick) {
                      e.currentTarget.style.background =
                        "rgba(255, 255, 255, 0.1)";
                      e.currentTarget.style.border = "2px solid transparent";
                      e.currentTarget.style.transform = "translateY(0px)";
                    }
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 600, color: "#87CEEB" }}>
                      {category}
                      {onCategoryClick && (
                        <span
                          style={{ fontSize: 12, marginLeft: 8, opacity: 0.7 }}
                        >
                          👆 Click to view entries
                        </span>
                      )}
                    </div>
                    <div
                      style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}
                    >
                      {categoryTransactions.length} transactions
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontWeight: 600, color: "#ff6b6b" }}>
                      {formatCurrency(totalSpent)}
                    </div>
                    <div
                      style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}
                    >
                      Avg: {formatCurrency(avgAmount)}
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      </div>

      {/* Backend Analysis Categories (For Reference) */}
      <div style={{ marginBottom: 30 }}>
        <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>
          🤖 Backend Analysis Categories
        </h3>
        <div style={{ display: "grid", gap: 10 }}>
          {Object.entries(analysis.spending_analysis.top_categories)
            .slice(0, 5)
            .map(([category, data]) => (
              <div
                key={category}
                style={{
                  background: "rgba(255, 255, 255, 0.1)",
                  padding: 15,
                  borderRadius: 8,
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  cursor: onCategoryClick ? "pointer" : "default",
                  transition: "all 0.2s ease",
                  border: "2px solid transparent",
                }}
                onClick={() => {
                  if (onCategoryClick) {
                    onCategoryClick(category);
                    onClose(); // Close the savings analyzer after clicking
                  }
                }}
                onMouseEnter={(e) => {
                  if (onCategoryClick) {
                    e.currentTarget.style.background =
                      "rgba(255, 255, 255, 0.2)";
                    e.currentTarget.style.border = "2px solid #87CEEB";
                    e.currentTarget.style.transform = "translateY(-2px)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (onCategoryClick) {
                    e.currentTarget.style.background =
                      "rgba(255, 255, 255, 0.1)";
                    e.currentTarget.style.border = "2px solid transparent";
                    e.currentTarget.style.transform = "translateY(0px)";
                  }
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, color: "#87CEEB" }}>
                    {category}
                    {onCategoryClick && (
                      <span
                        style={{ fontSize: 12, marginLeft: 8, opacity: 0.7 }}
                      >
                        👆 Click to view entries
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
                    {data.Transaction_Count} transactions
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontWeight: 600, color: "#ff6b6b" }}>
                    {formatCurrency(data.Total_Spent)}
                  </div>
                  <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
                    Avg: {formatCurrency(data.Avg_Amount)}
                  </div>
                </div>
              </div>
            ))}
        </div>
        <small style={{ color: "#87CEEB", opacity: 0.7, fontSize: "12px" }}>
          ⚠️ These categories come from the backend analysis and might not match
          your actual transaction categories exactly.
        </small>
      </div>

      {/* Detailed Merchant Recommendations */}
      {analysis.savings_report.detailed_recommendations?.length > 0 && (
        <div style={{ marginBottom: 30 }}>
          <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>
            🎯 Personalized Merchant Recommendations
          </h3>
          <div style={{ display: "grid", gap: 15 }}>
            {analysis.savings_report.detailed_recommendations
              .slice(0, 5)
              .map((rec, index) => (
                <div
                  key={index}
                  style={{
                    background: "rgba(255, 255, 255, 0.1)",
                    padding: 20,
                    borderRadius: 12,
                    border: "1px solid rgba(81, 207, 102, 0.3)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      marginBottom: 15,
                    }}
                  >
                    <div>
                      <div
                        style={{
                          fontWeight: 600,
                          color: "#87CEEB",
                          fontSize: 18,
                          marginBottom: 5,
                        }}
                      >
                        {rec.merchant}
                      </div>
                      <div
                        style={{ fontSize: 13, color: "#87CEEB", opacity: 0.8 }}
                      >
                        ${rec.current_spending} across {rec.transaction_count}{" "}
                        visits (avg ${rec.avg_per_visit}/visit)
                      </div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div
                        style={{
                          fontWeight: 600,
                          color: "#51cf66",
                          fontSize: 16,
                        }}
                      >
                        Save {formatCurrency(rec.potential_savings)}
                      </div>
                      <div
                        style={{ fontSize: 12, color: "#51cf66", opacity: 0.8 }}
                      >
                        {rec.savings_percentage}% savings
                      </div>
                    </div>
                  </div>

                  <div style={{ marginBottom: 15 }}>
                    <div
                      style={{
                        fontSize: 14,
                        color: "#87CEEB",
                        marginBottom: 8,
                      }}
                    >
                      <strong>Try instead:</strong>{" "}
                      {(rec.alternatives || []).slice(0, 3).join(", ")}
                    </div>
                    <div
                      style={{
                        fontSize: 13,
                        color: "#87CEEB",
                        opacity: 0.8,
                        fontStyle: "italic",
                        lineHeight: 1.4,
                      }}
                    >
                      {rec.reasoning}
                    </div>
                  </div>

                  {rec.sample_descriptions &&
                    rec.sample_descriptions.length > 0 && (
                      <div style={{ marginTop: 10 }}>
                        <div
                          style={{
                            fontSize: 12,
                            color: "#87CEEB",
                            opacity: 0.7,
                          }}
                        >
                          <strong>Sample purchases:</strong>{" "}
                          {(rec.sample_descriptions || [])
                            .slice(0, 2)
                            .join(", ")}
                        </div>
                      </div>
                    )}
                </div>
              ))}
          </div>
        </div>
      )}

      {/* General Savings Opportunities */}
      <div style={{ marginBottom: 30 }}>
        <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>
          💡 General Savings Opportunities
        </h3>
        <div style={{ display: "grid", gap: 15 }}>
          {(analysis.savings_report.savings_opportunities || [])
            .slice(0, 5)
            .map((opportunity, index) => (
              <div
                key={index}
                style={{
                  background: "rgba(255, 255, 255, 0.1)",
                  padding: 20,
                  borderRadius: 12,
                  border: "1px solid rgba(81, 207, 102, 0.3)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 15,
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontWeight: 600,
                        color: "#87CEEB",
                        fontSize: 16,
                      }}
                    >
                      {opportunity.category || opportunity.merchant}
                    </div>
                    <div
                      style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}
                    >
                      Current spending:{" "}
                      {formatCurrency(opportunity.current_spending)}
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div
                      style={{
                        fontWeight: 600,
                        color: "#51cf66",
                        fontSize: 16,
                      }}
                    >
                      Save {formatCurrency(opportunity.potential_savings)}
                    </div>
                    <div
                      style={{ fontSize: 12, color: "#51cf66", opacity: 0.8 }}
                    >
                      {(
                        (opportunity.potential_savings /
                          opportunity.current_spending) *
                        100
                      ).toFixed(1)}
                      % savings
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: 15 }}>
                  <div
                    style={{ fontSize: 14, color: "#87CEEB", marginBottom: 10 }}
                  >
                    Alternatives:
                  </div>
                  <div style={{ display: "grid", gap: 8 }}>
                    {(opportunity.alternatives || [])
                      .slice(0, 3)
                      .map((alt, altIndex) => (
                        <div
                          key={altIndex}
                          style={{
                            background: "rgba(255, 255, 255, 0.05)",
                            padding: 10,
                            borderRadius: 6,
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                          }}
                        >
                          <div>
                            <div style={{ fontWeight: 500, color: "#87CEEB" }}>
                              {alt.alternative}
                            </div>
                            <div
                              style={{
                                fontSize: 11,
                                color: "#87CEEB",
                                opacity: 0.7,
                              }}
                            >
                              {alt.reason}
                            </div>
                          </div>
                          <div style={{ textAlign: "right" }}>
                            <div style={{ fontWeight: 600, color: "#51cf66" }}>
                              Save {formatCurrency(alt.estimated_savings)}
                            </div>
                            <div
                              style={{
                                fontSize: 11,
                                color: "#51cf66",
                                opacity: 0.8,
                              }}
                            >
                              {alt.savings_percentage}%
                            </div>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Recommendations */}
      {analysis.comprehensive_savings.recommendations.length > 0 && (
        <div style={{ marginBottom: 30 }}>
          <h3 style={{ color: "#87CEEB", marginBottom: 15 }}>
            🎯 Personalized Recommendations
          </h3>
          <div style={{ display: "grid", gap: 10 }}>
            {analysis.comprehensive_savings.recommendations.map(
              (recommendation, index) => (
                <div
                  key={index}
                  style={{
                    background: "rgba(255, 255, 255, 0.1)",
                    padding: 15,
                    borderRadius: 8,
                    borderLeft: "4px solid #51cf66",
                  }}
                >
                  <div style={{ color: "#87CEEB", lineHeight: 1.5 }}>
                    {recommendation}
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div
        style={{
          display: "flex",
          gap: 10,
          justifyContent: "center",
          marginTop: 30,
        }}
      >
        <button
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #51cf66, #40c057)",
            color: "white",
            fontWeight: "600",
          }}
          onClick={() => setShowDetailedPage(true)}
        >
          📊 View All Recommendations
        </button>
        <button style={buttonStyle} onClick={analyzeSpending}>
          🔄 Refresh Analysis
        </button>
        <button
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #ff6b6b, #ee5a52)",
            color: "white",
            fontWeight: "600",
            padding: "12px 24px",
            fontSize: "16px",
          }}
          onClick={onClose}
        >
          ← Back to Main View
        </button>
      </div>

      {/* Detailed Page Modal */}
      {showDetailedPage && analysis && (
        <DetailedSavingsPage
          detailedRecommendations={
            analysis.savings_report.detailed_recommendations || []
          }
          generalOpportunities={
            analysis.savings_report.savings_opportunities || []
          }
          totalPotentialSavings={analysis.total_potential_savings}
          totalExpenses={analysis.spending_analysis.total_expenses}
          onClose={() => setShowDetailedPage(false)}
        />
      )}
    </div>
  );
};

export default SavingsAnalyzer;
