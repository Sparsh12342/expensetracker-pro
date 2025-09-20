import React from "react";

type Item = { source: string; title: string; link: string };

export default function SavingsCard({ items }: { items: Item[] }) {
  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 12,
        background: "#fff",
      }}
    >
      <h3 style={{ margin: "2px 0 10px", fontSize: 16, fontWeight: 600 }}>
        Save More (suggestions)
      </h3>
      {items.length === 0 ? (
        <div style={{ color: "#6b7280", fontSize: 14 }}>
          No suggestions yet.
        </div>
      ) : (
        <ul style={{ margin: 0, paddingLeft: 16 }}>
          {items.map((it, i) => (
            <li key={i} style={{ marginBottom: 8 }}>
              <a
                href={it.link}
                target="_blank"
                rel="noreferrer"
                style={{ textDecoration: "none" }}
              >
                {it.title}
              </a>
              <div style={{ fontSize: 12, color: "#6b7280" }}>{it.source}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
