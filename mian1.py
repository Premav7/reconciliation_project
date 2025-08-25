import os
import operator
from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.reconciliation_agent import get_reconciliation_agent
from agents.report_generation_agent import get_report_generation_agent
from tools.file_tools import read_excel_data, read_pdf_data
from langsmith import traceable


# Define the State
class AgentState(TypedDict):
    """
    Represents the state of our graph.
    """
    input: str
    reconciliation_data: str
    final_report: str

# Step 1: Read the files locally using the tools.
# This happens BEFORE we invoke the agent.
try:
    # --- CORRECTED FILE PATHS ---
    erp_data_string = read_excel_data('data/erp_data.xlsx')
    bank_statement_data_string = read_pdf_data('data/bank_statement.pdf')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure the files are in the correct directory (e.g., 'data/').")
    exit()

# Combine the data into a single string for the agent's input
combined_data = f"""
ERP Data:
{erp_data_string}

Bank Statement Data:
{bank_statement_data_string}
"""

# Create the Agents
reconciliation_agent = get_reconciliation_agent()
report_generation_agent = get_report_generation_agent()

# Define the Nodes
def reconcile_data_node(state):
    """Node to run the reconciliation agent."""
    print("---EXECUTING RECONCILIATION AGENT---")
    result = reconciliation_agent.invoke({"input": state["input"]})
    return {"reconciliation_data": result['output']}
@traceable(name="reconcilation")
def generate_report_node(state):
    """Node to run the report generation agent."""
    print("---EXECUTING REPORT GENERATION AGENT---")
    result = report_generation_agent.invoke({"input": state["reconciliation_data"]})
    return {"final_report": result['output']}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("reconciliation", reconcile_data_node)
workflow.add_node("report_generation", generate_report_node)
workflow.set_entry_point("reconciliation")
workflow.add_edge("reconciliation", "report_generation")
workflow.add_edge("report_generation", END)
app = workflow.compile()

# Run the app with the combined data string
final_output = app.invoke({"input": combined_data})

# Get the final report string
final_report_string = final_output['final_report']

# Split the output into the Markdown report and CSV data
try:
    report_content, csv_content = final_report_string.split("---CSV-OUTPUT---")
except ValueError:
    print("Error: Could not split the output. The agent's output format may have changed.")
    report_content = final_report_string
    csv_content = ""

# Create the output directory if it does not exist
output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\n--- Created directory: {output_dir} ---")

# Save the Markdown report to a file
report_file_path = os.path.join(output_dir, "reconciliation_report.md")
with open(report_file_path, "w", encoding="utf-8") as f:
    f.write(report_content)
    print(f"\n--- Markdown report saved to {report_file_path} ---")

# Save the CSV data to a file
csv_file_path = os.path.join(output_dir, "output_csv.csv")
with open(csv_file_path, "w", encoding="utf-8") as f:
    f.write(csv_content.strip())
    print(f"\n--- CSV results saved to {csv_file_path} ---")

print("\n--- FINAL RECONCILIATION OUTPUT (printed to console) ---")
print(final_report_string)