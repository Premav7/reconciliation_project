import pandas as pd
import pdfplumber
from pathlib import Path

def load_erp_data(filepath: str) -> pd.DataFrame:

    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip() 
    return df


def load_bank_statement(filepath: str) -> pd.DataFrame:

    rows = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                headers = table[0]
                for row in table[1:]:
                    if len(row) == len(headers):
                        rows.append(row)

    df = pd.DataFrame(rows, columns=["Date", "Description", "Amount", "Ref ID"])
    
    # Clean up
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Ref ID"] = df["Ref ID"].astype(str).str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()

    return df


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parents[1] / "data"
    
    erp_df = load_erp_data(base_path / "erp_data.xlsx")
    bank_df = load_bank_statement(base_path / "bank_statement.pdf")

    print("ERP Data Sample:")
    print(erp_df.head(208))
    print(erp_df.describe())
    print(erp_df.size)

    print("\nBank Statement Sample:")
    print(bank_df.head())
    print(bank_df.describe())
    print(bank_df.size)
