import React from "react";
import { Routes, Route } from "react-router-dom";

import Layout from "./components/layout/Layout";

import Home from "./pages/Home";
import Cameras from "./pages/Cameras";
import Violations from "./pages/Violations";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";

export default function App() {
  return (
    <Routes>

      {/* Shared layout */}
      <Route element={<Layout />}>

        {/* Pages */}
        <Route path="/" element={<Home />} />
        <Route path="/cameras" element={<Cameras />} />
        <Route path="/violations" element={<Violations />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/reports" element={<Reports />} />

      </Route>

    </Routes>
  );
}
