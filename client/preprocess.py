from PIL import Image
import imagehash
import io
import hashlib

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((256, 256))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    image_bytes = buffer.getvalue()
    phash = imagehash.phash(img)

    return image_bytes, str(phash)


def generate_file_id(image_bytes):
    sha256 = hashlib.sha256()
    sha256.update(image_bytes)
    return sha256.hexdigest()