import React from "react";
import CardLayout from "./CardLayout";
import { categoryOptions } from "../constants";

type Entry = {
  Date: string;
  Description: string;
  Amount: string;
  Category: (typeof categoryOptions)[number] | string;
};

type Props = {
  entry: Entry;
  loading: boolean;
  onChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  onAdd: () => void;
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

export default function EntryFormCard({
  entry,
  loading,
  onChange,
  onAdd,
  onFileUpload,
}: Props) {
  const [showVideo, setShowVideo] = React.useState(false);

  const downloadSampleCSV = async () => {
    try {
      // Fetch the sample CSV file
      const response = await fetch("/sample_transactions_1000.csv");
      if (!response.ok) {
        throw new Error("Failed to fetch sample CSV");
      }

      const csvContent = await response.text();

      // Create a blob and download link
      const blob = new Blob([csvContent], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);

      // Create download link and trigger download
      const link = document.createElement("a");
      link.href = url;
      link.download = "sample_transactions_1000.csv";
      document.body.appendChild(link);
      link.click();

      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error downloading sample CSV:", error);
      alert("Failed to download sample CSV. Please try again.");
    }
  };
  return (
    <CardLayout title="Add Transactions / Upload CSV">
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginBottom: 10,
          tableLayout: "fixed",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#333", color: "white" }}>
            <th style={{ padding: 8 }}>Date</th>
            <th style={{ padding: 8 }}>Description</th>
            <th style={{ padding: 8 }}>Amount</th>
            <th style={{ padding: 8 }}>Category</th>
            <th style={{ padding: 8 }}>Add</th>
          </tr>
        </thead>
        <tbody>
          <tr style={{ backgroundColor: "#f7f7f7" }}>
            <td style={{ padding: 4, border: "1px solid #ccc" }}>
              <input
                type="date"
                name="Date"
                value={entry.Date}
                onChange={onChange}
                style={{
                  width: "100%",
                  padding: 6,
                  borderRadius: 3,
                  border: "1px solid #ccc",
                }}
              />
            </td>
            <td style={{ padding: 4, border: "1px solid #ccc" }}>
              <input
                type="text"
                name="Description"
                value={entry.Description}
                onChange={onChange}
                placeholder="Description"
                style={{
                  width: "100%",
                  padding: 6,
                  borderRadius: 3,
                  border: "1px solid #ccc",
                }}
              />
            </td>
            <td style={{ padding: 4, border: "1px solid #ccc" }}>
              <input
                type="number"
                name="Amount"
                value={entry.Amount}
                onChange={onChange}
                placeholder="Amount"
                step="0.01"
                style={{
                  width: "100%",
                  padding: 6,
                  borderRadius: 3,
                  border: "1px solid #ccc",
                  textAlign: "right",
                }}
              />
            </td>
            <td style={{ padding: 4, border: "1px solid #ccc" }}>
              <select
                name="Category"
                value={entry.Category}
                onChange={onChange}
                style={{
                  width: "100%",
                  padding: 6,
                  borderRadius: 3,
                  border: "1px solid #ccc",
                }}
              >
                {categoryOptions.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </td>
            <td
              style={{
                padding: 4,
                border: "1px solid #ccc",
                textAlign: "center",
              }}
            >
              <button
                onClick={onAdd}
                style={{
                  padding: "6px 12px",
                  backgroundColor: "#0078d7",
                  color: "white",
                  border: "none",
                  borderRadius: 3,
                  cursor: "pointer",
                }}
              >
                ➕
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div style={{ marginBottom: "15px" }}>
        <div
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "center",
            marginBottom: "8px",
            flexWrap: "wrap",
          }}
        >
          <input type="file" accept=".csv" onChange={onFileUpload} />
          <button
            onClick={downloadSampleCSV}
            style={{
              padding: "8px 16px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "600",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = "#218838";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = "#28a745";
            }}
          >
            📄 Download Sample CSV (1000 entries)
          </button>
          <button
            onClick={() => setShowVideo(true)}
            style={{
              padding: "8px 16px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "600",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = "#0056b3";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = "#007bff";
            }}
          >
            🎥 Watch Instruction Video
          </button>
        </div>
        <div
          style={{
            fontSize: "12px",
            color: "#666",
            backgroundColor: "#f8f9fa",
            padding: "8px",
            borderRadius: "4px",
            border: "1px solid #e9ecef",
          }}
        >
          <strong>💡 Sample CSV includes:</strong> 1000 realistic transactions
          across Dining, Shopping, Transportation, Subscriptions, Utilities,
          Health, Housing, and Income categories from Jan-June 2024. Perfect for
          testing all features!
        </div>
      </div>
      {loading && <p style={{ marginTop: 8 }}>Processing… ⏳</p>}

      {/* Video Modal */}
      {showVideo && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
          onClick={() => setShowVideo(false)}
        >
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "8px",
              padding: "20px",
              maxWidth: "90vw",
              maxHeight: "90vh",
              position: "relative",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowVideo(false)}
              style={{
                position: "absolute",
                top: "10px",
                right: "15px",
                background: "none",
                border: "none",
                fontSize: "24px",
                cursor: "pointer",
                color: "#666",
                zIndex: 1001,
              }}
            >
              ×
            </button>
            <h3 style={{ margin: "0 0 15px 0", color: "#333" }}>
              📚 How to Use the Expense Tracker
            </h3>
            <video
              controls
              style={{
                width: "100%",
                maxWidth: "800px",
                height: "auto",
                borderRadius: "4px",
              }}
            >
              <source src="/video.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <div style={{ marginTop: "15px", fontSize: "14px", color: "#666" }}>
              <strong>💡 Quick Tips:</strong>
              <ul style={{ margin: "8px 0", paddingLeft: "20px" }}>
                <li>
                  Upload your CSV file or use the sample data to get started
                </li>
                <li>
                  Click on categories in the pie chart to filter transactions
                </li>
                <li>
                  Use the toggle to switch between spending and earning views
                </li>
                <li>
                  Check the Savings Analyzer for personalized recommendations
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </CardLayout>
  );
}
