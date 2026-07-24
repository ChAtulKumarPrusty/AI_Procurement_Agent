import React from "react";

import StatsCards from "./StatsCards";
import VendorComparisonTable from "./VendorComparisonTable";
import VendorScoreTable from "./VendorScoreTable";
import RecommendationCard from "./RecommendationCard";
import ReportDownload from "./ReportDownload";

export default function Result({ result }) {
  if (!result) return null;

  // Parse response
  let data;

  try {
    data =
      typeof result === "string"
        ? JSON.parse(result)
        : result;
  } catch {
    data = result;
  }

  // Backend response
  const report = data.result || data;

  // Extract data
  const vendors = report.comparison_df || [];
  const scores = report.vendor_scores || [];
  const recommendation = report.recommendation || "";
  const reportPath = report.report_path || "";
  const errors = report.errors || [];

  // -------------------------------
  // Best Vendor
  // -------------------------------

  let bestVendor = "";

  if (scores.length > 0) {
    const best = scores.reduce((a, b) =>
      Number(a.total_score) >= Number(b.total_score)
        ? a
        : b
    );

    bestVendor = best.vendor_name;
  }

  // -------------------------------
  // Lowest Price
  // -------------------------------

  let lowestPrice = 0;

  if (vendors.length > 0) {
    lowestPrice = Math.min(
      ...vendors.map((v) =>
        Number(v["Grand Total"] || 0)
      )
    );
  }

  return (
    <div className="results-section">

      {/* Stats */}

      <StatsCards
        vendorCount={vendors.length}
        bestVendor={bestVendor}
        lowestPrice={lowestPrice}
        reportReady={!!reportPath}
      />

      {/* Vendor Comparison */}

      <VendorComparisonTable
        vendors={vendors}
        bestVendor={bestVendor}
      />

      {/* Vendor Scores */}

      <VendorScoreTable
        scores={scores}
      />

      {/* Recommendation */}

      <RecommendationCard
        recommendation={recommendation}
      />

      {/* Errors */}

      {errors.length > 0 && (
        <div
          className="recommendation-card"
          style={{
            borderLeft: "5px solid red",
            marginTop: "25px",
          }}
        >
          <h3>Errors</h3>

          <ul>
            {errors.map((err, index) => (
              <li key={index}>
                {String(err)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Download */}

      <ReportDownload
        report={report}
        reportPath={reportPath}
      />
    </div>
  );
}