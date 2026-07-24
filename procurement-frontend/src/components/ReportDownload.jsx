import React from "react";

export default function ReportDownload({
  report,
  reportPath,
}) {
  const downloadJson = () => {
    if (!report) return;

    const blob = new Blob(
      [JSON.stringify(report, null, 2)],
      {
        type: "application/json",
      }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "procurement-report.json";
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="download-section">
      {reportPath && (
        <div
          style={{
            marginBottom: "16px",
            padding: "14px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            background: "#fafafa",
          }}
        >
          <strong>Generated Report</strong>

          <div
            style={{
              marginTop: "8px",
              color: "#666",
              wordBreak: "break-all",
              fontSize: "14px",
            }}
          >
            {reportPath}
          </div>
        </div>
      )}

      <button
        className="download-btn"
        onClick={downloadJson}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>

        Download JSON Report
      </button>
    </div>
  );
}