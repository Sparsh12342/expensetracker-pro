import React from "react";
import CardLayout from "./CardLayout";

export default function IncomeCard() {
  const income = 2750.0; // inject via props later
  return (
    <CardLayout title="Income">
      <div style={{ fontSize: 28, fontWeight: 700 }}>${income.toFixed(2)}</div>
      <div style={{ color: "#666", marginTop: 6 }}>This month</div>
    </CardLayout>
  );
}
