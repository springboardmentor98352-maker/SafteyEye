import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";
import { io } from "socket.io-client";

const SocketContext = createContext(null);
export const useSocket = () => useContext(SocketContext);

export function SocketProvider({ children }) {
  const socketRef = useRef(null);

  // Core state
  const [cameras, setCameras] = useState({});
  const [incidentMap, setIncidentMap] = useState({});
  const [violationHistory, setViolationHistory] = useState([]);
  const [occupancyTrend, setOccupancyTrend] = useState([]);
  const [smoothedCompliance, setSmoothedCompliance] = useState({});

  useEffect(() => {
    socketRef.current = io("http://localhost:5001", {
      transports: ["websocket"],
      reconnection: true
    });

    socketRef.current.on("camera_event", (data) => {
      const {
        camId,
        ts,
        frame,
        occupancy,
        ppeCompliance,
        persons = []
      } = data;
      if (!camId || !ts) return;

      // -------- CAMERA SNAPSHOT --------
      setCameras(prev => ({
        ...prev,
        [camId]: {
          camId,
          frame,
          occupancy,
          ppeCompliance,
          lastUpdated: ts,
          activeViolations: data.activeViolations ?? 0
        }
      }));


      // -------- OCCUPANCY TREND --------
      setOccupancyTrend(prev =>
        [...prev, { ts, value: occupancy }].slice(-60)
      );

      // -------- PPE COMPLIANCE SMOOTHING --------
      setSmoothedCompliance(prev => {
        const prevVal = prev[camId] ?? ppeCompliance;
        return {
          ...prev,
          [camId]: Math.round(prevVal * 0.8 + ppeCompliance * 0.2)
        };
      });

      // -------- STABLE INCIDENT MAP (TTL) --------
      setIncidentMap(prev => {
        const next = { ...prev };
        const now = ts;

        persons.forEach(person => {
          const { personId, risk, riskLevel, violations = [] } = person;

          violations.forEach(v => {
            const key = `${camId}-${personId}-${v.type}`;
            next[key] = {
              cameraId: camId,
              personId,
              type: v.type,
              state: v.state,
              duration: v.duration,
              confidence: v.confidence,
              risk,
              riskLevel,
              lastSeen: now
            };
          });
        });

        // TTL cleanup (5s)
        Object.keys(next).forEach(k => {
          if (now - next[k].lastSeen > 5000) delete next[k];
        });

        return next;
      });
    });

    return () => socketRef.current?.disconnect();
  }, []);

  // -------- VIOLATION HISTORY (REPORTS) --------
  useEffect(() => {
    setViolationHistory(prev => {
      const merged = [...prev];
      Object.values(incidentMap).forEach(v => {
        const exists = merged.find(m =>
          m.cameraId === v.cameraId &&
          m.personId === v.personId &&
          m.type === v.type &&
          Math.abs(m.lastSeen - v.lastSeen) < 1000
        );
        if (!exists) merged.push(v);
      });
      return merged.slice(-500);
    });
  }, [incidentMap]);

  // -------- DERIVED --------
  const activeAlerts = useMemo(
    () => Object.values(incidentMap),
    [incidentMap]
  );

  const topRisk = useMemo(() => {
    if (!activeAlerts.length) return null;
    const score = a =>
      (a.riskLevel === "HIGH" ? 3 : a.riskLevel === "MEDIUM" ? 2 : 1) *
      (a.confidence / 100) *
      Math.max(1, a.duration / 5);

    return [...activeAlerts].sort((a, b) => score(b) - score(a))[0];
  }, [activeAlerts]);

  return (
    <SocketContext.Provider
      value={{
        cameras,
        activeAlerts,
        violations: violationHistory,
        occupancyTrend,
        smoothedCompliance,
        topRisk
      }}
    >
      {children}
    </SocketContext.Provider>
  );
}
