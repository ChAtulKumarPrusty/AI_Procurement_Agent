from typing import TypedDict, List, Dict, Any, Optional
import pandas as pd
class ProcurementState(TypedDict):
    """
    Shared state for the AI Procurement Agent.
    Every LangGraph node reads from and updates this state.
    """

    # Uploaded quotation PDFs
    pdf_files: List[Any]

    # Raw extracted text from each PDF
    raw_texts: List[str]

    # Structured quotation data extracted by the LLM
    quotations: List[Dict[str, Any]]

    # Comparison table (Pandas DataFrame)
    comparison_df: Optional[pd.DataFrame]

    # Vendor scores
    vendor_scores: List[Dict[str, Any]]

    # AI recommendation
    recommendation: str

    # Excel report location
    report_path: str

    # Error messages (if any)
    errors: List[str]