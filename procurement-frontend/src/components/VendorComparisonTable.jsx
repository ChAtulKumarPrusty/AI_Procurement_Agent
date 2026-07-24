import React from "react";

export default function VendorComparisonTable({
  vendors,
  bestVendor,
}) {
  const formatPrice = (price) => {
    if (price === null || price === undefined) return "₹0";

    return "₹" + Number(price).toLocaleString("en-IN");
  };

  if (!vendors || vendors.length === 0) {
    return (
      <div className="comparison-table-wrapper">
        <h3>Vendor Comparison</h3>

        <div
          style={{
            textAlign: "center",
            padding: "40px",
            color: "#888",
          }}
        >
          No vendor data available.
        </div>
      </div>
    );
  }

  return (
    <div className="comparison-table-wrapper">
      <h3>Vendor Comparison</h3>

      <table className="comparison-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Vendor</th>
            <th>Quotation No</th>
            <th>Grand Total</th>
            <th>Delivery</th>
            <th>Warranty</th>
            <th>Payment Terms</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {vendors.map((vendor, index) => {
            const isBest =
              vendor["Vendor"] === bestVendor;

            return (
              <tr
                key={index}
                className={isBest ? "table-best" : ""}
              >
                <td>{index + 1}</td>

                <td
                  style={{
                    fontWeight: 600,
                  }}
                >
                  {vendor["Vendor"]}
                </td>

                <td>{vendor["Quotation No"]}</td>

                <td>
                  {formatPrice(
                    vendor["Grand Total"]
                  )}
                </td>

                <td>{vendor["Delivery Time"]}</td>

                <td>{vendor["Warranty"]}</td>

                <td>{vendor["Payment Terms"]}</td>

                <td>
                  <span
                    className={`badge ${
                      isBest
                        ? "badge-best"
                        : "badge-waiting"
                    }`}
                  >
                    {isBest
                      ? "Recommended"
                      : "Compared"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}