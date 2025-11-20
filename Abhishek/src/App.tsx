import { Box, Container, Stack } from "@mui/material";
import Grid from "@mui/material/Grid";
import { DashboardHeader } from "./components/DashboardHeader";
import { StatsHighlights } from "./components/StatsHighlights";
import { OccupancyTrendChart } from "./components/OccupancyTrendChart";
import { ComplianceRadarChart } from "./components/ComplianceRadarChart";
import { LiveZones } from "./components/LiveZones";
import { AlertsFeed } from "./components/AlertsFeed";
import { QuickActions } from "./components/QuickActions";
import { LiveHelmetFeed } from "./components/LiveHelmetFeed";

function App() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at 20% 20%, rgba(31,81,255,0.2) 0%, transparent 30%), radial-gradient(circle at 80% 0%, rgba(20,193,199,0.18) 0%, transparent 36%), #050B1A",
        py: { xs: 4, md: 6 }
      }}
    >
      <Container maxWidth="xl">
        <DashboardHeader />
        <StatsHighlights />
        <Grid container spacing={3} sx={{ mt: 0.5 }}>
          <Grid item xs={12} md={8}>
            <Stack spacing={3}>
              <LiveHelmetFeed />
              <OccupancyTrendChart />
              <LiveZones />
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Stack spacing={3}>
              <ComplianceRadarChart />
              <AlertsFeed />
              <QuickActions />
            </Stack>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;

