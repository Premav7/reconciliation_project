import pandas as pd
import re
from src.data_loader import load_erp_data, load_bank_statement
import os


def extract_invoice_id(description: str) -> str:
    """Extract invoice ID (e.g., INV0001) from bank description text."""
    if pd.isna(description):
        return None
    match = re.search(r"(INV\d+)", description)
    return match.group(1) if match else None


def reconcile_data(erp_df: pd.DataFrame, bank_df: pd.DataFrame, output_path="outputs/reconciled.csv") -> pd.DataFrame:
    erp_df = erp_df.copy()
    bank_df = bank_df.copy()

    # Extract invoice ID
    bank_df["Invoice ID"] = bank_df["Description"].apply(extract_invoice_id)

    # Clean amounts
    erp_df["Amount"] = pd.to_numeric(erp_df["Amount"], errors="coerce").round(2)
    bank_df["Amount"] = pd.to_numeric(bank_df["Amount"], errors="coerce").round(2)

    # --- Duplicate checks before merge ---
    bank_dupes = bank_df[bank_df.duplicated(subset=["Invoice ID", "Amount"], keep=False)]
    erp_dupes = erp_df[erp_df.duplicated(subset=["Invoice ID", "Amount"], keep=False)]

    # --- Merge on Invoice ID ---
    merged = pd.merge(
        erp_df,
        bank_df,
        on="Invoice ID",
        how="outer",
        suffixes=("_ERP", "_BANK"),
        indicator=True
    )

    # --- Classification ---
    conditions = []
    for _, row in merged.iterrows():
        if row["_merge"] == "both":
            if row.get("Status", "") == "Cancelled" and not pd.isna(row["Amount_BANK"]):
                conditions.append("ERP Cancellation Conflict")
            elif abs(row["Amount_ERP"] - row["Amount_BANK"]) < 0.01:
                conditions.append("Match")
            elif abs(row["Amount_ERP"] - row["Amount_BANK"]) <= 1:
                conditions.append("Rounding Difference")
            else:
                conditions.append("Amount Mismatch")

            if "Date_ERP" in row and "Date_BANK" in row:
                try:
                    if abs((row["Date_ERP"] - row["Date_BANK"]).days) > 2:
                        conditions[-1] = "Date Mismatch"
                except:
                    pass
        elif row["_merge"] == "left_only":
            conditions.append("Missing in Bank")
        elif row["_merge"] == "right_only":
            # Bank-only record
            if pd.isna(row["Invoice ID"]) or not re.match(r"INV\d+", str(row["Invoice ID"])):
                conditions.append("Non-Invoice Transaction")
            else:
                conditions.append("Missing in ERP")

        else:
            conditions.append("Unknown")

    merged["Reconciliation_Status"] = conditions
    # After reconciliation is done
# Reorder columns to have Invoice ID first
    cols = merged.columns.tolist()
    if "Invoice ID" in cols:
        cols.remove("Invoice ID")
        merged = merged[["Invoice ID"] + cols]

    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to CSV
    merged.to_csv(output_path, index=False)



    return merged




def summarize_reconciliation(reconciled_df: pd.DataFrame,erp_df: pd.DataFrame, bank_df: pd.DataFrame) -> dict:
    """
    Generate summary statistics of reconciliation results,
    including duplicates in ERP and Bank.
    """
    summary = reconciled_df["Reconciliation_Status"].value_counts().to_dict()
    total = len(reconciled_df)
    matches = summary.get("Match", 0)
    reconciliation_rate = round((matches / total) * 100, 2) if total > 0 else 0.0

    bank_dupes = bank_df[
        bank_df["Invoice ID"].notna() &
        bank_df.duplicated(subset=["Invoice ID", "Amount"], keep='first')
    ]
    erp_dupes = erp_df[
        erp_df["Invoice ID"].notna() &
        erp_df.duplicated(subset=["Invoice ID", "Amount"], keep='first')
    ]

    reconciled_df["Is_Duplicate_Bank"] = reconciled_df["Invoice ID"].isin(['right_only','both'])
    reconciled_df["Is_Duplicate_ERP"] = reconciled_df["Invoice ID"].isin(['left_only','both']) 


    lenn=len(bank_dupes)
    lenn1=len(erp_dupes)



    return {
        "total_records": total,
        "matches": matches,
        "reconciliation_rate": reconciliation_rate,
        "issues": summary,
        "duplicates": {
            "bank_duplicates": lenn,
            "erp_duplicates": lenn1
        }
    }



if __name__ == "__main__":
    from pathlib import Path
    from data_loader import load_erp_data, load_bank_statement

    base_path = Path(__file__).resolve().parents[1] / "data"
    erp_df = load_erp_data(base_path / "erp_data.xlsx")
    bank_df = load_bank_statement(base_path / "bank_statement.pdf")

    reconciled = reconcile_data(erp_df, bank_df)
        # Extract invoice ID
    bank_df["Invoice ID"] = bank_df["Description"].apply(extract_invoice_id)

    # Clean amounts
    erp_df["Amount"] = pd.to_numeric(erp_df["Amount"], errors="coerce").round(2)
    bank_df["Amount"] = pd.to_numeric(bank_df["Amount"], errors="coerce").round(2)

    # Save reconciled result to CSV file
    reconciled.to_csv(base_path / "reconciled_report.csv", index=False)

    print(reconciled)

    summary = summarize_reconciliation(reconciled,erp_df,bank_df)
    print("\nSummary:", summary)
