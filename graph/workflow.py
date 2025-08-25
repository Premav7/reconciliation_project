from langgraph.graph import StateGraph, END

from graph.state import ReconciliationState
from src.data_loader import load_erp_data, load_bank_statement
from src.reconciliation import reconcile_data, summarize_reconciliation
from src.summarizer import summarize_summary
from src.report_generator import save_report_to_pdf


# ---- Define Nodes ----
def load_data_node(state: ReconciliationState) -> ReconciliationState:
    erp_df = load_erp_data("data/erp_data.xlsx")
    bank_df = load_bank_statement("data/bank_statement.pdf")
    state["erp_df"] = erp_df
    state["bank_df"] = bank_df
    return state


def reconcile_node(state: ReconciliationState) -> ReconciliationState:
    state["summary"] = reconcile_data(state["erp_df"], state["bank_df"])
    return state

def summarize_node(state: ReconciliationState) -> ReconciliationState:
    state["report_text"] =  summarize_summary(state["summary"])
    return state


def generate_report_node(state: ReconciliationState) -> ReconciliationState:
    state["pdf_path"] = save_report_to_pdf(state["report_text"])
    return state


# ---- Build Graph ----
def build_graph():
    workflow = StateGraph(ReconciliationState)

    workflow.add_node("load_data", load_data_node)
    workflow.add_node("reconcile", reconcile_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("generate_report", generate_report_node)

    workflow.set_entry_point("load_data")

    workflow.add_edge("load_data", "reconcile")
    workflow.add_edge("reconcile", "summarize")
    workflow.add_edge("summarize", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()
