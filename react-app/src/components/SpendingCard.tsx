import React from "react";
import CardLayout from "./CardLayout";

export default function SpendingCard() {
  const total = 1234.56; // inject via props later
  return (
    <CardLayout title="Total Spending">
      <div style={{ fontSize: 28, fontWeight: 700 }}>${total.toFixed(2)}</div>
      <div style={{ color: "#666", marginTop: 6 }}>This month</div>
    </CardLayout>
  );
}
