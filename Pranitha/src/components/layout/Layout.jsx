import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="app-shell">
      {/* Left sidebar */}
      <Sidebar />

      {/* Main area */}
      <div className="app-main">
        {/* Top header */}
        <Topbar />

        {/* Routed page content */}
        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
