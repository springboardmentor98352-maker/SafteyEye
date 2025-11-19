# src/eda.py
import os
import json
import glob
from collections import Counter
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# CONFIG: update if your dataset path differs
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")            # expected: data/train, data/valid, data/test
RESULTS_DIR = os.path.join(ROOT, "results", "eda")
SAMPLE_OUT = os.path.join(RESULTS_DIR, "samples")
os.makedirs(SAMPLE_OUT, exist_ok=True)

CLASS_NAMES = ["person", "helmet", "vest", "boots"]  

splits = ["train", "valid", "test"]

def read_label_file(lbl_path):
    """
    Read YOLO label file. Returns list of class ids (ints) and bbox counts.
    """
    classes = []
    try:
        with open(lbl_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls = int(float(parts[0]))
                    classes.append(cls)
    except Exception:
        return None
    return classes

def find_corrupt_image(img_path):
    try:
        with Image.open(img_path) as im:
            im.verify()
        return False
    except Exception:
        return True

def annotate_and_save_image(img_path, lbl_path, out_path):
    try:
        img = Image.open(img_path).convert("RGB")
        w,h = img.size
        draw = ImageDraw.Draw(img)
        if os.path.exists(lbl_path):
            with open(lbl_path) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    cls = int(float(parts[0]))
                    xc, yc, bw, bh = map(float, parts[1:5])
                    x1 = int((xc - bw/2) * w)
                    y1 = int((yc - bh/2) * h)
                    x2 = int((xc + bw/2) * w)
                    y2 = int((yc + bh/2) * h)
                    color = "green"
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
                    draw.text((x1, y1-10), CLASS_NAMES[cls] if cls < len(CLASS_NAMES) else str(cls), fill=color)
        img.save(out_path)
    except Exception as e:
        print("Failed to annotate:", img_path, e)

def main():
    summary = {
        "total_images": 0,
        "split_counts": {},
        "class_counts": Counter(),
        "objects_per_image": [],
        "empty_label_images": [],
        "missing_label_files": [],
        "corrupt_images": [],
    }

    # iterate splits
    for split in splits:
        images_folder = os.path.join(DATA_DIR, split, "images")
        labels_folder = os.path.join(DATA_DIR, split, "labels")
        if not os.path.isdir(images_folder):
            print(f"WARNING: images folder not found: {images_folder}")
            summary["split_counts"][split] = 0
            continue

        img_files = sorted(glob.glob(os.path.join(images_folder, "*.*")))
        summary["split_counts"][split] = len(img_files)
        summary["total_images"] += len(img_files)

        for i, img_path in enumerate(img_files):
            base = os.path.splitext(os.path.basename(img_path))[0]
            lbl_path = os.path.join(labels_folder, base + ".txt")

            # corrupt images
            if find_corrupt_image(img_path):
                summary["corrupt_images"].append(img_path)
                continue

            # missing label
            if not os.path.exists(lbl_path):
                summary["missing_label_files"].append(img_path)
                continue

            classes = read_label_file(lbl_path)
            if classes is None:
                summary["corrupt_images"].append(img_path)
                continue

            if len(classes) == 0:
                summary["empty_label_images"].append(img_path)

            # update class counts and objects-per-image
            for c in classes:
                summary["class_counts"][str(c)] += 1
            summary["objects_per_image"].append(len(classes))

            # save a few annotated samples (first two from each split)
            if i < 2:
                out_img = os.path.join(SAMPLE_OUT, f"{split}_{base}.jpg")
                annotate_and_save_image(img_path, lbl_path, out_img)

    # basic statistics for objects-per-image
    o = summary["objects_per_image"]
    if o:
        summary["objects_per_image_stats"] = {
            "min": int(min(o)),
            "max": int(max(o)),
            "mean": float(sum(o)/len(o)),
            "median": int(sorted(o)[len(o)//2])
        }
    else:
        summary["objects_per_image_stats"] = {"min":0,"max":0,"mean":0,"median":0}

    # map class id to names if possible
    class_counts_named = {}
    for k,v in summary["class_counts"].items():
        idx = int(k)
        name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else str(idx)
        class_counts_named[name] = v
    summary["class_counts_named"] = class_counts_named

    # write summary json
    os.makedirs(RESULTS_DIR, exist_ok=True)
    summary_file = os.path.join(RESULTS_DIR, "eda_summary.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print("EDA finished. Summary written to:", summary_file)
    print("Sample annotated images in:", SAMPLE_OUT)

if __name__ == "__main__":
    main()
