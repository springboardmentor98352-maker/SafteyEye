export const occupancyTrend = [
  { time: "08:00", occupancy: 24, capacity: 60 },
  { time: "09:00", occupancy: 41, capacity: 60 },
  { time: "10:00", occupancy: 52, capacity: 60 },
  { time: "11:00", occupancy: 58, capacity: 60 },
  { time: "12:00", occupancy: 47, capacity: 60 },
  { time: "13:00", occupancy: 43, capacity: 60 },
  { time: "14:00", occupancy: 55, capacity: 60 },
  { time: "15:00", occupancy: 57, capacity: 60 },
  { time: "16:00", occupancy: 50, capacity: 60 },
  { time: "17:00", occupancy: 36, capacity: 60 }
];

export const complianceRadar = [
  { category: "PPE Compliance", score: 92 },
  { category: "Emergency Access", score: 86 },
  { category: "Safe Distance", score: 78 },
  { category: "Hazard Detection", score: 83 },
  { category: "Zone Integrity", score: 90 }
];

export const latestAlerts = [
  {
    id: "AL-1024",
    title: "Helmet Missing",
    description: "2 operators detected without helmets in Assembly Bay 3.",
    severity: "high",
    timestamp: "5 min ago",
    camera: "CAM-AB-3"
  },
  {
    id: "AL-1023",
    title: "Fire Exit Obstruction",
    description: "Pallet temporarily blocking the north emergency exit.",
    severity: "medium",
    timestamp: "12 min ago",
    camera: "CAM-NX-1"
  },
  {
    id: "AL-1022",
    title: "Overcrowding Risk",
    description: "Occupancy reached 90% in Collaboration Zone.",
    severity: "medium",
    timestamp: "25 min ago",
    camera: "CAM-CZ-2"
  },
  {
    id: "AL-1021",
    title: "Unauthorized Entry",
    description: "Badge mismatch detected at Robotics Lab door.",
    severity: "low",
    timestamp: "40 min ago",
    camera: "CAM-RL-1"
  }
];

export const zoneStatuses = [
  {
    name: "Robotics Lab",
    occupancy: 18,
    capacity: 24,
    compliance: 96,
    lastIncident: "2h ago"
  },
  {
    name: "Assembly Bay 3",
    occupancy: 22,
    capacity: 26,
    compliance: 82,
    lastIncident: "5 min ago"
  },
  {
    name: "Collaboration Hub",
    occupancy: 31,
    capacity: 40,
    compliance: 88,
    lastIncident: "24 min ago"
  },
  {
    name: "Warehouse West",
    occupancy: 14,
    capacity: 28,
    compliance: 91,
    lastIncident: "1h ago"
  }
];

export const statsCards = [
  {
    label: "Live Occupancy",
    value: "218",
    delta: "+12 vs 1h",
    trend: "up",
    chip: "73% capacity",
    gradient: "linear-gradient(135deg, rgba(31, 81, 255, 0.32), rgba(20, 193, 199, 0.16))"
  },
  {
    label: "Safety Compliance",
    value: "92%",
    delta: "+4% vs AVG",
    trend: "up",
    chip: "High adherence",
    gradient: "linear-gradient(135deg, rgba(74, 222, 128, 0.28), rgba(20, 193, 199, 0.12))"
  },
  {
    label: "Active Alerts",
    value: "8",
    delta: "-3 vs yesterday",
    trend: "down",
    chip: "2 critical",
    gradient: "linear-gradient(135deg, rgba(249, 115, 22, 0.28), rgba(250, 204, 21, 0.12))"
  },
  {
    label: "Average Dwell Time",
    value: "42m",
    delta: "-5m vs last week",
    trend: "down",
    chip: "Target 45m",
    gradient: "linear-gradient(135deg, rgba(20, 193, 199, 0.22), rgba(31, 81, 255, 0.18))"
  }
];

