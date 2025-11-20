import NotificationsActiveOutlinedIcon from "@mui/icons-material/NotificationsActiveOutlined";
import WarningAmberOutlinedIcon from "@mui/icons-material/WarningAmberOutlined";
import ShieldMoonOutlinedIcon from "@mui/icons-material/ShieldMoonOutlined";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { Avatar, Box, Button, Card, CardContent, CardHeader, Chip, Stack, Typography } from "@mui/material";
import { latestAlerts } from "../data/mockData";

const severityColors: Record<string, string> = {
  high: "#F97316",
  medium: "#FACC15",
  low: "#38BDF8"
};

const severityLabels: Record<string, string> = {
  high: "Critical",
  medium: "Warning",
  low: "Notice"
};

export function AlertsFeed() {
  return (
    <Card sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <CardHeader
        title="Live Safety Alerts"
        subheader="AI prioritizes by impact and urgency"
        action={
          <Chip
            icon={<ShieldMoonOutlinedIcon fontSize="small" />}
            label="Auto-escalation active"
            sx={{ borderRadius: 999, color: "text.secondary", border: "1px solid rgba(233,243,255,0.12)" }}
          />
        }
        sx={{ pb: 0 }}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Stack spacing={2.2}>
          {latestAlerts.map((alert) => (
            <Stack
              key={alert.id}
              direction="row"
              spacing={2}
              alignItems="center"
              sx={{
                px: 2,
                py: 1.8,
                borderRadius: 4,
                backgroundColor: "rgba(5,11,26,0.45)",
                border: "1px solid rgba(233,243,255,0.08)"
              }}
            >
              <Avatar
                sx={{
                  width: 56,
                  height: 56,
                  bgcolor: severityColors[alert.severity],
                  color: "#050B1A",
                  fontWeight: 700
                }}
              >
                {alert.severity === "high" ? <WarningAmberOutlinedIcon /> : <NotificationsActiveOutlinedIcon />}
              </Avatar>
              <Stack spacing={0.5} sx={{ flexGrow: 1 }}>
                <Stack direction={{ xs: "column", sm: "row" }} spacing={1} alignItems={{ xs: "flex-start", sm: "center" }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    {alert.title}
                  </Typography>
                  <Chip
                    size="small"
                    label={severityLabels[alert.severity]}
                    sx={{
                      borderRadius: 999,
                      fontWeight: 600,
                      bgcolor: "transparent",
                      border: `1px solid ${severityColors[alert.severity]}`,
                      color: severityColors[alert.severity]
                    }}
                  />
                </Stack>
                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  {alert.description}
                </Typography>
                <Stack direction="row" spacing={2} sx={{ color: "text.secondary", fontSize: 12 }}>
                  <Typography variant="caption">#{alert.id}</Typography>
                  <Typography variant="caption">{alert.timestamp}</Typography>
                  <Typography variant="caption">Camera: {alert.camera}</Typography>
                </Stack>
              </Stack>
              <Button
                variant="text"
                endIcon={<ChevronRightIcon />}
                sx={{
                  color: "primary.main",
                  borderRadius: 999,
                  textTransform: "none",
                  fontWeight: 600
                }}
              >
                Investigate
              </Button>
            </Stack>
          ))}
        </Stack>
      </CardContent>
      <Box px={3} pb={3}>
        <Button fullWidth variant="outlined" sx={{ borderRadius: 999 }}>
          View Incident Playbooks
        </Button>
      </Box>
    </Card>
  );
}

