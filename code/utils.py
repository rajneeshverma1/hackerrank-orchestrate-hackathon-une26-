import base64
import csv
from io import BytesIO
from typing import List, Dict, Any
from PIL import Image

def encode_image(image_path: str) -> str:
    """Read an image, resize/compress it if needed, and return its base64 string."""
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            max_size = 1024
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error compressing image {image_path}: {e}. Falling back to raw bytes.")
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as fallback_err:
            print(f"Fallback encoding failed for {image_path}: {fallback_err}")
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
