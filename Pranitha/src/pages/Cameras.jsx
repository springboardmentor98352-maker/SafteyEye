import { useState } from "react";
import { useSocket } from "../context/SocketProvider";
import CameraCard from "../components/camera/CameraCard";

export default function Cameras() {
  const { cameras = {} } = useSocket();
  const [view, setView] = useState(4);

  
  const CAM_ORDER = ["cam1", "cam2", "cam3", "cam4"];

  const visibleCameras = CAM_ORDER
    .map((id) => ({ id, data: cameras[id] }))
    .filter((c) => c.data)
    .slice(0, view);

  const gridStyle =
    view === 1
      ? { gridTemplateColumns: "1fr" }
      : view === 2
      ? { gridTemplateColumns: "1fr 1fr" }
      : { gridTemplateColumns: "1fr 1fr" };

  return (
    <div className="page">
      <h3 className="page-title">Live Cameras</h3>

      {/* GRID CONTROLS */}
      <div className="camera-controls">
        <span>View:</span>
        {[1, 2, 4].map((v) => (
          <button
            key={v}
            className={view === v ? "active" : ""}
            onClick={() => setView(v)}
          >
            {v}
          </button>
        ))}
      </div>

      {/* CAMERA GRID */}
      <div className="camera-page-grid" style={gridStyle}>
        {visibleCameras.length === 0 ? (
          <div className="empty-state">No camera streams available.</div>
        ) : (
          visibleCameras.map(({ id, data }) => (
            <CameraCard key={id} camId={id} data={data} />
          ))
        )}
      </div>
    </div>
  );
}
