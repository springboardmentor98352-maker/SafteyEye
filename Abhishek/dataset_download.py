import kagglehub
import zipfile
import os

# Download dataset
path = kagglehub.dataset_download("snehilsanyal/construction-site-safety-image-dataset-roboflow")

print("Dataset downloaded to:", path)

# Extract if zipped
for file in os.listdir(path):
    if file.endswith(".zip"):
        zip_path = os.path.join(path, file)
        print("Extracting:", zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path)

a="/Users/apple/Documents/Safety Eye Project/css-data/train"
b="/Users/apple/Documents/Safety Eye Project/css-data/valid"
yaml_text = f"""
train: {a}/images/train
val: {b}/images/val
nc: 3
names: ["helmet", "nohelmet", "person"]
"""

with open("data.yaml", "w") as f:
    f.write(yaml_text)

print("Created data.yaml")