import React from "react";

type Props = {
  title: string;
  children: React.ReactNode;
};

export default function CardLayout({ title, children }: Props) {
  return (
    <section
      style={{
        background: "white",
        border: "1px solid #e5e5e5",
        borderRadius: 10,
        boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
        padding: 12,
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 8 }}>{title}</div>
      {children}
    </section>
  );
}
