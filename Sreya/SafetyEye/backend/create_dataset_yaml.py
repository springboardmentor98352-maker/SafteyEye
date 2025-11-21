# backend/create_dataset_yaml.py
import argparse
from pathlib import Path
import yaml

def create_yaml(base: Path, output: Path):
    classes_file = base / 'classes.txt'
    names = []
    if classes_file.exists():
        with open(classes_file, 'r') as f:
            names = [l.strip() for l in f.readlines() if l.strip() != '']
    else:
        labels = list((base / 'data' / 'labels').rglob('*.txt'))
        idxs = set()
        for lb in labels:
            for line in lb.read_text().splitlines():
                if line.strip() == '':
                    continue
                idxs.add(int(line.split()[0]))
        maxidx = max(idxs) if idxs else -1
        names = [f"class_{i}" for i in range(maxidx + 1)]
    dataset = {
        'path': str(base / 'data'),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': names
    }
    with open(output, 'w') as f:
        yaml.safe_dump(dataset, f)
    print("Wrote dataset yaml to", output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    create_yaml(Path(args.base), Path(args.output))
