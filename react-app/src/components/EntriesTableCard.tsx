import React from "react";
import CardLayout from "./CardLayout";
import { getCategoryColor } from "../constants";

type Props = {
  entries: string[][];
  format: (n: number) => string;
  isFiltered?: boolean;
  selectedCategory?: string | null;
  onCategoryClick?: (category: string) => void;
  allEntries?: string[][]; // All entries to get category names from
  pieChartCategories?: Array<{ Category: string; TotalAmount: number }>; // Categories from pie chart
  backendEntries?: Array<{
    Date: string;
    Description: string;
    Amount: string | number;
    PredictedCategory?: string;
  }>; // Backend categorized entries
};

export default function EntriesTableCard({
  entries,
  format,
  isFiltered,
  selectedCategory,
  onCategoryClick,
  allEntries,
  pieChartCategories,
  backendEntries,
}: Props) {
  // Use the filtered entries passed from parent (App.tsx handles the filtering)
  const displayEntries = React.useMemo(() => {
    // Always use the entries prop - this contains the filtered results from App.tsx
    return entries;
  }, [entries]);

  // Use pie chart categories if available, otherwise fall back to entry categories
  const uniqueCategories = React.useMemo(() => {
    if (pieChartCategories && pieChartCategories.length > 0) {
      return pieChartCategories.map((cat) => cat.Category);
    }

    const sourceEntries = allEntries || entries;
    return [
      ...new Set(
        sourceEntries.map((entry) => (entry[3] || "Uncategorized").trim())
      ),
    ];
  }, [pieChartCategories, allEntries, entries]);
  return (
    <CardLayout title="Entries">
      {/* Clickable Category Chips */}
      {onCategoryClick && uniqueCategories.length > 0 && (
        <div
          style={{
            marginBottom: 15,
            padding: 10,
            backgroundColor: "#f8f9fa",
            borderRadius: 8,
            border: "1px solid #e9ecef",
          }}
        >
          <div
            style={{
              fontSize: 12,
              fontWeight: 600,
              color: "#495057",
              marginBottom: 8,
            }}
          >
            📂 Filter by Category:
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {uniqueCategories.map((category, index) => (
              <button
                key={index}
                onClick={() => onCategoryClick(category)}
                style={{
                  padding: "4px 8px",
                  backgroundColor:
                    selectedCategory === category ? "#007bff" : "#e9ecef",
                  color: selectedCategory === category ? "white" : "#495057",
                  border: "1px solid #dee2e6",
                  borderRadius: 12,
                  fontSize: "11px",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  fontWeight: selectedCategory === category ? 600 : 400,
                }}
                onMouseEnter={(e) => {
                  if (selectedCategory !== category) {
                    e.currentTarget.style.backgroundColor = "#dee2e6";
                    e.currentTarget.style.borderColor = "#adb5bd";
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedCategory !== category) {
                    e.currentTarget.style.backgroundColor = "#e9ecef";
                    e.currentTarget.style.borderColor = "#dee2e6";
                  }
                }}
              >
                {category}
                {selectedCategory === category && (
                  <span style={{ marginLeft: 4 }}>✓</span>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      <div
        style={{
          maxHeight: "calc(100vh - 260px)",
          overflowY: "auto",
          border: "1px solid #e5e5e5",
          borderRadius: 6,
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            tableLayout: "fixed",
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "#0078d7", color: "white" }}>
              <th style={{ padding: 8 }}>Date</th>
              <th style={{ padding: 8 }}>Description</th>
              <th style={{ padding: 8, textAlign: "right" }}>Amount</th>
              <th style={{ padding: 8 }}>Category</th>
            </tr>
          </thead>
          <tbody>
            {displayEntries.map((r, i) => (
              <tr
                key={i}
                style={{
                  backgroundColor: i % 2 === 0 ? "#f0f8ff" : "white",
                }}
              >
                <td style={{ padding: 8 }}>{r[0]}</td>
                <td style={{ padding: 8 }}>{r[1]}</td>
                <td
                  style={{
                    padding: 8,
                    textAlign: "right",
                    fontWeight: "bold",
                  }}
                >
                  {format(Number(r[2]))}
                </td>
                <td
                  style={{
                    padding: 8,
                    backgroundColor: getCategoryColor(r[3]),
                  }}
                >
                  {r[3]}
                </td>
              </tr>
            ))}
            {displayEntries.length === 0 && (
              <tr>
                <td
                  colSpan={4}
                  style={{ padding: 12, color: "#666", textAlign: "center" }}
                >
                  {isFiltered && selectedCategory ? (
                    <>
                      No entries found for category:{" "}
                      <strong>{selectedCategory}</strong>
                      <br />
                      <small>
                        The category name from the Savings Analyzer might not
                        match the exact category names in your transactions. Try
                        clicking a different category or clear the filter to see
                        all entries.
                      </small>
                      <br />
                      <small style={{ color: "#666", fontStyle: "italic" }}>
                        💡 Check the browser console for detailed matching
                        information.
                      </small>
                    </>
                  ) : (
                    "No entries yet."
                  )}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </CardLayout>
  );
}
