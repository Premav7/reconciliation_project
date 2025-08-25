from typing import TypedDict

class ReconciliationState(TypedDict):
    erp_df: object
    bank_df: object
    summary: dict
    report_text: str
    pdf_path: str
