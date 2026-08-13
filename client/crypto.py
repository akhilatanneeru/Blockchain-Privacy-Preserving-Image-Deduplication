from cryptography.fernet import Fernet


def generate_aes_key():
    return Fernet.generate_key()


def encrypt_image(image_bytes, aes_key):

    cipher = Fernet(aes_key)

    return cipher.encrypt(image_bytes)


def decrypt_image(encrypted_data, aes_key):

    cipher = Fernet(aes_key)

    return cipher.decrypt(encrypted_data)