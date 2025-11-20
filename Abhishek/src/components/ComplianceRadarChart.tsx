import { Card, CardContent, CardHeader, Stack, Typography } from "@mui/material";
import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";
import { complianceRadar } from "../data/mockData";

const tooltipStyles = {
  backgroundColor: "rgba(5, 11, 26, 0.95)",
  border: "1px solid rgba(233,243,255,0.12)",
  borderRadius: 16,
  padding: "10px 14px"
};

export function ComplianceRadarChart() {
  return (
    <Card sx={{ height: "100%" }}>
      <CardHeader
        title="Safety Compliance Pulse"
        subheader="AI-detected adherence across safety control points"
        sx={{ pb: 0 }}
      />
      <CardContent sx={{ height: 320, pt: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={complianceRadar} cx="50%" cy="50%" outerRadius="80%">
            <PolarGrid stroke="rgba(233,243,255,0.12)" />
            <PolarAngleAxis
              dataKey="category"
              tick={{ fill: "#8EA4CF", fontSize: 12 }}
              tickLine={false}
            />
            <PolarRadiusAxis
              angle={45}
              domain={[0, 100]}
              tickCount={6}
              axisLine={false}
              tick={{ fill: "#475a85", fontSize: 11 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload || payload.length === 0) {
                  return null;
                }
                const current = payload[0];
                return (
                  <Stack spacing={0.5} sx={tooltipStyles}>
                    <Typography variant="caption" sx={{ color: "text.secondary" }}>
                      {current?.payload.category}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {current?.value}% compliance
                    </Typography>
                  </Stack>
                );
              }}
            />
            <Radar
              name="Compliance"
              dataKey="score"
              stroke="#14C1C7"
              fill="#14C1C7"
              fillOpacity={0.45}
              strokeWidth={2}
            />
          </RadarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

