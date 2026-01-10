// src/components/charts/PPEComplianceDonut.jsx
// ------------------------------------------------------
// PPEComplianceDonut — PRODUCTION SAFE
// ------------------------------------------------------

import { useEffect, useMemo, useRef, useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { useSocket } from "../../context/SocketProvider";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip
} from "chart.js";

ChartJS.register(ArcElement, Tooltip);

export default function PPEComplianceDonut() {
  const { cameras = {} } = useSocket();

  const prevCompliance = useRef(null);
  const [pulse, setPulse] = useState(false);
  const [lastChangeTs, setLastChangeTs] = useState(Date.now());

  /* ---------- AGGREGATE REAL COMPLIANCE ---------- */
  const compliance = useMemo(() => {
    const values = Object.values(cameras)
      .map(c => c?.ppeCompliance)
      .filter(v => typeof v === "number");

    if (values.length === 0) return 100;

    return Math.round(
      values.reduce((a, b) => a + b, 0) / values.length
    );
  }, [cameras]);

  /* ---------- DROP DETECTION ---------- */
  useEffect(() => {
    if (
      prevCompliance.current !== null &&
      compliance < prevCompliance.current
    ) {
      setPulse(true);
      setTimeout(() => setPulse(false), 600);
    }

    if (prevCompliance.current !== compliance) {
      setLastChangeTs(Date.now());
      prevCompliance.current = compliance;
    }
  }, [compliance]);

  /* ---------- THRESHOLD COLOR ---------- */
  let statusColor = "#16a34a"; 
  let statusLabel = "Good Compliance";

  if (compliance < 80) {
    statusColor = "#f59e0b"; 
    statusLabel = "Warning";
  }

  if (compliance < 60) {
    statusColor = "#dc2626"; 
    statusLabel = "Critical";
  }

  
  const data = {
    datasets: [
      {
        data: [compliance, 100 - compliance],
        backgroundColor: [statusColor, "#e5e7eb"],
        borderWidth: 0,
        cutout: "72%"
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 300 },
    plugins: {
      tooltip: { enabled: false }
    }
  };

  const secondsAgo = Math.floor(
    (Date.now() - lastChangeTs) / 1000
  );

  /* ---------- RENDER ---------- */
  return (
    <div className={`analytics-card donut-card ${pulse ? "pulse" : ""}`}>

      {/* HEADER */}
      <div className="donut-header">
        <h4 className="analytics-title">PPE Compliance</h4>

        <div className="donut-legend vertical">
          <span className="legend-item">
            <span className="legend-dot green" />
            ≥ 80%
          </span>
          <span className="legend-item">
            <span className="legend-dot orange" />
            60–79%
          </span>
          <span className="legend-item">
            <span className="legend-dot red" />
            &lt; 60%
          </span>
        </div>
      </div>

      {/* DONUT */}
      <div className="donut-wrapper">
        <Doughnut data={data} options={options} />

        <div className="donut-center">
          <div className="donut-value">{compliance}%</div>
          <div className="donut-sub">{statusLabel}</div>
        </div>
      </div>

      {/* FOOTER */}
      <div className="donut-footer">
        Last updated {secondsAgo}s ago
      </div>

    </div>
  );
}

