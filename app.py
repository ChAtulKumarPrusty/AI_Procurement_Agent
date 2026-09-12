from pathlib import Path
import shutil
import uuid
import math

import pandas as pd
import numpy as np

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from workflow.graph import graph


app = FastAPI(
    title="AI Procurement Agent",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Upload directory
# ============================================================

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================
# JSON SAFE CONVERTER
# ============================================================

def make_json_safe(obj):
    """
    Recursively convert Pandas/NumPy objects into
    values that FastAPI can safely serialize as JSON.

    Handles:
    - NaN
    - +Infinity
    - -Infinity
    - numpy integers
    - numpy floats
    - numpy arrays
    - pandas DataFrames
    - pandas Series
    - dictionaries
    - lists
    - tuples
    """

    # --------------------------------------------------------
    # None / basic JSON types
    # --------------------------------------------------------

    if obj is None:
        return None

    if isinstance(obj, (str, bool, int)):
        return obj

    # --------------------------------------------------------
    # Python float
    # --------------------------------------------------------

    if isinstance(obj, float):
        if not math.isfinite(obj):
            return None

        return obj

    # --------------------------------------------------------
    # NumPy integer
    # --------------------------------------------------------

    if isinstance(obj, np.integer):
        return int(obj)

    # --------------------------------------------------------
    # NumPy floating point
    # --------------------------------------------------------

    if isinstance(obj, np.floating):
        value = float(obj)

        if not math.isfinite(value):
            return None

        return value

    # --------------------------------------------------------
    # NumPy boolean
    # --------------------------------------------------------

    if isinstance(obj, np.bool_):
        return bool(obj)

    # --------------------------------------------------------
    # NumPy array
    # --------------------------------------------------------

    if isinstance(obj, np.ndarray):
        return make_json_safe(obj.tolist())

    # --------------------------------------------------------
    # Pandas DataFrame
    # --------------------------------------------------------

    if isinstance(obj, pd.DataFrame):

        # Replace infinity with NaN first
        df = obj.replace([np.inf, -np.inf], np.nan)

        # Convert NaN to None
        df = df.astype(object).where(pd.notna(df), None)

        records = df.to_dict(orient="records")

        return make_json_safe(records)

    # --------------------------------------------------------
    # Pandas Series
    # --------------------------------------------------------

    if isinstance(obj, pd.Series):

        series = obj.replace([np.inf, -np.inf], np.nan)

        series = series.astype(object).where(
            pd.notna(series),
            None
        )

        return make_json_safe(series.tolist())

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(obj, dict):

        return {
            str(key): make_json_safe(value)
            for key, value in obj.items()
        }

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    if isinstance(obj, list):

        return [
            make_json_safe(item)
            for item in obj
        ]

    # --------------------------------------------------------
    # Tuple
    # --------------------------------------------------------

    if isinstance(obj, tuple):

        return [
            make_json_safe(item)
            for item in obj
        ]

    # --------------------------------------------------------
    # Pandas NA / NaT
    # --------------------------------------------------------

    try:
        if pd.isna(obj):
            return None
    except (TypeError, ValueError):
        pass

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return obj


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Procurement Agent API Running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# ANALYZE VENDOR PDF
# ============================================================

@app.post("/analyze")
async def analyze_vendor_pdf(
    files: list[UploadFile] = File(...)
):
    """
    Upload one or more vendor quotation PDFs
    and analyze them using the AI Procurement Agent.
    """

    if not files:

        raise HTTPException(
            status_code=400,
            detail="No files uploaded."
        )

    pdf_files = []

    try:

        # ====================================================
        # SAVE UPLOADED PDFs
        # ====================================================

        for file in files:

            if not file.filename:

                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file has no filename."
                )

            if not file.filename.lower().endswith(".pdf"):

                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} is not a PDF."
                )

            filename = f"{uuid.uuid4()}_{file.filename}"

            filepath = UPLOAD_DIR / filename

            with open(filepath, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            pdf_files.append(str(filepath))

        # ====================================================
        # INITIAL GRAPH STATE
        # ====================================================

        state = {
            "pdf_files": pdf_files
        }

        # ====================================================
        # RUN LANGGRAPH WORKFLOW
        # ====================================================

        result = graph.invoke(state)

        # ====================================================
        # DEBUG INFORMATION
        # ====================================================

        print("\n" + "=" * 70)
        print("PROCUREMENT GRAPH COMPLETED")
        print("=" * 70)

        print("Result keys:")

        for key in result.keys():

            print(
                f"  - {key}: "
                f"{type(result[key]).__name__}"
            )

        print("=" * 70 + "\n")

        # ====================================================
        # CONVERT EVERYTHING TO JSON-SAFE VALUES
        # ====================================================

        safe_result = make_json_safe(result)

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return {
            "success": True,
            "result": safe_result
        }

    except HTTPException:

        raise

    except Exception as e:

        print("\n" + "=" * 70)
        print("ERROR DURING PROCUREMENT ANALYSIS")
        print("=" * 70)
        print(type(e).__name__)
        print(str(e))
        print("=" * 70 + "\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
