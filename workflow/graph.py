from langgraph.graph import StateGraph, START, END
from state.state import ProcurementState

from node_function.upload_pdf_node import upload_pdf_node
from node_function.extract_text_node import extract_text_node
from node_function.extract_quotation_node import extract_quotation_node
from node_function.compare_vendor_node import compare_vendor_node
from node_function.score_vendor_node import score_vendor_node
from node_function.recommend_vendor_node import recommend_vendor_node
from node_function.generate_report_node import generate_report_node
from node_function.error_handler_node import error_handler_node

def check_errors(state: ProcurementState) -> str:
    """
    Route the graph based on the presence of errors.
    """

    errors = state.get("errors", [])

    return "error" if len(errors) > 0 else "success"


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(ProcurementState)

# Add Nodes
builder.add_node("upload_pdf", upload_pdf_node)
builder.add_node("extract_text", extract_text_node)
builder.add_node("extract_quotation", extract_quotation_node)
builder.add_node("compare_vendor", compare_vendor_node)
builder.add_node("score_vendor", score_vendor_node)
builder.add_node("recommend_vendor", recommend_vendor_node)
builder.add_node("generate_report", generate_report_node)
builder.add_node("error_handler", error_handler_node)

# ==========================================================
# Edges
# ==========================================================

builder.add_edge(START, "upload_pdf")

builder.add_edge("upload_pdf", "extract_text")

builder.add_conditional_edges(
    "extract_text",
    check_errors,
    {
        "success": "extract_quotation",
        "error": "error_handler",
    },
)

builder.add_conditional_edges(
    "extract_quotation",
    check_errors,
    {
        "success": "compare_vendor",
        "error": "error_handler",
    },
)

builder.add_conditional_edges(
    "compare_vendor",
    check_errors,
    {
        "success": "score_vendor",
        "error": "error_handler",
    },
)

builder.add_conditional_edges(
    "score_vendor",
    check_errors,
    {
        "success": "recommend_vendor",
        "error": "error_handler",
    },
)

builder.add_conditional_edges(
    "recommend_vendor",
    check_errors,
    {
        "success": "generate_report",
        "error": "error_handler",
    },
)
builder.add_edge("error_handler", END)
builder.add_edge("generate_report", END)

# ==========================================================
# Compile Graph
# ==========================================================

graph = builder.compile()
