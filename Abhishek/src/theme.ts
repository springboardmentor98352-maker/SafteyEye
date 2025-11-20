import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#14C1C7"
    },
    secondary: {
      main: "#1F51FF"
    },
    background: {
      default: "#050B1A",
      paper: "#0A1328"
    },
    text: {
      primary: "#E9F3FF",
      secondary: "#8EA4CF"
    },
    success: {
      main: "#4ADE80"
    },
    warning: {
      main: "#FACC15"
    },
    error: {
      main: "#F97316"
    }
  },
  typography: {
    fontFamily: ["'Inter'", "system-ui", "sans-serif"].join(","),
    h4: {
      fontWeight: 700,
      letterSpacing: "0.01em"
    },
    h6: {
      fontWeight: 600,
      letterSpacing: "0.02em"
    },
    subtitle1: {
      fontWeight: 500,
      letterSpacing: "0.04em",
      textTransform: "uppercase"
    }
  },
  shape: {
    borderRadius: 18
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 999
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "linear-gradient(145deg, rgba(20,193,199,0.08), rgba(31,81,255,0.08))",
          border: "1px solid rgba(228,242,255,0.04)",
          boxShadow: "0 18px 40px rgba(5, 11, 26, 0.45)"
        }
      }
    }
  }
});

