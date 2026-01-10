import { useSocket } from "../context/SocketProvider";

import CameraGrid from "../components/camera/CameraGrid";
import ViolationTable from "../components/layout/ViolationTable";
import OccupancyChart from "../components/charts/OccupancyChart";
import PPEComplianceDonut from "../components/charts/PPEComplianceDonut";
import GlobalStatsPanel from "../components/layout/GlobalStatsPanel";

export default function Home() {
  const {
    cameras = {},
    activeAlerts = [],
    occupancyTrend = [],
    smoothedCompliance = {}
  } = useSocket();

  // ---- View-only camera ordering ----
  const CAMERA_ORDER = ["cam1", "cam2"];
  const visibleCameras = CAMERA_ORDER.reduce((acc, id) => {
    if (cameras[id]) acc[id] = cameras[id];
    return acc;
  }, {});

  // ---- Basic aggregates (UI-only logic is OK) ----
  const cameraList = Object.values(cameras);
  const metrics = {
    totalOccupancy: cameraList.reduce(
      (sum, cam) => sum + (cam?.occupancy || 0),
      0
    ),
    onlineCameras: cameraList.length,
    totalCameras: 4
  };

  return (
    <div className="page home-page">
      <h2 className="page-heading">Live Safety Monitoring</h2>

      <div className="dashboard-fixed">

        {/* LEFT COLUMN */}
        <div className="dashboard-left">
          <CameraGrid cameras={visibleCameras} />

          {/* Active alerts table */}
          <ViolationTable events={activeAlerts} />
        </div>

        {/* RIGHT COLUMN */}
        <div className="dashboard-right">
          <GlobalStatsPanel metrics={metrics} />

          {/* Occupancy Trend */}
          <div className="analytics-card">
            <OccupancyChart trend={occupancyTrend} />
          </div>

          {/* PPE Compliance */}
          <div className="analytics-card donut-card">
            <PPEComplianceDonut
              cameras={cameras}
              compliance={smoothedCompliance}
            />
          </div>
        </div>

      </div>
    </div>
  );
}
