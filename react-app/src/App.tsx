import React, { useEffect, useMemo, useRef, useState } from "react";
import Papa from "papaparse";

import EntryFormCard from "./components/EntryFormCard";
import EntriesTableCard from "./components/EntriesTableCard";
import CategoryPieCard from "./components/CategoryPieCard";
import SavingsCard from "./components/SavingsCard";
import SavingsAnalyzer from "./components/SavingsAnalyzer";

import { categoryOptions } from "./constants";
import { SummaryData, CategorySummary, PredRow } from "./types";

const API = import.meta.env.VITE_API_URL || "http://localhost:5050";

// -------------------- helpers --------------------
const formatCurrency = (n: number) =>
  n >= 0 ? `$${n.toFixed(2)}` : `-$${Math.abs(n).toFixed(2)}`;

const sortByDateDesc = (rows: string[][]) =>
  [...rows].sort((a, b) => new Date(b[0]).getTime() - new Date(a[0]).getTime());

function emptyCat(cat: string): CategorySummary {
  return {
    Category: cat,
    TransactionCount: 0,
    TotalAmount: 0,
    Withdrawals: 0,
    Deposits: 0,
  };
}
function toArrayFromMap(m: Map<string, CategorySummary>) {
  return Array.from(m.values());
}
function addToSummary(summary: Map<string, CategorySummary>, row: string[]) {
  if (!row || row.length < 3) return;
  const cat = ((row[3] ?? "Uncategorized") as string).trim();
  const amt = Number(row[2] ?? 0);
  const rec = summary.get(cat) ?? emptyCat(cat);
  rec.TransactionCount += 1;
  rec.TotalAmount += amt;
  if (amt >= 0) rec.Deposits += amt;
  else rec.Withdrawals += amt;
  summary.set(cat, rec);
}
function withDefaultCategories(
  summaryArray: CategorySummary[]
): CategorySummary[] {
  const have = new Set(summaryArray.map((s) => s.Category));
  const zeros = categoryOptions
    .filter((c) => !have.has(c))
    .map((c) => emptyCat(c));
  return [...summaryArray, ...zeros];
}
function topNPlusOther(items: CategorySummary[], n = 10): CategorySummary[] {
  const sorted = [...items].sort(
    (a, b) => Math.abs(b.TotalAmount) - Math.abs(a.TotalAmount)
  );
  if (sorted.length <= n) return sorted;
  const top = sorted.slice(0, n);
  const rest = sorted.slice(n);
  const other: CategorySummary = {
    Category: "Other",
    TransactionCount: rest.reduce((s, r) => s + r.TransactionCount, 0),
    TotalAmount: rest.reduce((s, r) => s + r.TotalAmount, 0),
    Withdrawals: rest.reduce((s, r) => s + r.Withdrawals, 0),
    Deposits: rest.reduce((s, r) => s + r.Deposits, 0),
  };
  return [...top, other];
}
// summary from predicted rows
function summarizePredictedRows(rows: PredRow[]): CategorySummary[] {
  const byCat = new Map<string, CategorySummary>();
  for (const r of rows) {
    const cat = (r.PredictedCategory || "Uncategorized").trim();
    const amt = Number(r.Amount) || 0;
    if (!byCat.has(cat)) byCat.set(cat, emptyCat(cat));
    const rec = byCat.get(cat)!;
    rec.TransactionCount += 1;
    rec.TotalAmount += amt;
    amt >= 0 ? (rec.Deposits += amt) : (rec.Withdrawals += amt);
  }
  return Array.from(byCat.values());
}
// merchant tokens for savings
const extractMerchants = (
  rows: PredRow[] | string[][],
  limit = 12
): string[] => {
  const counts: Record<string, number> = {};
  const add = (s: string) => {
    // Improved regex to capture merchant names better
    (s.toLowerCase().match(/[a-z][a-z&'.-]+/g) || []).forEach((w) => {
      if (w.length < 3) return;
      if (
        [
          "transaction",
          "purchase",
          "payment",
          "debit",
          "credit",
          "online",
          "pos",
          "sale",
          "card",
          "store",
          "order",
          "transfer",
          "deposit",
          "withdrawal",
          "fee",
          "charge",
          "refund",
          "atm",
          "cash",
          "check",
          "ach",
          "wire",
        ].includes(w)
      )
        return;
      counts[w] = (counts[w] || 0) + 1;
    });
  };
  if (Array.isArray(rows) && rows.length && Array.isArray(rows[0])) {
    (rows as string[][]).forEach((r) => r[1] && add(String(r[1])));
  } else {
    (rows as PredRow[]).forEach(
      (r) => r.Description && add(String(r.Description))
    );
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([w]) => w);
};
// TS guard for predicted rows
const hasPredRows = (
  d: SummaryData | null
): d is SummaryData & { entries_with_pred: PredRow[] } =>
  !!d && Array.isArray((d as any).entries_with_pred);

// -------------------- inline review table --------------------
type PredictedTableProps = {
  rows: PredRow[];
  labels: string[];
  onFix: (rowIndex: number, correctCategory: string) => void;
};
const PredictedTableCard: React.FC<PredictedTableProps> = ({
  rows,
  labels,
  onFix,
}) => {
  // Filter for uncategorized transactions and sort by amount (highest first)
  const uncategorizedRows = rows
    .filter((r) => (r.PredictedCategory || "Uncategorized") === "Uncategorized")
    .sort((a, b) => {
      const amountA = Math.abs(Number(a.Amount) || 0);
      const amountB = Math.abs(Number(b.Amount) || 0);
      return amountB - amountA; // Sort descending (highest amounts first)
    });

  const card: React.CSSProperties = {
    border: "1px solid rgba(255, 255, 255, 0.2)",
    borderRadius: 16,
    padding: 20,
    background: "rgba(255, 255, 255, 0.15)",
    backdropFilter: "blur(10px)",
    boxShadow: "0 4px 16px rgba(0, 0, 0, 0.1)",
  };
  const thtd: React.CSSProperties = {
    padding: "12px 16px",
    borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
    fontSize: 14,
    color: "#87CEEB",
  };
  return (
    <div style={card}>
      <h3
        style={{
          margin: "2px 0 10px",
          fontSize: 18,
          fontWeight: 600,
          color: "#87CEEB",
        }}
      >
        Uncategorized Transactions ({uncategorizedRows.length})
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
            {uncategorizedRows.map((r, i) => {
              // Find the original index in the full rows array
              const originalIndex = rows.findIndex(
                (row) =>
                  row.Date === r.Date &&
                  row.Description === r.Description &&
                  row.Amount === r.Amount
              );
              return (
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
                      onChange={(e) => onFix(originalIndex, e.target.value)}
                    >
                      {labels.map((l) => (
                        <option key={l} value={l}>
                          {l}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              );
            })}
            {!uncategorizedRows.length && (
              <tr>
                <td style={thtd} colSpan={6}>
                  No uncategorized transactions to review.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// -------------------- main --------------------
export default function App() {
  const [serverData, setServerData] = useState<SummaryData | null>(null);
  const [useML, setUseML] = useState(true);

  const [loading, setLoading] = useState(false);
  const [entries, setEntries] = useState<string[][]>([]);
  const [entry, setEntry] = useState({
    Date: "",
    Description: "",
    Amount: "",
    Category: categoryOptions[0],
  });

  const [labels, setLabels] = useState<string[]>([
    "Dining",
    "Groceries",
    "Shopping",
    "Transportation",
    "Utilities",
    "Housing",
    "Health",
    "Entertainment",
    "Subscriptions",
    "Transfers",
    "Income",
    "Fees",
    "Travel",
    "Education",
    "Uncategorized",
  ]);

  const [showSavingsAnalyzer, setShowSavingsAnalyzer] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedFilterType, setSelectedFilterType] = useState<
    "all" | "spending" | "earning" | "category"
  >("all");
  const [showSpendingCategories, setShowSpendingCategories] = useState(true);

  const [savings, setSavings] = useState<
    { source: string; title: string; link: string }[]
  >([]);

  const summaryMapRef = useRef<Map<string, CategorySummary>>(new Map());

  // fetch label set once
  useEffect(() => {
    fetch(`${API}/nlp/labels`)
      .then((r) => r.json())
      .then((j) => {
        if (Array.isArray(j?.labels)) setLabels(j.labels);
      })
      .catch(() => {});
  }, []);

  // ---------- manual entry ----------
  const handleEntryChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setEntry((prev) => ({ ...prev, [name]: value }));
  };

  const addManualEntry = () => {
    if (!entry.Date || !entry.Description || !entry.Amount) return;
    const newRow: string[] = [
      entry.Date,
      entry.Description,
      entry.Amount,
      entry.Category,
    ];
    const newEntries = sortByDateDesc([newRow, ...entries]);
    setEntries(newEntries);
    addToSummary(summaryMapRef.current, newRow);
    setEntry({
      Date: "",
      Description: "",
      Amount: "",
      Category: categoryOptions[0],
    });
    void sendToBackend(newEntries);
  };

  // ---------- file upload (STREAMED) ----------
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);

    try {
      // Send the original file directly to the backend
      const form = new FormData();
      form.append("file", file);

      const res = await fetch(`${API}/upload-csv`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const json = (await res.json()) as SummaryData;
      console.log("Backend response:", json);
      console.log("Category summary from backend:", json.category_summary);
      setServerData(json);

      // Also parse the file for local display
      const newRows: string[][] = [];
      let skippedHeader = false;

      await new Promise<void>((resolve, reject) => {
        Papa.parse(file, {
          skipEmptyLines: true,
          worker: true,
          chunkSize: 1024 * 1024,
          chunk: (results) => {
            const rows = results.data as string[][];
            for (let i = 0; i < rows.length; i++) {
              const row = rows[i];
              if (!skippedHeader) {
                skippedHeader = true;
                const c0 = (row[0] || "").toLowerCase();
                const c1 = (row[1] || "").toLowerCase();
                const c2 = (row[2] || "").toLowerCase();
                if (
                  c0.includes("date") &&
                  c1.includes("desc") &&
                  c2.includes("amount")
                )
                  continue;
              }
              if (!row || row.length < 3) continue;
              newRows.push(row);
              addToSummary(summaryMapRef.current, row);
            }
          },
          complete: () => resolve(),
          error: (err) => reject(err),
        });
      });

      const combined = sortByDateDesc([...entries, ...newRows]);
      setEntries(combined);

      // --- Auto-refine "Uncategorized" using NLP microservice ---
      if (useML && hasPredRows(json) && json.entries_with_pred.length) {
        const uncats = json.entries_with_pred.filter(
          (r) => (r.PredictedCategory || "Uncategorized") === "Uncategorized"
        );
        if (uncats.length) {
          const refineResp = await fetch(`${API}/nlp/refine`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              rows: uncats.map((r) => ({
                Description: r.Description,
                Amount: r.Amount,
              })),
              threshold: 0.3,
            }),
          });
          const refined: Array<{
            PredictedCategory: string;
            Confidence: number;
          }> = await refineResp.json();

          let i = 0;
          const merged: PredRow[] = json.entries_with_pred.map((row) => {
            if (
              (row.PredictedCategory || "Uncategorized") === "Uncategorized"
            ) {
              const upd = refined[i++];
              return {
                ...row,
                PredictedCategory: upd.PredictedCategory,
                Confidence: upd.Confidence,
              };
            }
            return row;
          });

          const mlSummary = summarizePredictedRows(merged);
          setServerData({
            ...(serverData ?? {
              total_deposits: 0,
              total_withdrawals: 0,
              num_deposits: 0,
              num_withdrawals: 0,
              category_summary: [],
              entries_with_pred: [],
              deposits_grouped_by_first_word: [],
              withdrawals_grouped_by_first_word: [],
              deposits_grouped_by_cluster: [],
              withdrawals_grouped_by_cluster: [],
            }),
            category_summary: mlSummary,
            entries_with_pred: merged,
          });

          // savings based on ML categories + predicted rows
          void requestSavings(mlSummary, merged);
          setLoading(false);
          return;
        }
      }

      // otherwise request savings from whatever summary we have
      if (json.category_summary?.length) {
        void requestSavings(
          json.category_summary,
          hasPredRows(json) ? json.entries_with_pred : combined
        );
      }
    } catch (error) {
      console.error("Upload failed:", error);
    }

    setLoading(false);
  };

  // ---------- backend ----------
  const requestSavings = async (
    summary: CategorySummary[],
    rowsForMerchants: PredRow[] | string[][]
  ) => {
    try {
      const topCats = summary
        .slice(0, 5)
        .map((s) => s.Category)
        .filter(Boolean);
      const merchants = extractMerchants(rowsForMerchants, 12);
      const resp = await fetch(`${API}/savings/suggestions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ categories: topCats, merchants, max_items: 12 }),
      });
      const json = await resp.json();
      setSavings(Array.isArray(json.items) ? json.items : []);
    } catch (e) {
      console.error("savings fetch failed", e);
      setSavings([]);
    }
  };

  const sendToBackend = async (rows: string[][]) => {
    try {
      const headers = ["Date", "Description", "Amount", "Category"];
      const allData = [headers, ...rows];
      const blob = new Blob([Papa.unparse(allData)], { type: "text/csv" });
      const form = new FormData();
      form.append("file", blob, "combined.csv");

      const res = await fetch(`${API}/upload-csv`, {
        method: "POST",
        body: form,
      });
      const json = (await res.json()) as SummaryData;
      console.log("Backend response:", json);
      console.log("Category summary from backend:", json.category_summary);
      setServerData(json);

      // --- Auto-refine "Uncategorized" using NLP microservice ---
      if (useML && hasPredRows(json) && json.entries_with_pred.length) {
        const uncats = json.entries_with_pred.filter(
          (r) => (r.PredictedCategory || "Uncategorized") === "Uncategorized"
        );
        if (uncats.length) {
          const refineResp = await fetch(`${API}/nlp/refine`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              rows: uncats.map((r) => ({
                Description: r.Description,
                Amount: r.Amount,
              })),
              threshold: 0.3,
            }),
          });
          const refined: Array<{
            PredictedCategory: string;
            Confidence: number;
          }> = await refineResp.json();

          let i = 0;
          const merged: PredRow[] = json.entries_with_pred.map((row) => {
            if (
              (row.PredictedCategory || "Uncategorized") === "Uncategorized"
            ) {
              const upd = refined[i++];
              return {
                ...row,
                PredictedCategory: upd.PredictedCategory,
                Confidence: upd.Confidence,
              };
            }
            return row;
          });

          const mlSummary = summarizePredictedRows(merged);
          setServerData({
            ...(serverData ?? {
              total_deposits: 0,
              total_withdrawals: 0,
              num_deposits: 0,
              num_withdrawals: 0,
              category_summary: [],
              entries_with_pred: [],
              deposits_grouped_by_first_word: [],
              withdrawals_grouped_by_first_word: [],
              deposits_grouped_by_cluster: [],
              withdrawals_grouped_by_cluster: [],
            }),
            category_summary: mlSummary,
            entries_with_pred: merged,
          });

          // savings based on ML categories + predicted rows
          void requestSavings(mlSummary, merged);
          return;
        }
      }

      // otherwise request savings from whatever summary we have
      if (json.category_summary?.length) {
        void requestSavings(
          json.category_summary,
          hasPredRows(json) ? json.entries_with_pred : rows
        );
      }
    } catch (e) {
      console.error("Upload failed:", e);
    }
  };

  // feedback + optimistic update
  const handleFixCategory = async (
    rowIndex: number,
    correctCategory: string
  ) => {
    if (!hasPredRows(serverData)) return;
    const row = serverData.entries_with_pred[rowIndex];
    if (!row) return;

    const merged = serverData.entries_with_pred.map((r, i) =>
      i === rowIndex
        ? { ...r, PredictedCategory: correctCategory, Confidence: 1 }
        : r
    );
    const mlSummary = summarizePredictedRows(merged);
    setServerData({
      ...(serverData ?? {}),
      category_summary: mlSummary,
      entries_with_pred: merged,
    });

    void requestSavings(mlSummary, merged);

    try {
      await fetch(`${API}/nlp/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          samples: [
            {
              Description: row.Description,
              Amount: row.Amount,
              CorrectCategory: correctCategory,
            },
          ],
        }),
      });
    } catch (e) {
      console.error("feedback failed", e);
    }
  };

  // ---------- summaries for charts ----------
  const clientSummaryArray = useMemo(() => {
    const arr = toArrayFromMap(summaryMapRef.current);
    const result = withDefaultCategories(arr);
    console.log("clientSummaryArray calculation:");
    console.log("  - entries:", entries);
    console.log("  - summaryMapRef.current:", summaryMapRef.current);
    console.log("  - arr:", arr);
    console.log("  - result:", result);
    return result;
  }, [entries]);

  const effectiveSummary: CategorySummary[] = useMemo(() => {
    const fromServer = serverData?.category_summary ?? [];
    const base = useML && fromServer.length ? fromServer : clientSummaryArray;
    const result = topNPlusOther(base, 10);
    console.log("effectiveSummary calculation:");
    console.log("  - serverData:", serverData);
    console.log("  - fromServer:", fromServer);
    console.log("  - clientSummaryArray:", clientSummaryArray);
    console.log("  - useML:", useML);
    console.log("  - base:", base);
    console.log("  - result:", result);
    return result;
  }, [useML, serverData, clientSummaryArray]);

  // ---------- filtering logic ----------
  const handleSpendingClick = () => {
    setSelectedFilterType("spending");
    setSelectedCategory(null);
  };

  const handleEarningClick = () => {
    setSelectedFilterType("earning");
    setSelectedCategory(null);
  };

  const handleCategoryClick = (category: string | null) => {
    console.log("Category clicked:", category);
    console.log("Current entries sample:", entries.slice(0, 3));

    // Show all unique categories in entries
    const uniqueCategories = [
      ...new Set(entries.map((entry) => (entry[3] || "Uncategorized").trim())),
    ];
    console.log("All categories in entries:", uniqueCategories);
    console.log(
      "Is clicked category in entries?",
      uniqueCategories.includes(category || "")
    );

    // Enhanced debugging for category matching
    if (category) {
      const sampleEntries = entries.slice(0, 5).map((entry) => ({
        description: entry[1],
        category: entry[3],
        amount: entry[2],
      }));
      console.log("Sample entries with categories:", sampleEntries);

      // Check if there are any similar categories
      const similarCategories = uniqueCategories.filter(
        (cat) =>
          cat.toLowerCase().includes(category.toLowerCase()) ||
          category.toLowerCase().includes(cat.toLowerCase())
      );
      console.log("Similar categories found:", similarCategories);

      // If no exact match, try to find the best matching category
      if (!uniqueCategories.includes(category)) {
        console.log(
          "No exact match found. Available categories:",
          uniqueCategories
        );

        // Try to find the best match based on common patterns
        let bestMatch = null;
        const categoryLower = category.toLowerCase();

        // Look for partial matches
        for (const availableCategory of uniqueCategories) {
          const availableLower = availableCategory.toLowerCase();

          // Check if the clicked category contains words from available categories
          const availableWords = availableLower.split(/[\s&,]+/);
          const clickedWords = categoryLower.split(/[\s&,]+/);

          const hasCommonWords = availableWords.some((word) =>
            clickedWords.some(
              (clickedWord) =>
                word.includes(clickedWord) || clickedWord.includes(word)
            )
          );

          if (hasCommonWords) {
            bestMatch = availableCategory;
            break;
          }
        }

        if (bestMatch) {
          console.log(
            `Found best match: "${bestMatch}" for clicked category "${category}"`
          );
          setSelectedCategory(bestMatch);
          return;
        }
      }
    }

    setSelectedCategory(category);
    setSelectedFilterType(category ? "category" : "all");
  };

  const filteredEntries = useMemo(() => {
    let baseEntries: string[][] = [];

    // Get base entries (backend or regular)
    if (hasPredRows(serverData)) {
      baseEntries = serverData.entries_with_pred.map((entry) => [
        entry.Date,
        entry.Description,
        entry.Amount.toString(),
        entry.PredictedCategory || "Uncategorized",
      ]);
    } else {
      baseEntries = entries;
    }

    // Apply explicit spending/earning filter first (only if no category is selected)
    if (selectedFilterType === "spending" && !selectedCategory) {
      baseEntries = baseEntries.filter((entry) => {
        const amount = parseFloat(entry[2]);
        return amount < 0; // Negative amounts are spending
      });
      console.log(
        "Filtering for spending (negative amounts):",
        baseEntries.length
      );
    } else if (selectedFilterType === "earning" && !selectedCategory) {
      baseEntries = baseEntries.filter((entry) => {
        const amount = parseFloat(entry[2]);
        return amount > 0; // Positive amounts are earning
      });
      console.log(
        "Filtering for earning (positive amounts):",
        baseEntries.length
      );
    }
    // Apply toggle-based filter when no explicit filter is set and no category is selected
    else if (selectedFilterType === "all" && !selectedCategory) {
      if (showSpendingCategories) {
        // Show spending transactions when toggle is on "Spending"
        baseEntries = baseEntries.filter((entry) => {
          const amount = parseFloat(entry[2]);
          return amount < 0; // Negative amounts are spending
        });
        console.log(
          "Toggle: Showing spending transactions:",
          baseEntries.length
        );
      } else {
        // Show earning transactions when toggle is on "Earning"
        baseEntries = baseEntries.filter((entry) => {
          const amount = parseFloat(entry[2]);
          return amount > 0; // Positive amounts are earning
        });
        console.log(
          "Toggle: Showing earning transactions:",
          baseEntries.length
        );
      }
    }

    // Then apply category filter if selected
    if (selectedCategory && selectedFilterType === "category") {
      // Reset to show all entries first, then filter by category only
      baseEntries = baseEntries.filter((entry) => {
        const entryCategory = (entry[3] || "Uncategorized").trim();
        const match = entryCategory === selectedCategory;

        if (match) {
          console.log("✅ MATCH:", {
            entryCategory,
            selectedCategory,
            description: entry[1],
            amount: entry[2],
          });
        }

        return match;
      });

      console.log("Filtering for category:", selectedCategory);
      console.log("Category filtered entries:", baseEntries.length);
    }

    return baseEntries;
  }, [
    entries,
    selectedCategory,
    selectedFilterType,
    serverData,
    showSpendingCategories,
  ]);

  const filteredSummary = useMemo(() => {
    if (!selectedCategory) return effectiveSummary;

    // When a category is selected, show spending and earnings breakdown for that category
    const categorySummary = effectiveSummary.find((summary) => {
      const summaryCategory = summary.Category.trim();

      // Try exact match first
      let match = summaryCategory === selectedCategory;

      // If no exact match, try case-insensitive match
      if (!match) {
        match =
          summaryCategory.toLowerCase() === selectedCategory.toLowerCase();
      }

      // If still no match, try partial match (contains)
      if (!match) {
        match =
          summaryCategory
            .toLowerCase()
            .includes(selectedCategory.toLowerCase()) ||
          selectedCategory
            .toLowerCase()
            .includes(summaryCategory.toLowerCase());
      }

      return match;
    });

    if (categorySummary) {
      // Create spending and earning breakdown for the selected category
      const spendingBreakdown = {
        Category: `${categorySummary.Category} - Spending`,
        TransactionCount:
          Math.abs(categorySummary.Withdrawals) > 0
            ? Math.floor(
                categorySummary.TransactionCount *
                  (Math.abs(categorySummary.Withdrawals) /
                    Math.abs(categorySummary.TotalAmount))
              )
            : 0,
        TotalAmount: Math.abs(categorySummary.Withdrawals),
        Withdrawals: categorySummary.Withdrawals,
        Deposits: 0,
      };

      const earningBreakdown = {
        Category: `${categorySummary.Category} - Earning`,
        TransactionCount:
          categorySummary.Deposits > 0
            ? Math.floor(
                categorySummary.TransactionCount *
                  (categorySummary.Deposits /
                    Math.abs(categorySummary.TotalAmount))
              )
            : 0,
        TotalAmount: categorySummary.Deposits,
        Withdrawals: 0,
        Deposits: categorySummary.Deposits,
      };

      const breakdown = [];
      if (spendingBreakdown.TotalAmount > 0) breakdown.push(spendingBreakdown);
      if (earningBreakdown.TotalAmount > 0) breakdown.push(earningBreakdown);

      console.log("Category breakdown for:", selectedCategory, breakdown);
      return breakdown;
    }

    console.log("No matching category found for:", selectedCategory);
    return [];
  }, [effectiveSummary, selectedCategory]);

  // Always refresh savings whenever the summary we chart changes
  useEffect(() => {
    if (!effectiveSummary.length) return;
    const rowsForMerchants = hasPredRows(serverData)
      ? serverData.entries_with_pred
      : entries;
    void requestSavings(effectiveSummary, rowsForMerchants);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    JSON.stringify(effectiveSummary),
    hasPredRows(serverData) ? serverData?.entries_with_pred : entries,
  ]);

  // -------------------- layout --------------------
  return (
    <div className="app-container floating">
      <h1
        className="gradient-text"
        style={{
          textAlign: "center",
          marginBottom: 12,
          fontSize: "2.5rem",
          fontWeight: "700",
        }}
      >
        🏦 Spending Summary
      </h1>

      {/* ML toggle */}
      <div
        className="card"
        style={{
          display: "flex",
          gap: 12,
          alignItems: "center",
          margin: "4px 0 12px",
          padding: "16px 20px",
        }}
      >
        <label
          style={{
            fontWeight: 600,
            color: "#87CEEB",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <input
            type="checkbox"
            checked={useML}
            onChange={(e) => setUseML(e.target.checked)}
            style={{
              marginRight: 6,
              transform: "scale(1.2)",
              accentColor: "#667eea",
            }}
          />
          Use ML categories (auto-refine "Uncategorized" & learn from fixes)
        </label>

        {/* Clear Filter Button */}
        {(selectedCategory || selectedFilterType !== "all") && (
          <button
            onClick={() => {
              setSelectedCategory(null);
              setSelectedFilterType("all");
            }}
            style={{
              padding: "8px 16px",
              backgroundColor: "#ff6b6b",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "12px",
              fontWeight: "600",
            }}
          >
            🗑️ Clear Filter ({selectedCategory || selectedFilterType})
            <br />
            <small style={{ fontSize: "10px", opacity: 0.8 }}>
              Showing {filteredEntries.length} entries
            </small>
          </button>
        )}

        {/* Debug: Show available categories */}
        {selectedCategory && filteredEntries.length === 0 && (
          <div
            style={{
              padding: "12px",
              backgroundColor: "#fff3cd",
              border: "1px solid #ffeaa7",
              borderRadius: "8px",
              fontSize: "12px",
              marginTop: "8px",
            }}
          >
            <strong>🔍 Debug Info:</strong>
            <br />
            Looking for: <strong>{selectedCategory}</strong>
            <br />
            Available categories in your data:
            <div style={{ marginTop: "4px" }}>
              {[
                ...new Set(
                  entries.map((entry) => (entry[3] || "Uncategorized").trim())
                ),
              ].map((cat, i) => (
                <span
                  key={i}
                  style={{
                    display: "inline-block",
                    padding: "2px 6px",
                    margin: "2px",
                    backgroundColor: "#e9ecef",
                    borderRadius: "4px",
                    fontSize: "11px",
                  }}
                >
                  {cat}
                </span>
              ))}
            </div>
            <small style={{ color: "#666" }}>
              💡 The Savings Analyzer might be using different category names
              than your actual data.
            </small>
          </div>
        )}

        {/* Savings Analyzer Button */}
        <button
          onClick={() => setShowSavingsAnalyzer(true)}
          style={{
            padding: "8px 16px",
            backgroundColor: "#51cf66",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "600",
          }}
        >
          💰 Find Savings Opportunities
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 20,
          alignItems: "start",
        }}
      >
        {/* Left column */}
        <div style={{ display: "grid", gap: 20 }}>
          <EntryFormCard
            entry={entry}
            loading={loading}
            onChange={handleEntryChange}
            onAdd={addManualEntry}
            onFileUpload={handleFileUpload}
          />
          <EntriesTableCard
            entries={filteredEntries}
            format={formatCurrency}
            isFiltered={!!selectedCategory}
            selectedCategory={selectedCategory}
            onCategoryClick={handleCategoryClick}
            allEntries={entries}
            pieChartCategories={effectiveSummary}
            backendEntries={
              hasPredRows(serverData) ? serverData.entries_with_pred : undefined
            }
          />

          {useML &&
          hasPredRows(serverData) &&
          serverData.entries_with_pred.length ? (
            <PredictedTableCard
              rows={serverData.entries_with_pred}
              labels={labels}
              onFix={handleFixCategory}
            />
          ) : null}
        </div>

        {/* Right column (sticky) */}
        <div
          style={{
            position: "sticky",
            top: 12,
            alignSelf: "start",
            display: "grid",
            gap: 20,
          }}
        >
          <CategoryPieCard
            data={filteredSummary}
            format={formatCurrency}
            onCategoryClick={handleCategoryClick}
            onSpendingClick={handleSpendingClick}
            onEarningClick={handleEarningClick}
            selectedCategory={selectedCategory}
            selectedFilterType={selectedFilterType}
            showSpendingCategories={showSpendingCategories}
            onToggleSpendingCategories={setShowSpendingCategories}
          />
          <SavingsCard items={savings} />
        </div>
      </div>

      {/* Savings Analyzer Modal */}
      {showSavingsAnalyzer && (
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
            padding: "20px",
          }}
        >
          <div
            style={{
              maxWidth: "800px",
              width: "100%",
              maxHeight: "90vh",
              overflow: "auto",
            }}
          >
            <SavingsAnalyzer
              transactions={entries.map((row) => ({
                Date: row[0],
                Description: row[1],
                Amount: parseFloat(row[2]) || 0,
                Category: row[3] || "Uncategorized",
              }))}
              onClose={() => setShowSavingsAnalyzer(false)}
              onCategoryClick={handleCategoryClick}
            />
            <div
              style={{
                margin: "20px 0",
                padding: "10px",
                background: "#f0f0f0",
                borderRadius: "8px",
              }}
            >
              <strong>Debug: App.tsx</strong>
              <br />
              Entries count: {entries.length}
              <br />
              Filtered entries count: {filteredEntries.length}
              <br />
              Selected category: {selectedCategory || "None"}
              <br />
              Categories in entries:{" "}
              {[
                ...new Set(
                  entries.map((entry) => (entry[3] || "Uncategorized").trim())
                ),
              ].join(", ")}
              <br />
              Categories in summary:{" "}
              {effectiveSummary.map((s) => s.Category).join(", ")}
              <br />
              Sample entry:{" "}
              {entries.length > 0 ? JSON.stringify(entries[0]) : "No entries"}
              <br />
              Sample filtered entry:{" "}
              {filteredEntries.length > 0
                ? JSON.stringify(filteredEntries[0])
                : "No filtered entries"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
