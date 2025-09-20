import React, { useMemo, useState } from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
  Label,
} from "recharts";

type Item = {
  Category: string;
  TransactionCount: number;
  TotalAmount: number;
  Withdrawals: number; // negative
  Deposits: number; // positive
};

type Props = {
  data: Item[];
  format: (n: number) => string;
  onCategoryClick?: (category: string | null) => void;
  onSpendingClick?: () => void;
  onEarningClick?: () => void;
  selectedCategory?: string | null;
  selectedFilterType?: "all" | "spending" | "earning" | "category";
  showSpendingCategories?: boolean;
  onToggleSpendingCategories?: (showSpending: boolean) => void;
};

// Nice, readable palette (loops if we exceed length)
const PALETTE = [
  "#6366F1", // indigo
  "#10B981", // emerald
  "#F59E0B", // amber
  "#EF4444", // red
  "#3B82F6", // blue
  "#8B5CF6", // violet
  "#14B8A6", // teal
  "#F97316", // orange
  "#22C55E", // green
  "#A855F7", // purple
  "#06B6D4", // cyan
  "#EAB308", // yellow
];

const CategoryPieCard: React.FC<Props> = ({
  data,
  format,
  onCategoryClick,
  onSpendingClick,
  onEarningClick,
  selectedCategory,
  selectedFilterType,
  showSpendingCategories = true,
  onToggleSpendingCategories,
}) => {
  // Debug: Log the incoming data (can be removed in production)
  console.log("CategoryPieCard received data:", data);

  // prefer spend (abs of withdrawals), fall back to abs(total) when needed
  const pieData = useMemo(() => {
    const processed = data
      .map((d) => {
        // Use absolute value of withdrawals (spending) or total amount
        const spend = Math.abs(d.Withdrawals || 0);
        const fallback = Math.abs(d.TotalAmount || 0);
        const value = spend > 0 ? spend : fallback;
        return {
          name: d.Category || "Uncategorized",
          value: value,
        };
      })
      .filter((d) => d.value > 0); // Only show categories with actual spending

    console.log("CategoryPieCard pieData processed:", processed);
    return processed;
  }, [data]);

  // Calculate spending vs earnings analysis
  const spendingEarningsAnalysis = useMemo(() => {
    const totalSpending = data.reduce(
      (sum, d) => sum + Math.abs(d.Withdrawals || 0),
      0
    );
    const totalEarnings = data.reduce((sum, d) => sum + (d.Deposits || 0), 0);
    const netCashFlow = totalEarnings - totalSpending;

    // Top spending categories
    const topSpending = data
      .filter((d) => Math.abs(d.Withdrawals || 0) > 0)
      .sort(
        (a, b) => Math.abs(b.Withdrawals || 0) - Math.abs(a.Withdrawals || 0)
      )
      .slice(0, 5);

    // Top earning categories
    const topEarnings = data
      .filter((d) => (d.Deposits || 0) > 0)
      .sort((a, b) => (b.Deposits || 0) - (a.Deposits || 0))
      .slice(0, 5);

    return {
      totalSpending,
      totalEarnings,
      netCashFlow,
      topSpending,
      topEarnings,
    };
  }, [data]);

  return (
    <div
      style={{
        border: "1px solid rgba(255, 255, 255, 0.2)",
        borderRadius: 16,
        padding: 20,
        background: "rgba(255, 255, 255, 0.15)",
        backdropFilter: "blur(10px)",
        boxShadow: "0 4px 16px rgba(0, 0, 0, 0.1)",
      }}
    >
      <h3
        style={{
          margin: "4px 0 10px",
          fontSize: 18,
          fontWeight: 600,
          color: "#87CEEB",
        }}
      >
        Financial Analysis
      </h3>

      {/* Spending vs Earnings Summary */}
      <div style={{ marginBottom: 20 }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr",
            gap: 10,
            marginBottom: 15,
          }}
        >
          <div
            style={{
              background:
                selectedFilterType === "spending"
                  ? "rgba(255, 107, 107, 0.4)"
                  : "rgba(255, 107, 107, 0.2)",
              padding: 12,
              borderRadius: 8,
              textAlign: "center",
              cursor: "pointer",
              border:
                selectedFilterType === "spending"
                  ? "2px solid #ff6b6b"
                  : "2px solid transparent",
              transition: "all 0.2s ease",
            }}
            onClick={() => {
              console.log("Total Spending clicked");
              onSpendingClick?.();
            }}
            onMouseEnter={(e) => {
              if (selectedFilterType !== "spending") {
                e.currentTarget.style.background = "rgba(255, 107, 107, 0.3)";
                e.currentTarget.style.border = "2px solid #ff6b6b";
              }
            }}
            onMouseLeave={(e) => {
              if (selectedFilterType !== "spending") {
                e.currentTarget.style.background = "rgba(255, 107, 107, 0.2)";
                e.currentTarget.style.border = "2px solid transparent";
              }
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Total Spending {selectedFilterType === "spending" && "✓"}
            </div>
            <div style={{ fontSize: 16, fontWeight: 600, color: "#ff6b6b" }}>
              {format(spendingEarningsAnalysis.totalSpending)}
            </div>
          </div>
          <div
            style={{
              background:
                selectedFilterType === "earning"
                  ? "rgba(81, 207, 102, 0.4)"
                  : "rgba(81, 207, 102, 0.2)",
              padding: 12,
              borderRadius: 8,
              textAlign: "center",
              cursor: "pointer",
              border:
                selectedFilterType === "earning"
                  ? "2px solid #51cf66"
                  : "2px solid transparent",
              transition: "all 0.2s ease",
            }}
            onClick={() => {
              console.log("Total Earnings clicked");
              onEarningClick?.();
            }}
            onMouseEnter={(e) => {
              if (selectedFilterType !== "earning") {
                e.currentTarget.style.background = "rgba(81, 207, 102, 0.3)";
                e.currentTarget.style.border = "2px solid #51cf66";
              }
            }}
            onMouseLeave={(e) => {
              if (selectedFilterType !== "earning") {
                e.currentTarget.style.background = "rgba(81, 207, 102, 0.2)";
                e.currentTarget.style.border = "2px solid transparent";
              }
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Total Earnings {selectedFilterType === "earning" && "✓"}
            </div>
            <div style={{ fontSize: 16, fontWeight: 600, color: "#51cf66" }}>
              {format(spendingEarningsAnalysis.totalEarnings)}
            </div>
          </div>
          <div
            style={{
              background:
                selectedFilterType === "all"
                  ? spendingEarningsAnalysis.netCashFlow >= 0
                    ? "rgba(81, 207, 102, 0.4)"
                    : "rgba(255, 107, 107, 0.4)"
                  : spendingEarningsAnalysis.netCashFlow >= 0
                  ? "rgba(81, 207, 102, 0.2)"
                  : "rgba(255, 107, 107, 0.2)",
              padding: 12,
              borderRadius: 8,
              textAlign: "center",
              cursor: "pointer",
              border:
                selectedFilterType === "all"
                  ? "2px solid #87CEEB"
                  : "2px solid transparent",
              transition: "all 0.2s ease",
            }}
            onClick={() => {
              console.log("Net Cash Flow clicked - showing all");
              onCategoryClick?.(null); // This will reset to show all entries
            }}
            onMouseEnter={(e) => {
              if (selectedFilterType !== "all") {
                e.currentTarget.style.border = "2px solid #87CEEB";
                e.currentTarget.style.background =
                  spendingEarningsAnalysis.netCashFlow >= 0
                    ? "rgba(81, 207, 102, 0.3)"
                    : "rgba(255, 107, 107, 0.3)";
              }
            }}
            onMouseLeave={(e) => {
              if (selectedFilterType !== "all") {
                e.currentTarget.style.border = "2px solid transparent";
                e.currentTarget.style.background =
                  spendingEarningsAnalysis.netCashFlow >= 0
                    ? "rgba(81, 207, 102, 0.2)"
                    : "rgba(255, 107, 107, 0.2)";
              }
            }}
          >
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.8 }}>
              Net Cash Flow {selectedFilterType === "all" && "✓"}
            </div>
            <div
              style={{
                fontSize: 16,
                fontWeight: 600,
                color:
                  spendingEarningsAnalysis.netCashFlow >= 0
                    ? "#51cf66"
                    : "#ff6b6b",
              }}
            >
              {format(spendingEarningsAnalysis.netCashFlow)}
            </div>
          </div>
        </div>
      </div>

      {/* The container MUST have an explicit height */}
      <div style={{ width: "100%", height: 280 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={2}
              stroke="#ffffff"
              strokeWidth={2}
              isAnimationActive={false}
            >
              {pieData.map((entry, idx) => {
                // Use red for spending and green for earning when showing category breakdown
                let fillColor = PALETTE[idx % PALETTE.length];

                if (entry.name.includes(" - Spending")) {
                  fillColor = "#EF4444"; // Red for spending
                } else if (entry.name.includes(" - Earning")) {
                  fillColor = "#22C55E"; // Green for earning
                }

                return (
                  <Cell key={`cell-${entry.name}-${idx}`} fill={fillColor} />
                );
              })}
              {/* center label (total spend) */}
              <Label
                value={
                  pieData.length
                    ? `Total ${format(
                        pieData.reduce((s, x) => s + (x.value || 0), 0)
                      )}`
                    : "No data"
                }
                position="center"
                fontSize={12}
                fill="#87CEEB"
              />
            </Pie>
            <Tooltip
              formatter={(val: number, _name: string, payload: any) => [
                format(val),
                payload?.name,
              ]}
              cursor={{ fill: "rgba(0,0,0,0.03)" }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              wrapperStyle={{
                color: "#87CEEB !important",
                fontSize: "10px",
                fill: "#87CEEB !important",
              }}
              iconType="circle"
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Top Categories with Toggle */}
      {(spendingEarningsAnalysis.topSpending.length > 0 ||
        spendingEarningsAnalysis.topEarnings.length > 0) && (
        <div style={{ marginTop: 20 }}>
          {/* Toggle Button */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 10,
            }}
          >
            <div style={{ display: "flex", gap: 8 }}>
              <button
                onClick={() => onToggleSpendingCategories?.(true)}
                style={{
                  padding: "6px 12px",
                  backgroundColor: showSpendingCategories
                    ? "#ff6b6b"
                    : "transparent",
                  color: showSpendingCategories ? "white" : "#ff6b6b",
                  border: "1px solid #ff6b6b",
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  if (!showSpendingCategories) {
                    e.currentTarget.style.backgroundColor =
                      "rgba(255, 107, 107, 0.1)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (!showSpendingCategories) {
                    e.currentTarget.style.backgroundColor = "transparent";
                  }
                }}
              >
                🔥 Spending
              </button>
              <button
                onClick={() => onToggleSpendingCategories?.(false)}
                style={{
                  padding: "6px 12px",
                  backgroundColor: !showSpendingCategories
                    ? "#51cf66"
                    : "transparent",
                  color: !showSpendingCategories ? "white" : "#51cf66",
                  border: "1px solid #51cf66",
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  if (showSpendingCategories) {
                    e.currentTarget.style.backgroundColor =
                      "rgba(81, 207, 102, 0.1)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (showSpendingCategories) {
                    e.currentTarget.style.backgroundColor = "transparent";
                  }
                }}
              >
                💰 Earning
              </button>
            </div>
            <div style={{ fontSize: 12, color: "#87CEEB", opacity: 0.7 }}>
              Click categories to filter entries
            </div>
          </div>

          {/* Spending Categories */}
          {showSpendingCategories &&
            spendingEarningsAnalysis.topSpending.length > 0 && (
              <div>
                <h4
                  style={{
                    fontSize: 14,
                    fontWeight: 600,
                    color: "#87CEEB",
                    marginBottom: 10,
                    cursor: "pointer",
                    padding: "4px 8px",
                    borderRadius: "4px",
                    backgroundColor:
                      selectedFilterType === "spending"
                        ? "rgba(255, 107, 107, 0.2)"
                        : "transparent",
                    transition: "background-color 0.2s ease",
                  }}
                  onClick={() => {
                    console.log("Spending section clicked");
                    onSpendingClick?.();
                  }}
                  onMouseEnter={(e) => {
                    if (selectedFilterType !== "spending") {
                      e.currentTarget.style.backgroundColor =
                        "rgba(255, 107, 107, 0.1)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedFilterType !== "spending") {
                      e.currentTarget.style.backgroundColor = "transparent";
                    }
                  }}
                >
                  🔥 Top Spending Categories{" "}
                  {selectedFilterType === "spending" && "✓"}
                </h4>
                <div style={{ display: "grid", gap: 6 }}>
                  {spendingEarningsAnalysis.topSpending.map(
                    (category, index) => (
                      <div
                        key={category.Category}
                        onClick={() => {
                          console.log(
                            "Spending category clicked:",
                            category.Category
                          );
                          console.log("Full category object:", category);
                          onCategoryClick?.(category.Category);
                        }}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          background:
                            selectedCategory === category.Category &&
                            selectedFilterType === "category"
                              ? "rgba(255, 107, 107, 0.3)"
                              : "rgba(255, 107, 107, 0.1)",
                          padding: "8px 12px",
                          borderRadius: 6,
                          borderLeft: "3px solid #ff6b6b",
                          cursor: "pointer",
                          transition: "background-color 0.2s ease",
                          border:
                            selectedCategory === category.Category &&
                            selectedFilterType === "category"
                              ? "2px solid #ff6b6b"
                              : "2px solid transparent",
                        }}
                        onMouseEnter={(e) => {
                          if (selectedCategory !== category.Category) {
                            e.currentTarget.style.background =
                              "rgba(255, 107, 107, 0.2)";
                          }
                        }}
                        onMouseLeave={(e) => {
                          if (selectedCategory !== category.Category) {
                            e.currentTarget.style.background =
                              "rgba(255, 107, 107, 0.1)";
                          }
                        }}
                      >
                        <div>
                          <div
                            style={{
                              fontSize: 12,
                              fontWeight: 500,
                              color: "#87CEEB",
                            }}
                          >
                            {category.Category}{" "}
                            {selectedCategory === category.Category &&
                              selectedFilterType === "category" &&
                              "✓"}
                          </div>
                          <div
                            style={{
                              fontSize: 10,
                              color: "#87CEEB",
                              opacity: 0.7,
                            }}
                          >
                            {category.TransactionCount} transactions
                          </div>
                        </div>
                        <div
                          style={{
                            fontSize: 12,
                            fontWeight: 600,
                            color: "#ff6b6b",
                          }}
                        >
                          {format(Math.abs(category.Withdrawals || 0))}
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}

          {/* Earning Categories */}
          {!showSpendingCategories &&
            spendingEarningsAnalysis.topEarnings.length > 0 && (
              <div>
                <h4
                  style={{
                    fontSize: 14,
                    fontWeight: 600,
                    color: "#87CEEB",
                    marginBottom: 10,
                    cursor: "pointer",
                    padding: "4px 8px",
                    borderRadius: "4px",
                    backgroundColor:
                      selectedFilterType === "earning"
                        ? "rgba(81, 207, 102, 0.2)"
                        : "transparent",
                    transition: "background-color 0.2s ease",
                  }}
                  onClick={() => {
                    console.log("Earning section clicked");
                    onEarningClick?.();
                  }}
                  onMouseEnter={(e) => {
                    if (selectedFilterType !== "earning") {
                      e.currentTarget.style.backgroundColor =
                        "rgba(81, 207, 102, 0.1)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedFilterType !== "earning") {
                      e.currentTarget.style.backgroundColor = "transparent";
                    }
                  }}
                >
                  💰 Top Earning Sources{" "}
                  {selectedFilterType === "earning" && "✓"}
                </h4>
                <div style={{ display: "grid", gap: 6 }}>
                  {spendingEarningsAnalysis.topEarnings.map(
                    (category, index) => (
                      <div
                        key={category.Category}
                        onClick={() => {
                          console.log(
                            "Earning category clicked:",
                            category.Category
                          );
                          console.log("Full category object:", category);
                          onCategoryClick?.(category.Category);
                        }}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          background:
                            selectedCategory === category.Category &&
                            selectedFilterType === "category"
                              ? "rgba(81, 207, 102, 0.3)"
                              : "rgba(81, 207, 102, 0.1)",
                          padding: "8px 12px",
                          borderRadius: 6,
                          borderLeft: "3px solid #51cf66",
                          cursor: "pointer",
                          transition: "background-color 0.2s ease",
                          border:
                            selectedCategory === category.Category &&
                            selectedFilterType === "category"
                              ? "2px solid #51cf66"
                              : "2px solid transparent",
                        }}
                        onMouseEnter={(e) => {
                          if (selectedCategory !== category.Category) {
                            e.currentTarget.style.background =
                              "rgba(81, 207, 102, 0.2)";
                          }
                        }}
                        onMouseLeave={(e) => {
                          if (selectedCategory !== category.Category) {
                            e.currentTarget.style.background =
                              "rgba(81, 207, 102, 0.1)";
                          }
                        }}
                      >
                        <div>
                          <div
                            style={{
                              fontSize: 12,
                              fontWeight: 500,
                              color: "#87CEEB",
                            }}
                          >
                            {category.Category}{" "}
                            {selectedCategory === category.Category &&
                              selectedFilterType === "category" &&
                              "✓"}
                          </div>
                          <div
                            style={{
                              fontSize: 10,
                              color: "#87CEEB",
                              opacity: 0.7,
                            }}
                          >
                            {category.TransactionCount} transactions
                          </div>
                        </div>
                        <div
                          style={{
                            fontSize: 12,
                            fontWeight: 600,
                            color: "#51cf66",
                          }}
                        >
                          {format(category.Deposits || 0)}
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
        </div>
      )}

      {pieData.length === 0 && (
        <div style={{ padding: 8, color: "#87CEEB", fontSize: 14 }}>
          No transaction data to display.
        </div>
      )}
    </div>
  );
};

export default CategoryPieCard;
