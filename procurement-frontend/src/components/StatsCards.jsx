import React from "react";

export default function StatsCards({
  vendorCount,
  bestVendor,
  lowestPrice,
  reportReady,
}) {
  const formatPrice = (price) => {
    if (price === null || price === undefined) return "₹0";

    return "₹" + Number(price).toLocaleString("en-IN");
  };

  return (
    <div className="stats-grid">
      {/* Vendors */}
      <div className="stat-card">
        <div className="stat-card-icon vendors">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </div>

        <div className="stat-card-label">Total Vendors</div>

        <div className="stat-card-value">{vendorCount}</div>
      </div>

      {/* Best Vendor */}

      <div className="stat-card">
        <div className="stat-card-icon best">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
        </div>

        <div className="stat-card-label">Best Vendor</div>

        <div
          className="stat-card-value"
          style={{
            fontSize: "18px",
            lineHeight: "24px",
          }}
        >
          {bestVendor || "--"}
        </div>
      </div>

      {/* Lowest Price */}

      <div className="stat-card">
        <div className="stat-card-icon price">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <line x1="12" y1="1" x2="12" y2="23" />
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
        </div>

        <div className="stat-card-label">Lowest Price</div>

        <div className="stat-card-value">
          {formatPrice(lowestPrice)}
        </div>
      </div>

      {/* Report */}

      <div className="stat-card">
        <div className="stat-card-icon report">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
        </div>

        <div className="stat-card-label">Report</div>

        <div
          className="stat-card-value"
          style={{
            color: reportReady ? "#16a34a" : "#dc2626",
            fontSize: "18px",
          }}
        >
          {reportReady ? "Ready" : "Pending"}
        </div>
      </div>
    </div>
  );
}