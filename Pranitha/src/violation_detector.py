from ultralytics import YOLO
import os

# 1. Load  Trained Model
model = YOLO("models/best.pt")

# 2. Violation Checking Logic
def check_violations(result):
    """
    Takes a YOLO result object and returns a list of detected violations.
    """

    names = result.names                   # Class name dictionary
    classes = result.boxes.cls.tolist()    # Detected class IDs
    detected = [names[int(c)] for c in classes]  # Convert IDs → names

    violations = []

    # Only check for PPE violations if a person is detected
    if "Person" in detected:
        if "No_Hardhat" in detected:
            violations.append("Worker without Helmet")
        if "No_Vest" in detected:
            violations.append("Worker without Safety Vest")
        if "No_Gloves" in detected:
            violations.append(" Worker without Gloves")

    return violations


# 3. Folder Containing Images for Detection
folder = "data/raw/source_files/source_files"


if not os.path.exists(folder):
    print(f"Folder not found: {folder}")
    exit()



# 4. Valid Image Extensions
valid_exts = (".jpg", ".jpeg", ".png")


# 5. Process Every Image in the Folder
for file in os.listdir(folder):

    # Skip non-image files (mp4, jfif, etc.)
    if not file.lower().endswith(valid_exts):
        print(f"Skipping unsupported file: {file}")
        continue

    # Full path to the image
    img_path = os.path.join(folder, file)
    print(f"\n🔍 Processing: {img_path}")

    # Run YOLO prediction
    results = model.predict(img_path, conf=0.5)

    # For each result (usually just one)
    for r in results:

        # Check for safety violations
        alerts = check_violations(r)

        print("Detected Violations:")
        if alerts:
            for a in alerts:
                print(a)
        else:
            print("✔ No safety violations detected")
