from state.state import ProcurementState
from typing import Dict
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract

def read_pdf(pdf_path: str) -> str:
    """
    Extract text from a searchable PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """

    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()


def perform_ocr(pdf_path: str) -> str:
    """
    Perform OCR on scanned PDFs.

    Args:
        pdf_path (str)

    Returns:
        str
    """

    pages = convert_from_path(pdf_path)

    text = ""

    for page in pages:
        text += pytesseract.image_to_string(page)

    return text.strip()



def extract_text_node(state: ProcurementState) -> Dict:
    """
    Extract text from uploaded PDF files.

    Workflow:
    1. Read each PDF.
    2. If text extraction fails or returns very little text,
       perform OCR.
    3. Store extracted text in raw_texts.
    """

    pdf_files = state.get("pdf_files", [])
    raw_texts = []
    errors = list(state.get("errors", []))

    if not pdf_files:
        errors.append("No PDF files available for text extraction.")
        return {
            "errors": errors
        }

    for pdf in pdf_files:

        try:
            # -----------------------------
            # Step 1: Try normal PDF parsing
            # -----------------------------
            text = read_pdf(pdf)

            # -----------------------------
            # Step 2: OCR fallback
            # -----------------------------
            if not text or len(text.strip()) < 50:
                text = perform_ocr(pdf)

            # -----------------------------
            # Step 3: Save extracted text
            # -----------------------------
            raw_texts.append(text)

        except Exception as e:
            errors.append(f"Failed to extract text from {pdf}: {str(e)}")

    return {
        "raw_texts": raw_texts,
        "errors": errors
    }