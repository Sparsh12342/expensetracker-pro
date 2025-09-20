import React from "react";

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

interface DetailedSavingsPageProps {
  detailedRecommendations: DetailedRecommendation[];
  generalOpportunities: SavingsOpportunity[];
  totalPotentialSavings: number;
  totalExpenses: number;
  onClose: () => void;
}

const DetailedSavingsPage: React.FC<DetailedSavingsPageProps> = ({
  detailedRecommendations,
  generalOpportunities,
  totalPotentialSavings,
  totalExpenses,
  onClose,
}) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const pageStyle: React.CSSProperties = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0, 0, 0, 0.95)",
    zIndex: 2000,
    overflow: "auto",
    padding: "20px",
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: "1200px",
    margin: "0 auto",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    borderRadius: "20px",
    padding: "30px",
    boxShadow: "0 20px 40px rgba(0, 0, 0, 0.3)",
  };

  const headerStyle: React.CSSProperties = {
    textAlign: "center",
    marginBottom: "40px",
    color: "#87CEEB",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
    textShadow: "2px 2px 4px rgba(0, 0, 0, 0.3)",
  };

  const subtitleStyle: React.CSSProperties = {
    fontSize: "18px",
    opacity: 0.9,
    marginBottom: "20px",
  };

  const summaryCardStyle: React.CSSProperties = {
    background: "rgba(255, 255, 255, 0.15)",
    backdropFilter: "blur(10px)",
    borderRadius: "16px",
    padding: "25px",
    marginBottom: "30px",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.1)",
  };

  const summaryGridStyle: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "20px",
    marginBottom: "20px",
  };

  const summaryItemStyle: React.CSSProperties = {
    textAlign: "center",
    padding: "15px",
    background: "rgba(255, 255, 255, 0.1)",
    borderRadius: "12px",
  };

  const summaryLabelStyle: React.CSSProperties = {
    fontSize: "14px",
    color: "#87CEEB",
    opacity: 0.8,
    marginBottom: "5px",
  };

  const summaryValueStyle: React.CSSProperties = {
    fontSize: "24px",
    fontWeight: "600",
    color: "#fff",
  };

  const sectionStyle: React.CSSProperties = {
    marginBottom: "40px",
  };

  const sectionTitleStyle: React.CSSProperties = {
    fontSize: "24px",
    fontWeight: "600",
    color: "#87CEEB",
    marginBottom: "20px",
    textAlign: "center",
    textShadow: "1px 1px 2px rgba(0, 0, 0, 0.3)",
  };

  const recommendationCardStyle: React.CSSProperties = {
    background: "rgba(255, 255, 255, 0.15)",
    backdropFilter: "blur(10px)",
    borderRadius: "16px",
    padding: "25px",
    marginBottom: "20px",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.1)",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
  };

  const merchantHeaderStyle: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "20px",
    flexWrap: "wrap",
    gap: "15px",
  };

  const merchantInfoStyle: React.CSSProperties = {
    flex: "1",
    minWidth: "250px",
  };

  const merchantNameStyle: React.CSSProperties = {
    fontSize: "22px",
    fontWeight: "700",
    color: "#87CEEB",
    marginBottom: "8px",
    textShadow: "1px 1px 2px rgba(0, 0, 0, 0.3)",
  };

  const spendingStatsStyle: React.CSSProperties = {
    fontSize: "14px",
    color: "#87CEEB",
    opacity: 0.9,
    lineHeight: "1.4",
  };

  const savingsBadgeStyle: React.CSSProperties = {
    background: "linear-gradient(135deg, #51cf66, #40c057)",
    color: "white",
    padding: "15px 20px",
    borderRadius: "12px",
    textAlign: "center",
    minWidth: "150px",
    boxShadow: "0 4px 15px rgba(81, 207, 102, 0.3)",
  };

  const savingsAmountStyle: React.CSSProperties = {
    fontSize: "20px",
    fontWeight: "700",
    marginBottom: "5px",
  };

  const savingsPercentageStyle: React.CSSProperties = {
    fontSize: "14px",
    opacity: 0.9,
  };

  const alternativesSectionStyle: React.CSSProperties = {
    marginBottom: "20px",
  };

  const alternativesTitleStyle: React.CSSProperties = {
    fontSize: "16px",
    fontWeight: "600",
    color: "#87CEEB",
    marginBottom: "12px",
  };

  const alternativesListStyle: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "10px",
    marginBottom: "15px",
  };

  const alternativeItemStyle: React.CSSProperties = {
    background: "rgba(255, 255, 255, 0.1)",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    fontSize: "14px",
    color: "#fff",
    fontWeight: "500",
  };

  const reasoningStyle: React.CSSProperties = {
    fontSize: "14px",
    color: "#87CEEB",
    opacity: 0.9,
    fontStyle: "italic",
    lineHeight: "1.5",
    background: "rgba(255, 255, 255, 0.05)",
    padding: "15px",
    borderRadius: "8px",
    borderLeft: "4px solid #51cf66",
  };

  const samplePurchasesStyle: React.CSSProperties = {
    marginTop: "15px",
    fontSize: "12px",
    color: "#87CEEB",
    opacity: 0.7,
    background: "rgba(255, 255, 255, 0.05)",
    padding: "10px",
    borderRadius: "6px",
  };

  const closeButtonStyle: React.CSSProperties = {
    position: "fixed",
    top: "20px",
    right: "20px",
    background: "rgba(255, 255, 255, 0.2)",
    border: "1px solid rgba(255, 255, 255, 0.3)",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    color: "#87CEEB",
    cursor: "pointer",
    fontSize: "20px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backdropFilter: "blur(10px)",
    boxShadow: "0 4px 15px rgba(0, 0, 0, 0.2)",
    transition: "all 0.2s ease",
  };

  const scrollToTopStyle: React.CSSProperties = {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    background: "rgba(81, 207, 102, 0.8)",
    border: "none",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    color: "white",
    cursor: "pointer",
    fontSize: "18px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backdropFilter: "blur(10px)",
    boxShadow: "0 4px 15px rgba(81, 207, 102, 0.3)",
    transition: "all 0.2s ease",
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div style={pageStyle}>
      <button style={closeButtonStyle} onClick={onClose} title="Close">
        ✕
      </button>

      <div style={containerStyle}>
        <div style={headerStyle}>
          <h1 style={titleStyle}>💰 Detailed Savings Analysis</h1>
          <p style={subtitleStyle}>
            Personalized recommendations to help you save money on your spending
          </p>
        </div>

        {/* Summary Card */}
        <div style={summaryCardStyle}>
          <div style={summaryGridStyle}>
            <div style={summaryItemStyle}>
              <div style={summaryLabelStyle}>Total Expenses</div>
              <div style={{ ...summaryValueStyle, color: "#ff6b6b" }}>
                {formatCurrency(totalExpenses)}
              </div>
            </div>
            <div style={summaryItemStyle}>
              <div style={summaryLabelStyle}>Potential Savings</div>
              <div style={{ ...summaryValueStyle, color: "#51cf66" }}>
                {formatCurrency(totalPotentialSavings)}
              </div>
            </div>
            <div style={summaryItemStyle}>
              <div style={summaryLabelStyle}>Savings Percentage</div>
              <div style={{ ...summaryValueStyle, color: "#51cf66" }}>
                {((totalPotentialSavings / totalExpenses) * 100).toFixed(1)}%
              </div>
            </div>
            <div style={summaryItemStyle}>
              <div style={summaryLabelStyle}>Recommendations</div>
              <div style={{ ...summaryValueStyle, color: "#87CEEB" }}>
                {detailedRecommendations.length + generalOpportunities.length}
              </div>
            </div>
          </div>
        </div>

        {/* Detailed Merchant Recommendations */}
        {detailedRecommendations.length > 0 && (
          <div style={sectionStyle}>
            <h2 style={sectionTitleStyle}>
              🎯 Personalized Merchant Recommendations
            </h2>
            {detailedRecommendations.map((rec, index) => (
              <div key={index} style={recommendationCardStyle}>
                <div style={merchantHeaderStyle}>
                  <div style={merchantInfoStyle}>
                    <div style={merchantNameStyle}>{rec.merchant}</div>
                    <div style={spendingStatsStyle}>
                      <strong>Current Spending:</strong>{" "}
                      {formatCurrency(rec.current_spending)} across{" "}
                      {rec.transaction_count} visits
                      <br />
                      <strong>Average per visit:</strong>{" "}
                      {formatCurrency(rec.avg_per_visit)}
                    </div>
                  </div>
                  <div style={savingsBadgeStyle}>
                    <div style={savingsAmountStyle}>
                      Save {formatCurrency(rec.potential_savings)}
                    </div>
                    <div style={savingsPercentageStyle}>
                      {rec.savings_percentage}% savings
                    </div>
                  </div>
                </div>

                <div style={alternativesSectionStyle}>
                  <div style={alternativesTitleStyle}>🔄 Try Instead:</div>
                  <div style={alternativesListStyle}>
                    {rec.alternatives.map((alt, altIndex) => (
                      <div key={altIndex} style={alternativeItemStyle}>
                        {alt}
                      </div>
                    ))}
                  </div>
                </div>

                <div style={reasoningStyle}>
                  <strong>💡 Why this works:</strong> {rec.reasoning}
                </div>

                {rec.sample_descriptions &&
                  rec.sample_descriptions.length > 0 && (
                    <div style={samplePurchasesStyle}>
                      <strong>📝 Sample purchases:</strong>{" "}
                      {rec.sample_descriptions.join(", ")}
                    </div>
                  )}
              </div>
            ))}
          </div>
        )}

        {/* General Savings Opportunities */}
        {generalOpportunities.length > 0 && (
          <div style={sectionStyle}>
            <h2 style={sectionTitleStyle}>💡 General Savings Opportunities</h2>
            {generalOpportunities.map((opportunity, index) => (
              <div key={index} style={recommendationCardStyle}>
                <div style={merchantHeaderStyle}>
                  <div style={merchantInfoStyle}>
                    <div style={merchantNameStyle}>
                      {opportunity.category || opportunity.merchant}
                    </div>
                    <div style={spendingStatsStyle}>
                      <strong>Current Spending:</strong>{" "}
                      {formatCurrency(opportunity.current_spending)} across{" "}
                      {opportunity.transaction_count} transactions
                    </div>
                  </div>
                  <div style={savingsBadgeStyle}>
                    <div style={savingsAmountStyle}>
                      Save {formatCurrency(opportunity.potential_savings)}
                    </div>
                    <div style={savingsPercentageStyle}>
                      {(
                        (opportunity.potential_savings /
                          opportunity.current_spending) *
                        100
                      ).toFixed(1)}
                      % savings
                    </div>
                  </div>
                </div>

                <div style={alternativesSectionStyle}>
                  <div style={alternativesTitleStyle}>🔄 Alternatives:</div>
                  <div style={alternativesListStyle}>
                    {opportunity.alternatives.map((alt, altIndex) => (
                      <div key={altIndex} style={alternativeItemStyle}>
                        <div style={{ fontWeight: "600", marginBottom: "5px" }}>
                          {alt.alternative}
                        </div>
                        <div style={{ fontSize: "12px", opacity: 0.8 }}>
                          Save {formatCurrency(alt.estimated_savings)} (
                          {alt.savings_percentage}%)
                        </div>
                        <div
                          style={{
                            fontSize: "11px",
                            opacity: 0.7,
                            marginTop: "3px",
                          }}
                        >
                          {alt.reason}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Action Buttons */}
        <div style={{ textAlign: "center", marginTop: "40px" }}>
          <button
            style={{
              background: "linear-gradient(135deg, #51cf66, #40c057)",
              border: "none",
              borderRadius: "12px",
              padding: "15px 30px",
              color: "white",
              fontSize: "16px",
              fontWeight: "600",
              cursor: "pointer",
              margin: "0 10px",
              boxShadow: "0 4px 15px rgba(81, 207, 102, 0.3)",
              transition: "all 0.2s ease",
            }}
            onClick={onClose}
          >
            ✅ Got it! Let's start saving
          </button>
        </div>
      </div>

      <button
        style={scrollToTopStyle}
        onClick={scrollToTop}
        title="Scroll to top"
      >
        ↑
      </button>
    </div>
  );
};

export default DetailedSavingsPage;

