import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATA_PATHS = {
    "bank": "data/bank_statement.pdf",
    "erp": "data/erp_data.xlsx"
}

OUTPUT_PATHS = {
    "reconciliation": "outputs/reconciliation_results.csv",
    "report": "outputs/final_report.md"
}

# Load model name from env, fallback to default 'gpt-4o'
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Example: API key (for LangChain/OpenAI integrations)
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# You can then configure your LangChain ChatOpenAI initialization using these env vars:
# llm = ChatOpenAI(model_name=MODEL_NAME, openai_api_key=OPENAI_API_KEY)
