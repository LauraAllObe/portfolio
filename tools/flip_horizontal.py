from PIL import Image
from pathlib import Path

# Build absolute paths safely
base_dir = Path(__file__).resolve().parent.parent  # one folder up from 'tools'
input_path = base_dir / "static" / "clouds" / "cloud7.avif"
output_path = base_dir / "static" / "clouds" / "cloud7_flipped.avif"

# Open, flip, and save
with Image.open(input_path) as img:
    flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save(output_path, format="AVIF")

print(f"✅ Flipped image saved to {output_path}")
