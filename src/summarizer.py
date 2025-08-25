import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts.chat import ChatPromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def summarize_summary(summary: dict) -> str:
    """
    Uses Gemini API (via LangChain Runnable) to generate
    a natural language summary of reconciliation results.
    """

    if not GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY. Please set it in .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    report_prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are a financial reconciliation analyst. "
        "Your task is to produce a short professional report (1–2 pages). "
        "The report must include:\n"
        "1. Overall reconciliation rate\n"
        "2. Summary of issues found\n"
        "3. Recommendations for improvement\n\n"
        "Write in clear, concise, and professional language with headings."),
        
        ("user", 
        "Here is the reconciliation summary JSON:\n\n{summary}\n\n"
        "Please generate the report now.")
    ])

    chain = (
        {"summary": RunnablePassthrough()}  
        | report_prompt
        | llm
    )

    result = chain.invoke(summary)

    return result.content



if __name__ == "__main__":
    from reconciliation import reconcile_data, summarize_reconciliation,extract_invoice_id
    from data_loader import load_erp_data, load_bank_statement
    from pathlib import Path
    import pandas as pd

    base_path = Path(__file__).resolve().parents[1] / "data"

    erp_df = load_erp_data(base_path / "erp_data.xlsx")
    bank_df = load_bank_statement(base_path / "bank_statement.pdf")

    bank_df["Invoice ID"] = bank_df["Description"].apply(extract_invoice_id)

    erp_df["Amount"] = pd.to_numeric(erp_df["Amount"], errors="coerce").round(2)
    bank_df["Amount"] = pd.to_numeric(bank_df["Amount"], errors="coerce").round(2)

    reconciled_df = reconcile_data(erp_df, bank_df)
    summary = summarize_reconciliation(reconciled_df, erp_df, bank_df)

    print("Reconciliation Summary:")
    print(summary)

    print("\nGenerated Report:")
    report = summarize_summary(summary)
    print(report)
