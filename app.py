from pathlib import Path
import shutil
import uuid
import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from workflow.graph import graph

app = FastAPI(
    title="AI Procurement Agent",
    version="1.0.0"
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],          # Replace with your React URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Procurement Agent API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_vendor_pdf(
    files: list[UploadFile] = File(...)
):
    """
    Upload one or more vendor quotation PDFs.
    """

    if len(files) == 0:
        raise HTTPException(
            status_code=400,
            detail="No files uploaded."
        )

    pdf_files = []

    try:
        # Save uploaded PDFs
        for file in files:

            if not file.filename.lower().endswith(".pdf"):
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} is not a PDF."
                )

            filename = f"{uuid.uuid4()}_{file.filename}"

            filepath = UPLOAD_DIR / filename

            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            pdf_files.append(str(filepath))

        # Initial graph state
        state = {
            "pdf_files": pdf_files
        }

        result = graph.invoke(state)

        # Convert DataFrame to list of dictionaries
        if "comparison_df" in result and isinstance(result["comparison_df"], pd.DataFrame):
            result["comparison_df"] = result["comparison_df"].to_dict(orient="records")

        # Convert NumPy types
        def convert(obj):
            if isinstance(obj, np.integer):
                return int(obj)

            if isinstance(obj, np.floating):
                return float(obj)

            if isinstance(obj, np.ndarray):
                return obj.tolist()

            return obj

        # Convert all values
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = [
                    {k: convert(v) for k, v in item.items()} if isinstance(item, dict)
                    else convert(item)
                    for item in value
                ]
            elif isinstance(value, dict):
                result[key] = {k: convert(v) for k, v in value.items()}
            else:
                result[key] = convert(value)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    