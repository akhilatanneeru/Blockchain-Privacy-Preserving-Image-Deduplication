import hashlib
import sqlite3

from client.crypto import decrypt_image

from csp.database import (
    DB_PATH,
    get_file_key
)

from blockchain.eth_chain import (
    file_exists_on_chain
)


def get_encrypted_image(file_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT encrypted_data
        FROM images
        WHERE file_id = ?
        """,
        (file_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


def is_authorized_owner(
    file_id,
    owner_id
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM file_owners
        WHERE file_id = ?
        AND owner_id = ?
        """,
        (
            file_id,
            owner_id
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row is not None


def retrieve_and_verify(
    file_id,
    owner_id
):

    if not is_authorized_owner(
        file_id,
        owner_id
    ):

        return (
            False,
            "Access Denied: User is not an authorized owner",
            None
        )

    if not file_exists_on_chain(
        file_id
    ):

        return (
            False,
            "Tampering Detected: file hash not found on blockchain",
            None
        )

    encrypted_data = get_encrypted_image(
        file_id
    )

    if encrypted_data is None:

        return (
            False,
            "File not found in CSP database",
            None
        )

    aes_key = get_file_key(
        file_id
    )

    if aes_key is None:

        return (
            False,
            "AES key not found",
            None
        )

    try:

        decrypted_bytes = decrypt_image(
            encrypted_data,
            aes_key
        )

    except Exception as e:

        return (
            False,
            f"Decryption failed: {e}",
            None
        )

    regenerated_hash = hashlib.sha256(
        decrypted_bytes
    ).hexdigest()

    if regenerated_hash != file_id:

        return (
            False,
            "Tampering Detected: hash mismatch",
            None
        )

    return (
        True,
        "Integrity Verified: Retrieved file matches stored hash",
        decrypted_bytes
    )