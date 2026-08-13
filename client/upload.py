import os
from .preprocess import preprocess_image

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg')

def upload_image(file_path):

    if not file_path.lower().endswith(ALLOWED_EXTENSIONS):
        raise ValueError("Unsupported file type")

    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")

    image_bytes, phash = preprocess_image(file_path)

    
    print("pHash generated:", phash)

    return image_bytes, phash
