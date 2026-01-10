import { useMemo } from "react";
import { useSocket } from "../context/SocketProvider";

export default function Reports() {
  //  CORRECT SOURCES
  const {
    cameras = {},
    violations = [],
    activeAlerts = []
  } = useSocket();

  // ================= GLOBAL STATS =================
  const stats = useMemo(() => {
    const camList = Object.values(cameras);

    return {
      camerasOnline: camList.length,
      totalOccupancy: camList.reduce(
        (sum, c) => sum + (c.occupancy || 0),
        0
      ),
      totalViolations: activeAlerts.length,
      activeAlerts: activeAlerts.length
    };
  }, [cameras, violations, activeAlerts]);

  return (
    <div className="page reports-page">
      <h2 className="page-heading">Reports</h2>

      {/* METRICS */}
      <div className="metrics-grid">
        <Metric label="Cameras Online" value={stats.camerasOnline} />
        <Metric label="Total Occupancy" value={stats.totalOccupancy} />
        <Metric label="Total Violations Detected" value={stats.totalViolations} />

        <Metric
          label="Active Alerts"
          value={stats.activeAlerts}
          danger={stats.activeAlerts > 0}
        />
      </div>

      {/* CAMERA-WISE SUMMARY */}
      <div className="card">
        <h3 className="section-heading">Camera-wise Summary</h3>

        <table className="data-table">
          <thead>
            <tr>
              <th>Camera</th>
              <th>Status</th>
              <th>Occupancy</th>
              <th>Total Violations (History)</th>
              <th>Active Alerts</th>
            </tr>
          </thead>

          <tbody>
            {Object.entries(cameras).map(([id, cam]) => {
              const camViolations = violations.filter(
                v => v.cameraId === id
              ).length;

              const camActiveAlerts = activeAlerts.filter(
                a => a.cameraId === id
              ).length;

              return (
                <tr key={id}>
                  <td>{id.toUpperCase()}</td>
                  <td className="status-online">ONLINE</td>
                  <td>{cam.occupancy ?? 0}</td>
                  <td>{camViolations}</td>
                  <td>{camActiveAlerts}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ---------------- METRIC CARD ----------------
function Metric({ label, value, danger }) {
  return (
    <div className={`metric-card ${danger ? "danger" : ""}`}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
    </div>
  );
}
