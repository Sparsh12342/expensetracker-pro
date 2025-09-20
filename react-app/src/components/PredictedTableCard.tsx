import React from "react";

type Pred = {
  Date: string;
  Description: string;
  Amount: string | number;
  PredictedCategory: string;
  Confidence?: number;
};

type Props = {
  rows: Pred[];
  onFix: (idx: number, correctCategory: string) => void;
  labels: string[]; // available categories (can come from /nlp/labels)
};

const card: React.CSSProperties = {
  border: "1px solid #e5e7eb",
  borderRadius: 12,
  padding: 12,
  background: "#fff",
};
const thtd: React.CSSProperties = {
  padding: "8px 10px",
  borderBottom: "1px solid #eee",
  fontSize: 13,
};

export default function PredictedTableCard({ rows, onFix, labels }: Props) {
  return (
    <div style={card}>
      <h3 style={{ margin: "2px 0 10px", fontSize: 16, fontWeight: 600 }}>
        Model Predictions (fix any)
      </h3>
      <div style={{ overflow: "auto", maxHeight: 360 }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={thtd}>Date</th>
              <th style={thtd}>Description</th>
              <th style={thtd}>Amount</th>
              <th style={thtd}>Predicted</th>
              <th style={thtd}>Confidence</th>
              <th style={thtd}>Fix</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td style={thtd}>{r.Date}</td>
                <td style={thtd}>{r.Description}</td>
                <td style={thtd}>{r.Amount}</td>
                <td style={thtd}>{r.PredictedCategory}</td>
                <td style={thtd}>
                  {r.Confidence != null
                    ? (r.Confidence * 100).toFixed(0) + "%"
                    : "-"}
                </td>
                <td style={thtd}>
                  <select
                    defaultValue={r.PredictedCategory}
                    onChange={(e) => onFix(i, e.target.value)}
                  >
                    {labels.map((l) => (
                      <option key={l} value={l}>
                        {l}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td style={thtd} colSpan={6}>
                  No predicted rows to review.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
