import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import { Box, Chip, Stack, Typography } from "@mui/material";
import Grid from "@mui/material/Grid";
import { statsCards } from "../data/mockData";

export function StatsHighlights() {
  return (
    <Grid container spacing={3}>
      {statsCards.map((card) => (
        <Grid key={card.label} item xs={12} sm={6} lg={3}>
          <Box
            sx={{
              borderRadius: 4,
              px: 3,
              py: 2.5,
              minHeight: 160,
              background: card.gradient,
              bgcolor: "rgba(5, 11, 26, 0.65)",
              border: "1px solid rgba(233,243,255,0.08)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              position: "relative",
              overflow: "hidden"
            }}
          >
            <Box
              sx={{
                position: "absolute",
                inset: 0,
                opacity: 0.5,
                background: "radial-gradient(80% 100% at 90% 10%, rgba(255,255,255,0.18) 0%, transparent 60%)"
              }}
            />
            <Stack spacing={1} sx={{ position: "relative", zIndex: 1 }}>
              <Chip
                label={card.chip}
                size="small"
                sx={{
                  alignSelf: "flex-start",
                  borderRadius: 999,
                  bgcolor: "rgba(5,11,26,0.35)",
                  color: "text.secondary",
                  border: "1px solid rgba(233,243,255,0.12)"
                }}
              />
              <Typography variant="subtitle1" sx={{ color: "text.secondary" }}>
                {card.label}
              </Typography>
              <Typography variant="h4" component="p" sx={{ fontWeight: 700 }}>
                {card.value}
              </Typography>
            </Stack>
            <Stack direction="row" spacing={1} alignItems="center" sx={{ position: "relative", zIndex: 1 }}>
              {card.trend === "up" ? (
                <TrendingUpIcon fontSize="small" sx={{ color: "success.main" }} />
              ) : (
                <TrendingDownIcon fontSize="small" sx={{ color: "warning.main" }} />
              )}
              <Typography variant="body2" sx={{ color: card.trend === "up" ? "success.main" : "warning.main", fontWeight: 600 }}>
                {card.delta}
              </Typography>
            </Stack>
          </Box>
        </Grid>
      ))}
    </Grid>
  );
}

