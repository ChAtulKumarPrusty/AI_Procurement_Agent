from state.state import ProcurementState
from typing import Dict
import json
from model.llm import model

def recommend_vendor_node(state: ProcurementState) -> Dict:
    """
    Generate an AI recommendation for the best vendor.

    Input:
        comparison_df
        vendor_scores

    Output:
        recommendation
        errors
    """

    comparison_df = state.get("comparison_df")
    vendor_scores = state.get("vendor_scores", [])
    errors = list(state.get("errors", []))

    if comparison_df is None or comparison_df.empty:
        errors.append("Comparison table is empty.")

        return {
            "errors": errors
        }

    if not vendor_scores:
        errors.append("Vendor scores are missing.")

        return {
            "errors": errors
        }

    comparison_table = comparison_df.to_markdown(index=False)

    prompt = f"""
You are an expert Procurement Evaluation Assistant.

Your job is to recommend the best vendor.

Vendor Scores:

{json.dumps(vendor_scores, indent=2)}

Vendor Comparison Table:

{comparison_table}

Instructions:

- Choose the best vendor.
- Explain why that vendor is recommended.
- Compare it with the other vendors.
- Mention strengths and weaknesses.
- Consider:
    • Price
    • Delivery Time
    • Warranty
    • Payment Terms
- Keep the response professional.
"""

    response = model.invoke(prompt)

    recommendation = response.content.strip()

    return {
        "recommendation": recommendation,
        "errors": errors
    }



