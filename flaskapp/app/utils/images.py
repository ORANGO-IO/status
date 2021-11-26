import os
from PIL import Image


def convert_compress(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize(
            (int(img.size[0]/2), int(img.size[1]/2)), Image.ANTIALIAS)
        image_path_without_extension = image_path.split('.')[0]
        img.save(f'{image_path_without_extension}.jpg',
                 optimize=True, quality=50)
        os.remove(image_path)
