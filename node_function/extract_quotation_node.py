from state.state import ProcurementState
from typing import Dict
import json
from model.llm import model

def extract_quotation_details(text: str) -> dict:
    """
    Extract structured quotation information using the LLM.

    Args:
        text (str)

    Returns:
        dict
    """

    prompt = f"""
You are an AI Procurement Assistant.

Extract the following information from the quotation.

Return ONLY a valid JSON object.

Do NOT write any explanation.
Do NOT write markdown.
Do NOT wrap the JSON inside ```json.
Do NOT write any text before or after the JSON.

If a field is missing, use null.

Fields:

{{
    "vendor_name": "",
    "quotation_number": "",
    "quotation_date": "",
    "currency": "",
    "subtotal": "",
    "gst": "",
    "grand_total": "",
    "delivery_time": "",
    "payment_terms": "",
    "warranty": "",
    "validity": "",
    "contact_person": "",
    "email": "",
    "phone": "",
    "items": [
        {{
            "item_name": "",
            "quantity": "",
            "unit_price": "",
            "total_price": ""
        }}
    ]
}}

If any field is missing, return null.

Quotation:

{text}
"""

    response = model.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        print("Invalid JSON received:")
        print(content)
        raise


def extract_quotation_node(state: ProcurementState) -> Dict:
    """
    Extract structured quotation details from raw text using an LLM.

    Input:
        state["raw_texts"]

    Output:
        state["quotations"]
        state["errors"]
    """

    raw_texts = state.get("raw_texts", [])
    quotations = []
    errors = list(state.get("errors", []))

    if not raw_texts:
        errors.append("No extracted text available.")
        return {
            "errors": errors
        }

    for index, text in enumerate(raw_texts):

        try:
            quotation = extract_quotation_details(text)

            quotations.append(quotation)

        except Exception as e:
            errors.append(
                f"Failed to extract quotation from document {index + 1}: {str(e)}"
            )

    return {
        "quotations": quotations,
        "errors": errors
    }
