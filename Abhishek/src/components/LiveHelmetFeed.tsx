import VideocamOutlinedIcon from "@mui/icons-material/VideocamOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import { Box, Card, CardContent, CardHeader, Chip, Stack, Typography } from "@mui/material";
import { keyframes } from "@mui/material/styles";

const detectionPulse = keyframes`
  0% {
    box-shadow: 0 0 0 0 rgba(20, 193, 199, 0.45);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(20, 193, 199, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(20, 193, 199, 0);
  }
`;

const detections = [
  {
    id: "operator-01",
    label: "Helmet On",
    confidence: "98%",
    compliance: "Compliant",
    color: "#14C1C7",
    box: { top: "18%", left: "14%", width: "22%", height: "42%" }
  },
  {
    id: "operator-02",
    label: "No Helmet",
    confidence: "87%",
    compliance: "Violation",
    color: "#F97316",
    box: { top: "28%", left: "44%", width: "19%", height: "38%" }
  },
  {
    id: "operator-03",
    label: "Helmet On",
    confidence: "94%",
    compliance: "Compliant",
    color: "#14C1C7",
    box: { top: "22%", left: "68%", width: "20%", height: "40%" }
  }
];

export function LiveHelmetFeed() {
  return (
    <Card>
      <CardHeader
        title="Live PPE Compliance Feed"
        subheader="AI detection stream · Assembly Bay 3"
        action={
          <Stack direction="row" spacing={1} alignItems="center">
            <Chip
              icon={<VideocamOutlinedIcon fontSize="small" />}
              label="CAM-AB-3"
              sx={{ borderRadius: 999, border: "1px solid rgba(233,243,255,0.12)", color: "text.secondary" }}
            />
          </Stack>
        }
        sx={{ pb: 0 }}
      />
      <CardContent>
        <Stack spacing={2}>
          <Box
            sx={{
              position: "relative",
              borderRadius: 4,
              overflow: "hidden",
              border: "1px solid rgba(233,243,255,0.08)",
              background: "linear-gradient(160deg, rgba(20,193,199,0.18), rgba(31,81,255,0.12))"
            }}
          >
            <Box
              component="video"
              src="/helmet.jpg"
              poster="/helmet.jpg"
              autoPlay
              loop
              muted
              playsInline
              sx={{
                display: "block",
                width: "100%",
                filter: "saturate(1.05)",
                objectFit: "cover",
                maxHeight: { xs: 260, md: 320 }
              }}
            />

            {detections.map((target) => (
              <Box
                key={target.id}
                sx={{
                  position: "absolute",
                  border: `2px solid ${target.color}`,
                  borderRadius: 2,
                  ...target.box,
                  animation: `${detectionPulse} 3s ease-in-out infinite`,
                  backdropFilter: "blur(1px)"
                }}
              >
                <Stack
                  direction="row"
                  spacing={1}
                  alignItems="center"
                  sx={{
                    position: "absolute",
                    bottom: "100%",
                    left: 0,
                    transform: "translateY(-6px)",
                    bgcolor: "rgba(5,11,26,0.85)",
                    borderRadius: 999,
                    border: `1px solid rgba(233,243,255,0.12)`,
                    px: 1.2,
                    py: 0.4
                  }}
                >
                  <Box sx={{ width: 8, height: 8, borderRadius: "50%", bgcolor: target.color }} />
                  <Typography variant="caption" sx={{ fontWeight: 600 }}>
                    {target.label}
                  </Typography>
                  <Typography variant="caption" sx={{ color: "text.secondary" }}>
                    {target.confidence}
                  </Typography>
                </Stack>
              </Box>
            ))}

            <Stack
              direction={{ xs: "column", sm: "row" }}
              spacing={{ xs: 1, sm: 3 }}
              sx={{
                position: "absolute",
                left: 0,
                right: 0,
                bottom: 0,
                bgcolor: "linear-gradient(180deg, rgba(5,11,26,0) 0%, rgba(5,11,26,0.85) 60%, rgba(5,11,26,0.95) 100%)",
                px: 3,
                py: { xs: 2, sm: 2.5 }
              }}
            >
              <Stack direction="row" spacing={1.5} alignItems="center">
                <VisibilityOutlinedIcon sx={{ color: "primary.main" }} />
                <Typography variant="subtitle2" sx={{ color: "primary.main", fontWeight: 600 }}>
                  3 subjects tracked · 2 compliant
                </Typography>
              </Stack>
              <Stack direction={{ xs: "column", sm: "row" }} spacing={{ xs: 0.5, sm: 3 }} sx={{ color: "text.secondary" }}>
                <Typography variant="caption">Auto-notify Safety Officer</Typography>
                <Typography variant="caption">Last frame analyzed: 320ms ago</Typography>
              </Stack>
            </Stack>
          </Box>

          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            {detections.map((target) => (
              <Stack
                key={`${target.id}-meta`}
                spacing={0.3}
                sx={{
                  flex: 1,
                  px: 2,
                  py: 1.5,
                  borderRadius: 3,
                  border: "1px solid rgba(233,243,255,0.06)",
                  bgcolor: "rgba(5,11,26,0.45)"
                }}
              >
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2" sx={{ color: "text.secondary" }}>
                    {target.id}
                  </Typography>
                  <Chip
                    size="small"
                    label={target.compliance}
                    sx={{
                      borderRadius: 999,
                      bgcolor: "transparent",
                      border: `1px solid ${target.color}`,
                      color: target.color,
                      fontWeight: 600
                    }}
                  />
                </Stack>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {target.label}
                </Typography>
                <Typography variant="caption" sx={{ color: "text.secondary" }}>
                  Confidence {target.confidence}
                </Typography>
              </Stack>
            ))}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}

