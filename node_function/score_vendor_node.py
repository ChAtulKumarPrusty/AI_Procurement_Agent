from state.state import ProcurementState
from typing import Dict
import pandas as pd


def score_vendor_node(state: ProcurementState) -> Dict:
    """
    Score vendors based on quotation comparison.

    Scoring Criteria:
    - Lowest Price       : 40%
    - Fastest Delivery   : 30%
    - Longest Warranty   : 20%
    - Payment Terms      : 10%
    """

    comparison_df = state.get("comparison_df")
    errors = list(state.get("errors", []))

    if comparison_df is None or comparison_df.empty:
        errors.append("Comparison DataFrame is empty.")

        return {
            "errors": errors
        }

    df = comparison_df.copy()

    # -----------------------------------
    # Convert columns to numeric values
    # -----------------------------------

    df["Grand Total"] = pd.to_numeric(
        df["Grand Total"],
        errors="coerce"
    )

    df["Delivery Days"] = (
        df["Delivery Time"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    df["Warranty Years"] = (
        df["Warranty"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    df["Payment Days"] = (
        df["Payment Terms"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    # -----------------------------------
    # Normalize scores
    # -----------------------------------

    price_score = (
        (df["Grand Total"].max() - df["Grand Total"])
        / (df["Grand Total"].max() - df["Grand Total"].min() + 1e-6)
    ) * 40

    delivery_score = (
        (df["Delivery Days"].max() - df["Delivery Days"])
        / (df["Delivery Days"].max() - df["Delivery Days"].min() + 1e-6)
    ) * 30

    warranty_score = (
        (df["Warranty Years"] - df["Warranty Years"].min())
        / (df["Warranty Years"].max() - df["Warranty Years"].min() + 1e-6)
    ) * 20

    payment_score = (
        (df["Payment Days"] - df["Payment Days"].min())
        / (df["Payment Days"].max() - df["Payment Days"].min() + 1e-6)
    ) * 10

    total_score = (
        price_score +
        delivery_score +
        warranty_score +
        payment_score
    )

    vendor_scores = []

    for i in range(len(df)):

        vendor_scores.append(
            {
                "vendor_name": df.iloc[i]["Vendor"],
                "price_score": float(round(price_score.iloc[i], 2)),
                "delivery_score": float(round(delivery_score.iloc[i], 2)),
                "warranty_score": float(round(warranty_score.iloc[i], 2)),
                "payment_score": float(round(payment_score.iloc[i], 2)),
                "total_score": float(round(total_score.iloc[i], 2))
            }
        )

    vendor_scores = sorted(
        vendor_scores,
        key=lambda x: x["total_score"],
        reverse=True
    )

    return {
        "vendor_scores": vendor_scores,
        "errors": errors
    }


