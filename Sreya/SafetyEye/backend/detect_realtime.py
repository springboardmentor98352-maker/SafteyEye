# backend/detect_realtime.py
import argparse
import time
import random
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
from db import insert_detection, init_db

BASE = Path(__file__).resolve().parent
MEDIA = BASE / 'media'
MODELS_DIR = BASE / 'models'
MEDIA.mkdir(parents=True, exist_ok=True)

# Initialize database
init_db()

# Load class names
CLASS_PATH = BASE / "classes.txt"
CLASS_NAMES = []
if CLASS_PATH.exists():
    CLASS_NAMES = [l.strip() for l in CLASS_PATH.read_text().splitlines() if l.strip()]

def iou(boxA, boxB):
    """Calculate Intersection over Union between two boxes."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH
    
    areaA = max(0, boxA[2] - boxA[0]) * max(0, boxA[3] - boxA[1])
    areaB = max(0, boxB[2] - boxB[0]) * max(0, boxB[3] - boxB[1])
    
    union = areaA + areaB - interArea
    return interArea / union if union > 0 else 0.0

def box_to_int(box):
    """Convert box coordinates to integers."""
    return [int(round(x)) for x in box]

def get_class_name(cls_idx):
    """Get class name from index."""
    if 0 <= cls_idx < len(CLASS_NAMES):
        return CLASS_NAMES[cls_idx]
    return str(cls_idx)

def run(weights: str,
        source: str = "0",
        imgsz: int = 640,
        conf_threshold: float = 0.35,
        iou_head_threshold: float = 0.05,
        save_violations: bool = True,
        camera_name: str = "cam1"):
    
    print(f"[INFO] Loading model from: {weights}")
    
    if not Path(weights).exists():
        print(f"[ERROR] Model file not found: {weights}")
        return
    
    model = YOLO(weights)
    
    # --- SOURCE HANDLING ---
    source_path = Path(source)
    is_directory = source_path.is_dir()
    image_files = []
    cap = None
    
    if is_directory:
        valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        image_files = [p for p in source_path.glob('*') if p.suffix.lower() in valid_exts]
        
        if not image_files:
            print(f"[ERROR] No images found in directory: {source}")
            return
        print(f"[INFO] Found {len(image_files)} test images in {source}")
        print("[INFO] Mode: Random Test Image Loop")
    else:
        source_val = int(source) if str(source).isdigit() else source
        cap = cv2.VideoCapture(source_val)
        if not cap.isOpened():
            print(f"[ERROR] Could not open video source: {source}")
            return
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        print(f"[INFO] Video source connected @ {fps:.1f} FPS")

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Define colors for ALL classes in dataset.yaml
    # BGR format
    colors = {
        'person': (200, 100, 20),    # Blue-ish
        'helmet': (20, 200, 80),     # Green
        'vest': (80, 200, 200),      # Yellow
        'no_helmet': (0, 0, 255),    # Red (Violation Class)
        'face_mask': (200, 200, 255),# Pink/White
        'boot': (50, 100, 150),      # Brown/Dark
        'gloves': (180, 50, 180),    # Purple
        'vehicle': (255, 100, 0),    # Blue
        'sign': (0, 255, 255),       # Yellow
        'other_equipment': (128, 128, 128), # Grey
        'violation': (0, 0, 255)     # Red (Generic Violation)
    }
    
    violation_cooldown = {} 
    print("[INFO] Starting inference loop. Press 'q' to quit.")
    
    try:
        while True:
            # --- FRAME ACQUISITION ---
            if is_directory:
                img_path = random.choice(image_files)
                print(f"[TEST] Processing: {img_path.name}")
                frame = cv2.imread(str(img_path))
                
                if frame is None:
                    print(f"[WARN] Could not read image {img_path}")
                    continue
                
                if frame.shape[1] > 1920: 
                    scale = 1920 / frame.shape[1]
                    frame = cv2.resize(frame, None, fx=scale, fy=scale)
            else:
                ret, frame = cap.read()
                if not ret:
                    if str(source).isdigit():
                        print("[WARN] Cannot fetch frame from camera")
                        time.sleep(0.1)
                        continue
                    else:
                        print("[INFO] End of video stream")
                        break
            
            # Run inference
            results = model(frame, imgsz=imgsz, conf=conf_threshold, verbose=False)[0]
            
            # Initialize lists for logic
            persons = []
            helmets = []
            vests = []
            boots = []
            gloves = []
            all_detections = [] # To store everything for drawing
            
            # Parse detections
            for box in results.boxes.data.tolist():
                if len(box) < 6: continue
                    
                x1, y1, x2, y2, conf, cls = box[:6]
                cls = int(cls)
                cls_name = get_class_name(cls).lower()
                bbox = [x1, y1, x2, y2]
                
                detection = {'box': bbox, 'conf': float(conf), 'class': cls, 'class_name': cls_name}
                all_detections.append(detection)
                
                # Categorize for Logic Checks
                if 'person' in cls_name:
                    persons.append(detection)
                elif any(k in cls_name for k in ['helmet', 'hardhat']):
                    helmets.append(detection)
                elif 'vest' in cls_name:
                    vests.append(detection)
                elif 'boot' in cls_name or 'shoe' in cls_name:
                    boots.append(detection)
                elif 'glove' in cls_name:
                    gloves.append(detection)
            
            # --- VIOLATION LOGIC ---
            violations = []
            
            # 1. Check each person for missing PPE
            for p in persons:
                px1, py1, px2, py2 = p['box']
                person_height = py2 - py1
                
                # Define Regions
                head_box = [px1, py1, px2, py1 + person_height * 0.3]
                torso_box = [px1, py1 + person_height * 0.2, px2, py1 + person_height * 0.6]
                feet_box = [px1, py2 - person_height * 0.2, px2, py2] # Bottom 20%
                
                # A. Check Helmet
                has_helmet = False
                for h in helmets:
                    if iou(head_box, h['box']) > iou_head_threshold:
                        # Mask Filter: Ignore "helmets" that are too low on the face
                        helmet_top = h['box'][1]
                        relative_pos = (helmet_top - py1) / person_height
                        if relative_pos > 0.10: # If starts below top 10%, it's likely a mask
                            continue
                        has_helmet = True
                        break
                
                if not has_helmet:
                    violations.append({'person': p, 'type': 'missing_helmet', 'box': p['box']})

                # B. Check Vest
                has_vest = False
                for v in vests:
                    if iou(torso_box, v['box']) > 0.05:
                        has_vest = True
                        break
                
                if not has_vest:
                    violations.append({'person': p, 'type': 'missing_vest', 'box': p['box']})

                # C. Check Boots
                has_boots = False
                for b in boots:
                    if iou(feet_box, b['box']) > 0.05:
                        has_boots = True
                        break
                
                if not has_boots:
                    # Only strict enforcement if needed, but good for visualization
                    violations.append({'person': p, 'type': 'missing_boots', 'box': p['box']})

            # 2. Check for explicit "no_helmet" class detections
            for det in all_detections:
                if 'no_helmet' in det['class_name'] or 'no helmet' in det['class_name']:
                    # This is a direct violation class
                    violations.append({'person': det, 'type': 'missing_helmet_direct', 'box': det['box']})

            # --- VISUALIZATION ---
            
            # Draw ALL regular detections first
            for det in all_detections:
                name = det['class_name']
                # Skip drawing "no_helmet" here, we draw it as a violation later
                if 'no_helmet' in name: continue 
                
                color = colors.get(name, (128, 128, 128)) # Default grey
                
                # Check if we have a specific color match
                for key in colors:
                    if key in name:
                        color = colors[key]
                        break

                x1, y1, x2, y2 = box_to_int(det['box'])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Simple label
                label = f"{name} {det['conf']:.2f}"
                cv2.putText(frame, label, (x1, max(y1 - 5, 15)), font, 0.5, color, 2)

            # Draw Violations (Overlays)
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            
            for v in violations:
                p = v['person']
                x1, y1, x2, y2 = box_to_int(p['box'])
                v_type = v['type']
                
                # Determine Label
                if 'helmet' in v_type:
                    label = "NO HELMET"
                    offset = 0
                elif 'vest' in v_type:
                    label = "NO VEST"
                    offset = 25
                elif 'boot' in v_type:
                    label = "NO BOOTS"
                    offset = 50
                else:
                    label = "VIOLATION"
                    offset = 0

                # Draw Red Box around the person/area
                cv2.rectangle(frame, (x1, y1), (x2, y2), colors['violation'], 3)
                cv2.putText(frame, label, (x1, max(25, y1 - 10) + offset), font, 0.7, colors['violation'], 2)
                
                # Database Logging & Cooldown
                cooldown_key = f"{int(x1/50)}_{int(y1/50)}_{v_type}"
                
                should_log = True
                if not is_directory:
                    if cooldown_key in violation_cooldown:
                        if time.time() - violation_cooldown[cooldown_key] < 5:
                            should_log = False
                    violation_cooldown[cooldown_key] = time.time()
                
                if should_log and save_violations:
                    snapshot_name = f"violation_{int(time.time()*1000)}.jpg"
                    snapshot_path = MEDIA / snapshot_name
                    cv2.imwrite(str(snapshot_path), frame)
                    
                    try:
                        insert_detection({
                            'ts': ts,
                            'camera': "TEST_IMG" if is_directory else camera_name,
                            'class': str(p['class']),
                            'conf': p['conf'],
                            'x1': p['box'][0], 'y1': p['box'][1], 'x2': p['box'][2], 'y2': p['box'][3],
                            'image_path': snapshot_name,
                            'violation_type': v_type
                        })
                        print(f"[VIOLATION] {label} logged.")
                    except Exception as e:
                        print(f"[ERROR] DB Insert failed: {e}")

            # Info Overlays
            cv2.putText(frame, "TEST MODE" if is_directory else ts, (10, 30), font, 0.7, (255, 255, 255), 2)
            
            # Update Dashboard Image
            try:
                cv2.imwrite(str(MEDIA / 'last_frame.jpg'), frame)
            except Exception: pass
            
            # Display
            try:
                cv2.imshow('SafetyEye', frame)
                wait_time = 2000 if is_directory else 1
                if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                    print("[INFO] 'q' pressed - exiting")
                    break
            except Exception:
                pass 
                
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    finally:
        if cap: cap.release()
        try: cv2.destroyAllWindows()
        except: pass
        print("[INFO] Detection stopped")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default=str(MODELS_DIR / 'best.pt'))
    parser.add_argument('--source', type=str, default='0', help='Path to video or FOLDER of images')
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--conf', type=float, default=0.35)
    parser.add_argument('--iou-head', type=float, default=0.05)
    parser.add_argument('--camera', type=str, default='cam1')
    parser.add_argument('--no-save', dest='save_violations', action='store_false')
    
    args = parser.parse_args()
    
    run(
        weights=args.weights,
        source=args.source,
        imgsz=args.imgsz,
        conf_threshold=args.conf,
        iou_head_threshold=args.iou_head,
        save_violations=args.save_violations,
        camera_name=args.camera
    )