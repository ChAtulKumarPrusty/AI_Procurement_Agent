import React from "react";

export default function VendorScoreTable({ scores }) {
  if (!scores || scores.length === 0) {
    return null;
  }

  // Find highest score
  const highestScore = Math.max(
    ...scores.map((s) => Number(s.total_score || 0))
  );

  return (
    <div className="comparison-table-wrapper">
      <h3>Vendor Score Analysis</h3>

      <table className="comparison-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Vendor</th>
            <th>Price</th>
            <th>Delivery</th>
            <th>Warranty</th>
            <th>Payment</th>
            <th>Total</th>
            <th>Rank</th>
          </tr>
        </thead>

        <tbody>
          {scores.map((score, index) => {
            const isBest =
              Number(score.total_score) === highestScore;

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
                  {score.vendor_name}
                </td>

                <td>{score.price_score}</td>

                <td>{score.delivery_score}</td>

                <td>{score.warranty_score}</td>

                <td>{score.payment_score}</td>

                <td
                  style={{
                    fontWeight: 700,
                  }}
                >
                  {score.total_score}
                </td>

                <td>
                  <span
                    className={`badge ${
                      isBest
                        ? "badge-best"
                        : "badge-waiting"
                    }`}
                  >
                    {isBest ? "Winner" : "Compared"}
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