import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools.file_tools import read_excel_data, read_pdf_data # Import necessary tools
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_report_generation_agent():
    """
    Creates and returns a report generation agent.
    """
    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )
    # 2. Define the Agent's Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert financial report generation agent. Your task is to create a detailed, human-readable reconciliation summary and a CSV file from a structured JSON object.

                You will receive a JSON object containing the reconciliation results, with keys such as `matched_transactions`, `missing_in_erp`, `missing_in_bank`, `amount_mismatches`, `date_differences`, and `duplicates`,`negative_transactions`.

                Your workflow should be as follows:
                1.  Parse the input JSON object to understand the reconciliation results
                2.  Generate a comprehensive summary report in markdown format. This report should include:
                    -   A heading for the summary.
                    -   A section for "Matched Transactions" stating the total number of matches.
                    -   Overall reconciliation rate as a percentage.
                    -   A separate section for each type of discrepancy found (`Missing in ERP`, `Missing in Bank`, `Amount Mismatch`, `Date Difference`, `Duplicates`,`negative_transactions`).
                    -   For each discrepancy, clearly list the affected transactions and provide a brief explanation.
                3.  Create a single, consolidated CSV string with the following columns: `ERP_Date`, `ERP_InvoiceID`, `ERP_Amount`, `Bank_Date`, `Bank_Amount`, `Discrepancy_Type`, `Reasoning`.
                4.  Your final output should be a single string containing the markdown report followed by the CSV string, clearly separated by a delimiter like "---CSV-OUTPUT---".
                """
            ),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # 3. Create the Agent
    # This agent does not use any external tools; it's a pure generation agent.
    tools=[]
    agent = create_tool_calling_agent(llm,[], prompt)
    
    return AgentExecutor(agent=agent, tools=[], verbose=True)

# Note: This is a function that returns the agent. You will call this from main.py