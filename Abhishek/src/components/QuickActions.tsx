import AutoAwesomeMotionOutlinedIcon from "@mui/icons-material/AutoAwesomeMotionOutlined";
import CloudDownloadOutlinedIcon from "@mui/icons-material/CloudDownloadOutlined";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";
import UsbOutlinedIcon from "@mui/icons-material/UsbOutlined";
import { Box, Button, Card, CardContent, CardHeader, Divider, Stack, Typography } from "@mui/material";

const actions = [
  {
    title: "Deploy New Safety Model",
    description: "Promote trained PPE detection model to production cameras.",
    icon: <AutoAwesomeMotionOutlinedIcon />,
    color: "primary"
  },
  {
    title: "Download Compliance Snapshot",
    description: "Export daily compliance metrics for facility managers.",
    icon: <CloudDownloadOutlinedIcon />,
    color: "secondary"
  },
  {
    title: "Run Incident Drill Playback",
    description: "Simulate recent alerts and review AI decision paths.",
    icon: <PlayCircleOutlineIcon />,
    color: "success"
  },
  {
    title: "Calibrate Edge Sensors",
    description: "Validate camera inputs and reset analytics thresholds.",
    icon: <UsbOutlinedIcon />,
    color: "warning"
  }
];

export function QuickActions() {
  return (
    <Card sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <CardHeader
        title="Operations Center"
        subheader="Automations and workflows"
        sx={{ pb: 0 }}
      />
      <Divider />
      <CardContent sx={{ flexGrow: 1, px: 0 }}>
        <Stack spacing={0}>
          {actions.map((action, index) => (
            <Box
              key={action.title}
              sx={{
                px: 3,
                py: 2.5,
                display: "flex",
                gap: 2,
                alignItems: "center",
                bgcolor: index % 2 === 0 ? "rgba(5,11,26,0.35)" : "transparent"
              }}
            >
              <Box
                sx={{
                  width: 42,
                  height: 42,
                  borderRadius: 3,
                  display: "grid",
                  placeItems: "center",
                  bgcolor: "rgba(20,193,199,0.16)",
                  color: `${action.color}.main`
                }}
              >
                {action.icon}
              </Box>
              <Stack spacing={0.5} sx={{ flexGrow: 1 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {action.title}
                </Typography>
                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  {action.description}
                </Typography>
              </Stack>
              <Button variant="contained" color={action.color as "primary" | "secondary" | "error" | "warning" | "success"} sx={{ borderRadius: 999 }}>
                Execute
              </Button>
            </Box>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}

