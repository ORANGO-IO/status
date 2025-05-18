import os
from PIL import Image


def convert_and_compress_image(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("RGB")
        img = img.resize(
            (img.size[0] // 2, img.size[1] // 2),
            resample=Image.Resampling.LANCZOS  # substitui o antigo ANTIALIAS
        )
        new_path = image_path.rsplit(".", 1)[0] + ".jpg"
        img.save(new_path, format="JPEG", optimize=True, quality=50)
        if image_path != new_path:
            os.remove(image_path)