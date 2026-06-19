import base64
import csv
from typing import List, Dict, Any

def encode_image(image_path: str) -> str:
    """Read an image and return its base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return ""

def load_csv(filepath: str) -> List[Dict[str, str]]:
    """Load a CSV file and return a list of dictionaries."""
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return data

def save_csv(filepath: str, fieldnames: List[str], data: List[Dict[str, Any]]):
    """Save a list of dictionaries to a CSV file."""
    try:
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
