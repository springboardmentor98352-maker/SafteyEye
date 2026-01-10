export default function GlobalStatsPanel({ metrics }) {
  if (!metrics) return null;

  return (
    <div className="analytics-card">
      <h4>Site Overview</h4>

      <div className="stats">
        <div>
          Total Occupancy: <b>{metrics.totalOccupancy}</b>
        </div>

        <div>
          System Health:{" "}
          <b>{metrics.onlineCameras} / {metrics.totalCameras}</b>{" "}
          Cameras Online
        </div>
      </div>
    </div>
  );
}
