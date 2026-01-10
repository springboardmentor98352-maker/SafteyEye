import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { SocketProvider } from "./context/SocketProvider";
import App from "./App";
import "./index.css";
import {
  Chart as ChartJS,
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);


const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>

    
    <BrowserRouter>

      
      <SocketProvider>
        <App />
      </SocketProvider>

    </BrowserRouter>

  </React.StrictMode>
);
