import { useEffect, useRef } from "react";
import { useSocket } from "../context/SocketProvider";

export default function Alerts() {
  
  const { activeAlerts = [] } = useSocket();

  // Track previously seen alerts for sound trigger
  const prevKeys = useRef(new Set());

  // Play sound ONLY on NEW alerts
  useEffect(() => {
    const currentKeys = new Set(
      activeAlerts.map(
        a => `${a.cameraId}-${a.type}-${a.personId}`
      )
    );

    currentKeys.forEach(key => {
      if (!prevKeys.current.has(key)) {
        new Audio("/alert.mp3").play().catch(() => {});
      }
    });

    prevKeys.current = currentKeys;
  }, [activeAlerts]);

  return (
    <div className="page alerts-page">
      <h2 className="page-heading">Active Alerts</h2>

      <div className="card alerts-card">
        {activeAlerts.length === 0 ? (
          <div className="empty-state">
            No active safety alerts
          </div>
        ) : (
          <div className="alerts-grid">
            {activeAlerts.map((a, i) => (
              <div
                key={`${a.cameraId}-${a.personId}-${a.type}`}
                className={`alert-card ${
                  a.riskLevel === "HIGH"
                    ? "critical"
                    : a.riskLevel === "MEDIUM"
                    ? "danger"
                    : "warning"
                }`}
              >
                <div className="alert-title">
                  {a.type.replaceAll("_", " ")}
                </div>

                <div className="alert-meta">
                  Camera <b>{a.cameraId.toUpperCase()}</b> · Person{" "}
                  <b>{a.personId}</b>
                </div>

                <div className="alert-meta">
                  Risk: <b>{a.riskLevel}</b> · Confidence{" "}
                  <b>{a.confidence}%</b>
                </div>

                <div className="alert-meta">
                  Duration <b>{Math.floor(a.duration)}s</b>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
