import pandas as pd
from pathlib import Path

csv_path = Path("database/violations_log.csv")
fixed_path = Path("database/violations_log_fixed.csv")

rows = []

with open(csv_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

header = lines[0]

for line in lines[1:]:
    parts = line.strip().split(",")

    if len(parts) < 5:
        continue

    id = parts[0]
    timestamp = parts[-1]
    image = parts[-2]
    confidence = parts[-3]

    label = ",".join(parts[1:-3])

    rows.append([id, label, confidence, image, timestamp])

df = pd.DataFrame(
    rows,
    columns=["id", "label", "confidence", "image", "timestamp"]
)

df.to_csv(fixed_path, index=False)

print("✅ CSV fixed successfully")
