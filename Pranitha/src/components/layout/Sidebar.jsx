import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Home */}
      <NavLink to="/" className="nav-item" title="Home">
        🏠
      </NavLink>

      {/* Live Cameras */}
      <NavLink to="/cameras" className="nav-item" title="Cameras">
        📷
      </NavLink>

      {/* Alerts */}
      <NavLink to="/alerts" className="nav-item" title="Alerts">
        ⚠️
      </NavLink>

      {/* Reports */}
      <NavLink to="/reports" className="nav-item" title="Reports">
        📊
      </NavLink>

      {/* Violations */}
      <NavLink to="/violations" className="nav-item" title="Violations">
        🚨
      </NavLink>
    </aside>
  );
}
