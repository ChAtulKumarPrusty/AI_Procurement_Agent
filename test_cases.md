## Test Cases for AI Procurement Agent

This document outlines test cases for the AI Procurement Agent, covering both the FastAPI backend and the LangGraph workflow. The tests aim to ensure the system's functionality, robustness, and error handling.

### I. Backend API Tests (`/analyze` endpoint)

**Objective:** Verify the `/analyze` endpoint's behavior under various conditions, including successful PDF uploads, invalid file types, and internal workflow errors.

| Test Case ID | Description | Input | Expected Output | Notes |
|---|---|---|---|---|
| **1.1** | Successful PDF Upload (Single) | Valid single PDF quotation file | `success: true`, structured JSON result with `comparison_df`, `vendor_scores`, `recommendation`, `report_path` | Verify all fields are populated correctly. |
| **1.2** | Successful PDF Upload (Multiple) | Multiple valid PDF quotation files | `success: true`, structured JSON result with aggregated data | Ensure correct processing and aggregation of multiple documents. |
| **1.3** | No Files Uploaded | Empty request or no files in `files` array | `status_code: 400`, `detail: "No files uploaded." ` | Test FastAPI validation. |
| **1.4** | Invalid File Type Upload | Upload a `.txt` or `.jpg` file instead of `.pdf` | `status_code: 400`, `detail: "<filename> is not a PDF." ` | Ensure file type validation works. |
| **1.5** | Mixed File Types Upload | One valid PDF, one invalid file | `status_code: 400`, `detail: "<filename> is not a PDF." ` | Should reject the entire batch if any file is invalid. |
| **1.6** | Large PDF File Upload | A very large PDF file (e.g., >10MB) | `success: true` (if processed), or appropriate error if size limit is hit | Test performance and potential resource exhaustion. (Requires configuring max file size in FastAPI if not already) |
| **1.7** | Corrupted PDF File Upload | A PDF file that is unreadable or malformed | `status_code: 500`, `detail: "Failed to extract text..."` (or similar) | Test robustness of PDF parsing. |
| **1.8** | LLM Extraction Failure | Valid PDF, but LLM fails to extract structured data | `status_code: 500`, `detail: "Invalid JSON received..."` (or similar) | Simulate LLM returning malformed JSON or no JSON. |
| **1.9** | Empty Quotation Data | Valid PDF, but contains no recognizable quotation information | `success: true`, but `comparison_df`, `vendor_scores`, `recommendation` might be empty/null | Verify graceful handling of sparse data. |

### II. LangGraph Workflow Tests

**Objective:** Validate the behavior of individual nodes and the overall flow of the LangGraph, especially conditional routing and error propagation.

| Test Case ID | Description | Input State (Key elements) | Expected Outcome | Notes |
|---|---|---|---|---|
| **2.1** | `upload_pdf_node` - Valid Input | `pdf_files: ["path/to/vendor1.pdf"]` | `pdf_files` populated, `errors` empty | Basic functionality. |
| **2.2** | `upload_pdf_node` - No PDF Files | `pdf_files: []` | `errors` contains "No PDF files provided." | Test initial validation. |
| **2.3** | `extract_text_node` - Successful Extraction | `pdf_files: ["path/to/vendor1.pdf"]` (containing text) | `raw_texts` populated, `errors` empty | Verify text extraction. |
| **2.4** | `extract_text_node` - OCR Fallback | `pdf_files: ["path/to/scanned.pdf"]` (image-only PDF) | `raw_texts` populated via OCR, `errors` empty | Verify OCR mechanism. |
| **2.5** | `extract_text_node` - Extraction Failure | `pdf_files: ["path/to/corrupted.pdf"]` | `raw_texts` empty, `errors` contains extraction error | Test robustness. |
| **2.6** | `extract_quotation_node` - Successful Extraction | `raw_texts: ["text from quotation"]` | `quotations` populated, `errors` empty | Verify LLM-based structured extraction. |
| **2.7** | `extract_quotation_node` - LLM Malformed JSON | `raw_texts: ["text causing LLM to output bad JSON"]` | `quotations` empty, `errors` contains JSON parsing error | Test LLM output handling. |
| **2.8** | `compare_vendor_node` - Successful Comparison | `quotations: [...]` (multiple valid) | `comparison_df` populated, `errors` empty | Verify DataFrame creation. |
| **2.9** | `compare_vendor_node` - Insufficient Quotations | `quotations: []` or `[...]` (single) | `comparison_df` empty, `errors` contains "Insufficient quotations for comparison." | Test edge case for comparison. |
| **2.10** | `score_vendor_node` - Successful Scoring | `comparison_df: [...]` (valid DataFrame) | `vendor_scores` populated, `errors` empty | Verify scoring logic. |
| **2.11** | `score_vendor_node` - Empty Comparison Data | `comparison_df: None` or empty DataFrame | `vendor_scores` empty, `errors` contains scoring error | Test dependency on comparison data. |
| **2.12** | `recommend_vendor_node` - Successful Recommendation | `vendor_scores: [...]`, `comparison_df: [...]` | `recommendation` populated, `errors` empty | Verify LLM-based recommendation. |
| **2.13** | `recommend_vendor_node` - No Scores/Comparison | `vendor_scores: []` or `comparison_df: None` | `recommendation` empty, `errors` contains recommendation error | Test dependency. |
| **2.14** | `generate_report_node` - Successful Report Generation | All previous nodes successful | `report_path` populated, `errors` empty | Verify Excel report creation. |
| **2.15** | `error_handler_node` - Error Routing | Any node preceding `check_errors` adds to `state["errors"]` | Workflow routes to `error_handler`, then `END` | Verify error path. |

### III. Error Handling Improvements

The current error handling primarily relies on `HTTPException` for the API and a generic `errors` list in the LangGraph state. While functional, it can be enhanced for better debugging, user feedback, and resilience.

**1. Granular Error Types and Codes:**
Instead of generic `500` or `400` with simple strings, define specific error codes and messages for different failure scenarios. This allows the frontend to display more user-friendly messages and for easier debugging.

*   **Example:**
    *   `PDF_UPLOAD_FAILED`: For issues during file saving.
    *   `PDF_PARSE_FAILED`: For issues with PyMuPDF or OCR.
    *   `LLM_EXTRACTION_FAILED`: When the LLM fails to return valid JSON.
    *   `INSUFFICIENT_DATA_FOR_COMPARISON`: When not enough quotations are available.

**2. Centralized Error Logging:**
Implement a robust logging mechanism (e.g., using Python's `logging` module) to capture detailed error information, including stack traces, at different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). This is crucial for monitoring and debugging in production.

*   **Current:** `print("Invalid JSON received:")` in `extract_quotation_node.py` is not ideal for production.
*   **Improvement:** Replace `print` statements with `logging.error` or `logging.exception`.

**3. Enhanced Frontend Error Display:**
The frontend currently uses `alert('Upload Failed')`. This can be improved to display specific error messages received from the backend, guiding the user on how to resolve the issue.

*   **Improvement:** Parse the `detail` field from `HTTPException` responses and display it prominently in the UI.

**4. Retry Mechanisms (Optional but Recommended):**
For transient errors (e.g., network issues with the LLM provider), consider implementing retry logic with exponential backoff. This can improve the robustness of the LangGraph workflow.

**5. Circuit Breaker Pattern (Optional for LLM/External Services):**
If an external service (like the LLM) is consistently failing, a circuit breaker can prevent repeated calls to a failing service, allowing it to recover and preventing cascading failures.

**6. Structured Error Objects in LangGraph State:**
Instead of just a list of strings for `errors`, consider a list of structured error objects (e.g., `{'code': 'PDF_PARSE_FAILED', 'message': 'Failed to parse PDF: ...', 'node': 'extract_text_node'}`). This makes error handling within the graph more programmatic.

**7. Graceful Degradation:**
In cases where a non-critical step fails (e.g., report generation), the system could still return partial results (e.g., comparison table and scores) to the user, rather than a complete failure.

These improvements will make the AI Procurement Agent more reliable, maintainable, and user-friendly.
