import CameraCard from "./CameraCard";

export default function CameraGrid({ cameras = {}, limit = 4 }) {
  const ORDER = ["cam1", "cam2", "cam3", "cam4"];

  const list = ORDER
    .map((id) => ({ id, data: cameras[id] }))
    .filter((c) => c.data)
    .slice(0, limit);

  if (list.length === 0) {
    return <div className="empty-state">Waiting for camera streams…</div>;
  }

  return (
    <div className="camera-grid">
      {list.map(({ id, data }) => (
        <CameraCard key={id} camId={id} data={data} />
      ))}
    </div>
  );
}
