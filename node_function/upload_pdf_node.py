from state.state import ProcurementState
from typing import Dict

def upload_pdf_node(state: ProcurementState) -> Dict:
    """
    Upload PDF Node

    Purpose:
    - Validate uploaded PDF files.
    - Initialize the workflow state.
    - Return the validated PDF list.

    Input:
        state["pdf_files"] -> List of uploaded PDF file paths or file objects

    Output:
        Updates:
            - pdf_files
            - errors (if any)
    """

    pdf_files = state.get("pdf_files", [])
    errors = []

    # Check if any PDF is uploaded
    if not pdf_files:
        errors.append("No PDF files were uploaded.")

        return {
            "errors": errors
        }

    # Validate each uploaded file
    valid_pdfs = []

    for pdf in pdf_files:

        # If using file paths
        if isinstance(pdf, str):

            if pdf.lower().endswith(".pdf"):
                valid_pdfs.append(pdf)
            else:
                errors.append(f"Invalid file type: {pdf}")

        # If using UploadedFile objects (Streamlit/FastAPI)
        else:

            filename = getattr(pdf, "name", None)

            if filename and filename.lower().endswith(".pdf"):
                valid_pdfs.append(pdf)
            else:
                errors.append("Uploaded file is not a PDF.")

    return {
        "pdf_files": valid_pdfs,
        "errors": errors
    }
