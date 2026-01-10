import React from "react";

export default function CameraCard({ camId, data }) {
  if (!data) return null;

  const isLive = !!data.frame;

  return (
    <div className="camera-card">

      {/* HEADER */}
      <div className="camera-header">
        <span className="camera-title">{camId.toUpperCase()}</span>
        <span className={`status-badge ${isLive ? "online" : "offline"}`}>
          {isLive ? "ONLINE" : "OFFLINE"}
        </span>
      </div>

      {/* VIDEO FRAME */}
      <div className="camera-frame">

        {isLive && (
          <div className="rec-overlay">
            <span className="rec-dot" />
            REC
          </div>
        )}

        {data.frame ? (
          <img
            src={`data:image/jpeg;base64,${data.frame}`}
            alt={camId}
          />
        ) : (
          <div className="no-frame">
            NO SIGNAL
          </div>
        )}
      </div>

      {/* META */}
      <div className="camera-meta">
        <span>Occupancy: {data.occupancy ?? "-"}</span>
        <span>Violations: {data.activeViolations ?? 0}</span>
      </div>

    </div>
  );
} 

