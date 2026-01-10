export default function Topbar() {
  const now = new Date().toLocaleTimeString();

  return (
    <header className="topbar">

      {/* LEFT  */}
      <div className="topbar-left"></div>

      {/* CENTER TITLE */}
      <div className="topbar-center">
        <h2>SafetyEye Monitoring System</h2>
      </div>

      {/* RIGHT USER */}
      <div className="topbar-right">
        Admin • {now}
      </div>

    </header>
  );
}
