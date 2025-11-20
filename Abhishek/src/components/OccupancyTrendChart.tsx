import { Card, CardContent, CardHeader, Divider, Stack, Typography } from "@mui/material";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { occupancyTrend } from "../data/mockData";

const tooltipStyles = {
  backgroundColor: "rgba(5, 11, 26, 0.92)",
  border: "1px solid rgba(233,243,255,0.12)",
  borderRadius: 16,
  padding: "12px 16px"
};

export function OccupancyTrendChart() {
  return (
    <Card sx={{ height: "100%" }}>
      <CardHeader
        title="Occupancy Trend"
        subheader="Live and historical occupancy vs. threshold"
        action={
          <Stack spacing={0.5} sx={{ textAlign: "right" }}>
            <Typography variant="subtitle2" sx={{ color: "text.secondary" }}>
              Peak Utilization
            </Typography>
            <Typography variant="body1" sx={{ fontWeight: 600, color: "primary.main" }}>
              96% · 11:15 AM
            </Typography>
          </Stack>
        }
        sx={{ pb: 0 }}
      />
      <CardContent sx={{ height: 320, pt: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={occupancyTrend}>
            <defs>
              <linearGradient id="fillOccupancy" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#1F51FF" stopOpacity={0.45} />
                <stop offset="95%" stopColor="#1F51FF" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="fillCapacity" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#14C1C7" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#14C1C7" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#8EA4CF", fontSize: 12 }} />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#8EA4CF", fontSize: 12 }}
              domain={[0, 70]}
              ticks={[0, 20, 40, 60]}
              width={36}
            />
            <Tooltip
              cursor={{ strokeDasharray: "4 4", stroke: "rgba(20,193,199,0.6)" }}
              content={({ active, payload, label }) => {
                if (!active || !payload || payload.length === 0) {
                  return null;
                }
                const current = payload[0]?.value as number;
                const cap = payload[1]?.value as number;

                return (
                  <Stack spacing={1} sx={tooltipStyles}>
                    <Typography variant="caption" sx={{ color: "text.secondary" }}>
                      {label}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      Occupancy: {current} people
                    </Typography>
                    <Typography variant="body2" sx={{ color: "primary.main" }}>
                      Capacity Limit: {cap} people
                    </Typography>
                    <Typography variant="caption" sx={{ color: current > cap * 0.85 ? "warning.main" : "success.main" }}>
                      {current > cap * 0.85 ? "Approaching threshold" : "Within safe range"}
                    </Typography>
                  </Stack>
                );
              }}
            />
            <Area type="monotone" dataKey="capacity" stroke="#14C1C7" strokeWidth={1.5} fillOpacity={1} fill="url(#fillCapacity)" />
            <Area type="monotone" dataKey="occupancy" stroke="#1F51FF" strokeWidth={2} fillOpacity={1} fill="url(#fillOccupancy)" />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
      <Divider />
      <Stack direction="row" spacing={3} px={3} py={2} sx={{ color: "text.secondary" }}>
        <Stack>
          <Typography variant="caption">Avg. Occupancy</Typography>
          <Typography variant="body1" sx={{ fontWeight: 600 }}>
            48 / 60
          </Typography>
        </Stack>
        <Stack>
          <Typography variant="caption">High Alert Events</Typography>
          <Typography variant="body1" sx={{ fontWeight: 600, color: "warning.main" }}>
            3 today
          </Typography>
        </Stack>
        <Stack>
          <Typography variant="caption">Utilization</Typography>
          <Typography variant="body1" sx={{ fontWeight: 600, color: "success.main" }}>
            82% weekly
          </Typography>
        </Stack>
      </Stack>
    </Card>
  );
}

