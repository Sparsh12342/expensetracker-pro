// Shared types
export interface FirstWordSummary {
  FirstWord: string;
  TotalDeposits?: number;
  TotalWithdrawals?: number;
}
export interface DepositCluster {
  Cluster_Label: string;
  TotalDeposits: number;
}
export interface WithdrawalCluster {
  Cluster_Label: string;
  TotalWithdrawals: number;
}
export interface CategorySummary {
  Category: string;
  TransactionCount: number;
  TotalAmount: number;
  Withdrawals: number;
  Deposits: number;
};
export type PredRow = {
  Date: string;
  Description: string;
  Amount: string | number;
  PredictedCategory: string;
  Confidence?: number;
};

export interface SummaryData {
  total_deposits: number;
  total_withdrawals: number;
  num_deposits: number;
  num_withdrawals: number;
  deposits_grouped_by_first_word: FirstWordSummary[];
  withdrawals_grouped_by_first_word: FirstWordSummary[];
  deposits_grouped_by_cluster: DepositCluster[];
  withdrawals_grouped_by_cluster: WithdrawalCluster[];
  category_summary: CategorySummary[];   // server pie data
  entries_with_pred?: PredRow[];         // per-row predictions (optional)
};
