import { Box, Button, Chip, Stack, Typography } from "@mui/material";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import InsightsOutlinedIcon from "@mui/icons-material/InsightsOutlined";
import ShieldOutlinedIcon from "@mui/icons-material/ShieldOutlined";

export function DashboardHeader() {
  return (
    <Box
      sx={{
        borderRadius: 4,
        px: 4,
        py: 3,
        mb: 4,
        position: "relative",
        overflow: "hidden",
        bgcolor: "background.paper"
      }}
    >
      <Box
        sx={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(120% 140% at 100% 0%, rgba(31,81,255,0.35) 0%, rgba(20,193,199,0.05) 55%, transparent 100%)",
          opacity: 0.9
        }}
      />

      <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" alignItems={{ xs: "flex-start", md: "center" }} spacing={3} position="relative" zIndex={1}>
        <Stack spacing={1.2}>
          <Stack direction="row" spacing={1.5} alignItems="center">
            <Chip label="Live AI Monitoring" color="secondary" variant="outlined" sx={{ borderRadius: 999, borderColor: "rgba(20,193,199,0.35)", color: "text.secondary" }} />
            <Chip
              icon={<ShieldOutlinedIcon fontSize="small" />}
              label="SafetyEye"
              color="primary"
              sx={{ borderRadius: 999 }}
            />
          </Stack>
          <Typography variant="h4" component="h1">
            SafetyEye – Workplace Occupancy & Safety Intelligence
          </Typography>
          <Typography variant="body1" sx={{ color: "text.secondary", maxWidth: 640 }}>
            Monitor capacity, identify safety risks, and orchestrate rapid responses through AI-powered surveillance insights. Every data point is derived from real-time video analytics across your facility.
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            <Button variant="contained" color="primary" startIcon={<InsightsOutlinedIcon />}>
              Generate Report
            </Button>
            <Button variant="outlined" color="secondary" startIcon={<NotificationsNoneIcon />}>
              Manage Alerts
            </Button>
          </Stack>
        </Stack>
        <Box
          sx={{
            borderRadius: 3,
            px: 3,
            py: 2,
            background: "linear-gradient(160deg, rgba(20,193,199,0.18), rgba(31,81,255,0.12))",
            border: "1px solid rgba(233,243,255,0.12)",
            minWidth: { xs: "100%", md: 240 }
          }}
        >
          <Typography variant="subtitle1" sx={{ color: "text.secondary", mb: 0.5 }}>
            Monitoring Status
          </Typography>
          <Typography variant="h5" sx={{ fontWeight: 700 }}>
            Stable · On Track
          </Typography>
          <Stack spacing={1.2} mt={2}>
            <Stack direction="row" spacing={1.5} alignItems="center" sx={{ color: "success.main" }}>
              <Box sx={{ width: 10, height: 10, borderRadius: "50%", bgcolor: "success.main", boxShadow: "0 0 12px rgba(74,222,128,0.7)" }} />
              <Typography variant="body2">16/16 AI nodes online</Typography>
            </Stack>
            <Stack direction="row" spacing={1.5} alignItems="center">
              <Box sx={{ width: 10, height: 10, borderRadius: "50%", bgcolor: "warning.main", boxShadow: "0 0 10px rgba(250,204,21,0.6)" }} />
              <Typography variant="body2" sx={{ color: "warning.main" }}>
                4 zones nearing capacity
              </Typography>
            </Stack>
            <Stack direction="row" spacing={1.5} alignItems="center">
              <Box sx={{ width: 10, height: 10, borderRadius: "50%", bgcolor: "primary.main", boxShadow: "0 0 10px rgba(20,193,199,0.6)" }} />
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                SLA compliance at 99.4%
              </Typography>
            </Stack>
          </Stack>
        </Box>
      </Stack>
    </Box>
  );
}

