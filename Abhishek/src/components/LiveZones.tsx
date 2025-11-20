import SensorsIcon from "@mui/icons-material/Sensors";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import { Avatar, Box, Card, CardContent, CardHeader, LinearProgress, Stack, Typography } from "@mui/material";
import { zoneStatuses } from "../data/mockData";

export function LiveZones() {
  return (
    <Card sx={{ height: "100%" }}>
      <CardHeader
        title="Live Zone Overview"
        subheader="Capacity, dwell time, and compliance insights"
        action={
          <Stack direction="row" spacing={1} alignItems="center" sx={{ color: "text.secondary" }}>
            <SensorsIcon fontSize="small" />
            <Typography variant="body2">16 cameras streaming</Typography>
          </Stack>
        }
        sx={{ pb: 0 }}
      />
      <CardContent>
        <Stack spacing={2.5}>
          {zoneStatuses.map((zone) => {
            const occupancyPct = Math.round((zone.occupancy / zone.capacity) * 100);
            return (
              <Stack
                key={zone.name}
                direction={{ xs: "column", sm: "row" }}
                spacing={2}
                sx={{
                  px: 2,
                  py: 1.5,
                  borderRadius: 3,
                  backgroundColor: "rgba(5,11,26,0.35)",
                  border: "1px solid rgba(233,243,255,0.06)"
                }}
                alignItems={{ xs: "flex-start", sm: "center" }}
                justifyContent="space-between"
              >
                <Stack direction="row" spacing={2} alignItems="center">
                  <Avatar
                    sx={{
                      bgcolor: "rgba(31,81,255,0.22)",
                      border: "1px solid rgba(31,81,255,0.35)",
                      width: 48,
                      height: 48
                    }}
                  >
                    <TimelineOutlinedIcon sx={{ color: "primary.main" }} />
                  </Avatar>
                  <Stack spacing={0.5}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {zone.name}
                    </Typography>
                    <Typography variant="body2" sx={{ color: "text.secondary" }}>
                      Last incident: {zone.lastIncident}
                    </Typography>
                  </Stack>
                </Stack>

                <Box sx={{ flexGrow: 1, maxWidth: 280 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="body2" sx={{ color: "text.secondary" }}>
                      {zone.occupancy} / {zone.capacity} occupants
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ color: occupancyPct > 85 ? "warning.main" : "success.main", fontWeight: 600 }}
                    >
                      {occupancyPct}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={occupancyPct}
                    sx={{
                      height: 8,
                      borderRadius: 999,
                      backgroundColor: "rgba(233,243,255,0.08)",
                      "& .MuiLinearProgress-bar": {
                        borderRadius: 999,
                        background: occupancyPct > 85 ? "linear-gradient(90deg, #F97316, #FACC15)" : "linear-gradient(90deg, #14C1C7, #1F51FF)"
                      }
                    }}
                  />
                </Box>

                <Stack spacing={0.5} alignItems={{ xs: "flex-start", sm: "flex-end" }}>
                  <Typography variant="body2" sx={{ color: "text.secondary" }}>
                    Compliance Score
                  </Typography>
                  <Typography variant="h6" sx={{ color: zone.compliance > 90 ? "success.main" : "warning.main", fontWeight: 700 }}>
                    {zone.compliance}%
                  </Typography>
                </Stack>
              </Stack>
            );
          })}
        </Stack>
      </CardContent>
    </Card>
  );
}

