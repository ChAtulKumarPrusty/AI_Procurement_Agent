from typing import Dict
import pandas as pd
from state.state import ProcurementState

def compare_vendor_node(state: ProcurementState) -> Dict:
    """
    Compare all extracted quotations and create a comparison DataFrame.

    Input:
        state["quotations"]

    Output:
        state["comparison_df"]
        state["errors"]
    """

    quotations = state.get("quotations", [])
    errors = list(state.get("errors", []))

    if not quotations:
        errors.append("No quotations available for comparison.")

        return {
            "errors": errors
        }

    comparison_data = []

    for quotation in quotations:

        row = {
            "Vendor": quotation.get("vendor_name"),
            "Quotation No": quotation.get("quotation_number"),
            "Quotation Date": quotation.get("quotation_date"),
            "Currency": quotation.get("currency"),
            "Subtotal": quotation.get("subtotal"),
            "GST": quotation.get("gst"),
            "Grand Total": quotation.get("grand_total"),
            "Delivery Time": quotation.get("delivery_time"),
            "Payment Terms": quotation.get("payment_terms"),
            "Warranty": quotation.get("warranty"),
            "Validity": quotation.get("validity"),
            "Contact Person": quotation.get("contact_person"),
            "Email": quotation.get("email"),
            "Phone": quotation.get("phone"),
            "No. of Items": len(quotation.get("items", []))
        }

        comparison_data.append(row)

    comparison_df = pd.DataFrame(comparison_data)

    return {
        "comparison_df": comparison_df,
        "errors": errors
    }

