import { useMemo } from "react";
import { useSocket } from "../context/SocketProvider";

export default function Violations() {
  
  const { violations = [] } = useSocket();

  // Show last 50 incidents (newest first)
  const rows = useMemo(
    () => [...violations].slice(-50).reverse(),
    [violations]
  );

  return (
    <div className="page violations-page">
      <h2 className="page-heading">Violation History</h2>

      <div className="card violation-history-card">
        {rows.length === 0 ? (
          <div className="empty-state">
            No violations recorded
          </div>
        ) : (
          <div className="violation-history-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Camera</th>
                  <th>Violation</th>
                  <th>Person</th>
                  <th>Confidence</th>
                  <th>Risk</th>
                  <th>Last Seen</th>
                </tr>
              </thead>

              <tbody>
                {rows.map((v, i) => (
                  <tr key={`${v.cameraId}-${v.personId}-${v.type}-${i}`}>
                    <td className="mono">
                      {v.cameraId?.toUpperCase()}
                    </td>

                    <td>
                      {v.type.replaceAll("_", " ")}
                    </td>

                    <td className="mono">
                      P-{v.personId}
                    </td>

                    <td>
                      {v.confidence}%
                    </td>

                    <td>
                      <span
                        className={`badge ${
                          v.riskLevel === "HIGH"
                            ? "danger"
                            : v.riskLevel === "MEDIUM"
                            ? "warning"
                            : "ok"
                        }`}
                      >
                        {v.riskLevel}
                      </span>
                    </td>

                    <td className="mono">
                      {new Date(v.lastSeen).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
