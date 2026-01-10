export default function ViolationTable({ events = [] }) {
  if (!Array.isArray(events) || events.length === 0) {
    return (
      <div className="analytics-card empty-state">
        No active safety alerts
      </div>
    );
  }

  // ---- PRIORITIZATION LOGIC  ----
  const PRIORITY = { HIGH: 3, MEDIUM: 2, LOW: 1 };
  const STATE_PRIORITY = { ESCALATED: 3, CONFIRMED: 2 };

  const sorted = [...events].sort((a, b) => {
    const r =
      (PRIORITY[b.riskLevel] || 0) -
      (PRIORITY[a.riskLevel] || 0);
    if (r !== 0) return r;

    const s =
      (STATE_PRIORITY[b.state] || 0) -
      (STATE_PRIORITY[a.state] || 0);
    if (s !== 0) return s;

    return (b.duration || 0) - (a.duration || 0);
  });

  return (
    <div className="analytics-card violation-table">
      <h4 className="card-title">Active Safety Alerts</h4>

      <div className="violation-table-wrapper">
        <table className="violation-table-grid">
          <thead>
            <tr>
              <th>Person</th>
              <th>Camera</th>
              <th>Violation</th>
              <th>State</th>
              <th>Duration</th>
              <th>Confidence</th>
              <th>Risk</th>
            </tr>
          </thead>

          <tbody>
            {sorted.map((v, i) => (
              <tr key={`${v.personId}-${v.type}-${i}`}>
                <td className="mono">{v.personId}</td>
                <td className="mono">
                  {v.cameraId?.toUpperCase()}
                </td>

                <td>{v.type?.replaceAll("_", " ")}</td>

                <td>
                  <span className={`state-badge ${v.state?.toLowerCase()}`}>
                    {v.state}
                  </span>
                </td>

                <td className="mono">{v.duration ?? 0}s</td>

                <td className="mono">
                  {Math.round(v.confidence ?? 0)}%
                </td>

                <td>
                  <span className={`risk-pill ${v.riskLevel?.toLowerCase()}`}>
                    {v.riskLevel}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
