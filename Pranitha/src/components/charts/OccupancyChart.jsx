import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function OccupancyChart({ trend = [] }) {
  if (!Array.isArray(trend) || trend.length === 0) {
    return <div className="empty-state">Waiting for data…</div>;
  }

  return (
    <div className="analytics-card chart">
      <h4 className="card-title">Occupancy Trend</h4>

      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={trend}>
          <XAxis
            dataKey="ts"
            tickFormatter={ts =>
              new Date(ts).toLocaleTimeString()
            }
          />
          <YAxis allowDecimals={false} />
          <Tooltip
            labelFormatter={ts =>
              new Date(ts).toLocaleTimeString()
            }
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#4f46e5"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
