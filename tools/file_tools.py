import pandas as pd
from langchain_core.tools import tool
import pdfplumber
import json
import numpy as np

@tool
def read_excel_data(file_path: str) -> str:
    """
    Reads data from an Excel (.xlsx) file and returns it as a valid CSV string.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_csv(index=False)
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def read_pdf_data(file_path: str) -> str:
    """
    Reads text content from a PDF, cleans it, and returns it as a valid CSV string.
    """
    rows = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    for row in table[1:]:
                        if len(row) == 4:
                            rows.append(row)
        df = pd.DataFrame(rows, columns=["Date", "Description", "Amount", "Ref ID"])
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Ref ID"] = df["Ref ID"].astype(str).str.strip()
        df["Description"] = df["Description"].astype(str).str.strip()
        return df.to_csv(index=False)
    except Exception as e:
        return f"Error reading file: {e}"

def convert_types(obj):
    if isinstance(obj, list):
        return [convert_types(item) for item in obj]
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    if isinstance(obj, (pd.Timestamp,)):
        return str(obj)
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    return obj

@tool
def analyze_reconciliation_data(erp_data: str, bank_data: str) -> str:
    """
    Analyzes ERP and bank statement data to find matched, missing, amount mismatches,
    duplicates, non-invoice transactions, rounding differences, and negative transactions.
    Returns a JSON string with all reconciliation results.
    """
    try:
        erp_df = pd.read_csv(pd.io.common.StringIO(erp_data))
        print(erp_df    )
        bank_df = pd.read_csv(pd.io.common.StringIO(bank_data))

        erp_df.rename(columns={'Date': 'erp_date', 'Invoice ID': 'erp_invoice_id', 'Amount': 'erp_amount', 'Status': 'erp_status'}, inplace=True)
        bank_df.rename(columns={'Date': 'bank_date', 'Description': 'bank_description', 'Amount': 'bank_amount', 'Ref ID': 'bank_ref_id'}, inplace=True)

        erp_map = {str(row['erp_invoice_id']).strip(): row for _, row in erp_df.iterrows()}
        bank_map = {str(row['bank_description']).strip(): row for _, row in bank_df.iterrows() if str(row['bank_description']).startswith('INV')}

        matched = []
        amount_mismatches = []
        missing_in_bank = []
        missing_in_erp = []

        for erp_id, erp_row in erp_map.items():
            bank_row = bank_map.get(erp_id)
            if bank_row is None:
                missing_in_bank.append(erp_row.to_dict())
            else:
                erp_amt = erp_row['erp_amount']
                bank_amt = bank_row['bank_amount']
                # Use tolerance for matching (e.g., 0.01)
                if abs(erp_amt - bank_amt) < 0.01:
                    matched.append({**erp_row, **bank_row})
                else:
                    amount_mismatches.append({
                        "erp_invoice_id": erp_id,
                        "erp_date": erp_row.get('erp_date', ''),
                        "erp_amount": erp_amt,
                        "bank_ref_id": bank_row.get('bank_ref_id', ''),
                        "bank_date": bank_row.get('bank_date', ''),
                        "bank_description": bank_row.get('bank_description', ''),
                        "bank_amount": bank_amt,
                        "difference": bank_amt - erp_amt
                    })

        for bank_id, bank_row in bank_map.items():
            if bank_id not in erp_map:
                missing_in_erp.append(bank_row.to_dict())

        non_invoice_transactions = bank_df[~bank_df['bank_description'].str.contains('INV', na=False, case=False)].to_dict('records')

        bank_duplicates = bank_df[bank_df.duplicated(['bank_description', 'bank_amount'], keep=False)].to_dict('records')

        rounding_diffs = []
        for erp_id, erp_row in erp_map.items():
            bank_row = bank_map.get(erp_id)
            if bank_row is not None:
                erp_amt = erp_row['erp_amount']
                bank_amt = bank_row['bank_amount']
                diff = abs(bank_amt - erp_amt)
                if 0.10 < diff < 1.00:
                    rounding_diffs.append({
                        "erp_invoice_id": erp_id,
                        "bank_ref_id": bank_row.get('bank_ref_id', ''),
                        "difference": bank_amt - erp_amt
                    })

        # Negative transactions
        negative_transactions = {
            "erp_negatives": erp_df[erp_df['erp_amount'] < 0].to_dict('records'),
            "bank_negatives": bank_df[bank_df['bank_amount'] < 0].to_dict('records')
        }

        reconciliation_results = {
            "matched_transactions": matched,
            "missing_in_bank": missing_in_bank,
            "missing_in_erp": missing_in_erp,
            "amount_mismatches": amount_mismatches,
            "non_invoice_transactions": non_invoice_transactions,
            "duplicates_in_bank": bank_duplicates,
            "rounding_differences": rounding_diffs,
            "negative_transactions": negative_transactions
        }
        reconciliation_results = convert_types(reconciliation_results)
        return json.dumps(reconciliation_results, indent=2)

    except Exception as e:
        return f"Error during reconciliation analysis: {e}"

if __name__ == "__main__":
    erp_data = """Date,Invoice ID,Amount,Status
2024-08-01,INV0001,1000.00,Paid
2024-08-02,INV0002,2000.00,Paid
2024-08-03,INV0003,1500.00,Unpaid
2024-08-04,INV0004,-2500.00,Cancelled
"""

    bank_data = """Date,Description,Amount,Ref ID
2024-08-01,INV0001,-1000.11,101
2024-08-02,INV0002,2000.00,102
2024-08-02,INV0002,2000.00,102
2024-08-03,INV0003,1500.11,103
2024-08-05,INV0005,3000.00,104
2024-08-04,Other,-500.00,103
2024-08-06,other,2500.00,105
"""

    result = analyze_reconciliation_data(erp_data, bank_data)
    print("\n=== Reconciliation Results ===\n")
    print(result)