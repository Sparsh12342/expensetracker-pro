export const categoryOptions = [
  "Bars & Pubs",
  "Clothing & Apparel",
  "Food & Dining",
  "Retail",
  "Transfers",
] as const;

export const pieColors: Record<string, string> = {
  "Bars & Pubs": "#ff9999",
  "Clothing & Apparel": "#66b3ff",
  "Food & Dining": "#99ff99",
  Retail: "#ffcc99",
  Transfers: "#c299ff",
};

export const getCategoryColor = (cat: string) =>
  ({
    "Bars & Pubs": "#ffe5e5",
    "Clothing & Apparel": "#e5f0ff",
    "Food & Dining": "#e5ffe5",
    Retail: "#fff5cc",
    Transfers: "#f0e5ff",
  }[cat] || "#f9f9f9");

export const getPieColor = (cat: string) => pieColors[cat] || "#dddddd";
