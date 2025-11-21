# backend/api.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import time
from typing import List
from db import init_db, fetch_recent, stats_over_time, counts_by_violation

BASE = Path(__file__).resolve().parent
MEDIA = BASE / "media"
MEDIA.mkdir(exist_ok=True)

# Initialize database
init_db()

# Read class names from classes.txt
CLASS_PATH = BASE / "classes.txt"

def _read_class_names() -> List[str]:
    if CLASS_PATH.exists():
        return [l.strip() for l in CLASS_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    return []

CLASS_NAMES = _read_class_names()

app = FastAPI(title="SafetyEye Backend", version="1.0.0")

# ✅ CORS Middleware - Allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _to_media_url(image_path_value: str) -> str:
    """Convert stored image path to frontend-accessible URL."""
    if not image_path_value:
        return ""
    img = str(image_path_value).strip()
    if img.lower().startswith(("http://", "https://")):
        return img
    if img.startswith("/media/"):
        return img
    p = Path(img)
    if p.is_absolute():
        return f"/media/{p.name}"
    return f"/media/{img}"


@app.get("/")
def root():
    return {"service": "SafetyEye Backend", "status": "ok", "version": "1.0.0"}


@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}


@app.get("/api/detections")
def get_detections(limit: int = 100):
    """Returns recent detections with class names and image URLs."""
    try:
        data = fetch_recent(limit)
        
        for d in data:
            # Attach human-readable class name
            cls_val = d.get("class")
            cls_idx = None
            try:
                if cls_val is not None:
                    cls_idx = int(cls_val)
            except (ValueError, TypeError):
                cls_idx = None

            if isinstance(cls_idx, int) and 0 <= cls_idx < len(CLASS_NAMES):
                d["class_name"] = CLASS_NAMES[cls_idx]
            else:
                d["class_name"] = str(cls_val) if cls_val else "unknown"

            # Normalize image path to URL
            d["image_url"] = _to_media_url(d.get("image_path", ""))

        return JSONResponse(content={"detections": data, "count": len(data)})
    except Exception as e:
        return JSONResponse(content={"detections": [], "error": str(e)}, status_code=500)


@app.get("/api/stats/hourly")
def hourly():
    """Returns detection counts grouped by hour."""
    try:
        data = stats_over_time()
        return JSONResponse(content={"data": data})
    except Exception as e:
        return JSONResponse(content={"data": [], "error": str(e)}, status_code=500)


@app.get("/api/stats/violations")
def violations():
    """Returns violation counts by type."""
    try:
        data = counts_by_violation()
        return JSONResponse(content={"data": data})
    except Exception as e:
        return JSONResponse(content={"data": [], "error": str(e)}, status_code=500)


@app.get("/api/stats/summary")
def summary():
    """Returns overall statistics summary."""
    try:
        detections = fetch_recent(1000)
        total = len(detections)
        violations_count = sum(1 for d in detections if d.get("violation_type"))
        compliance_rate = ((total - violations_count) / total * 100) if total > 0 else 100
        
        return JSONResponse(content={
            "total_detections": total,
            "total_violations": violations_count,
            "compliance_rate": round(compliance_rate, 1),
            "classes": CLASS_NAMES
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/media/last_frame")
def last_frame():
    """Serves the latest camera frame."""
    path = MEDIA / "last_frame.jpg"
    if path.exists():
        return FileResponse(
            path, 
            media_type="image/jpeg",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return Response(status_code=404, content="No frame available")


@app.get("/media/{filename:path}")
def media_file(filename: str):
    """Serves media files (violation snapshots, etc.)."""
    file_path = MEDIA / filename
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")


@app.post("/api/upload_test")
async def upload_test(image: UploadFile = File(...)):
    """Debug endpoint - saves uploaded file and returns URL."""
    dest = MEDIA / f"uploaded_{int(time.time() * 1000)}_{image.filename}"
    content = await image.read()
    with open(dest, "wb") as f:
        f.write(content)
    return {"path": str(dest), "url": _to_media_url(dest.name)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)