from state.state import ProcurementState
from typing import Dict
import pandas as pd
import os
from datetime import datetime

def generate_excel_report(
    comparison_df: pd.DataFrame,
    vendor_scores: list,
    recommendation: str
) -> str:

    os.makedirs("reports", exist_ok=True)

    filename = (
        f"procurement_report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    report_path = os.path.join("reports", filename)

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:

        # Sheet 1
        comparison_df.to_excel(
            writer,
            sheet_name="Comparison",
            index=False
        )

        # Sheet 2
        pd.DataFrame(vendor_scores).to_excel(
            writer,
            sheet_name="Vendor Scores",
            index=False
        )

        # Sheet 3
        recommendation_df = pd.DataFrame(
            {
                "Recommendation": [recommendation]
            }
        )

        recommendation_df.to_excel(
            writer,
            sheet_name="Recommendation",
            index=False
        )

    return report_path



def generate_report_node(state: ProcurementState) -> Dict:
    """
    Generate the final procurement comparison report.

    Input:
        comparison_df
        vendor_scores
        recommendation

    Output:
        report_path
        errors
    """

    comparison_df = state.get("comparison_df")
    vendor_scores = state.get("vendor_scores", [])
    recommendation = state.get("recommendation", "")
    errors = list(state.get("errors", []))

    if comparison_df is None or comparison_df.empty:
        errors.append("Comparison DataFrame is empty.")

        return {
            "errors": errors
        }

    try:

        report_path = generate_excel_report(
            comparison_df=comparison_df,
            vendor_scores=vendor_scores,
            recommendation=recommendation
        )

        return {
            "report_path": report_path,
            "errors": errors
        }

    except Exception as e:

        errors.append(f"Report generation failed: {str(e)}")

        return {
            "errors": errors
        }

