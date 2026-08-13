import sqlite3
import imagehash

from csp.database import DB_PATH

HAMMING_THRESHOLD = 5


def check_duplicate(phash):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT phash FROM images")
    rows = cursor.fetchall()

    new_hash = imagehash.hex_to_hash(phash)

    best_distance = float("inf")
    best_phash = None

    for row in rows:

        existing_hash = imagehash.hex_to_hash(row[0])

        distance = new_hash - existing_hash

        if distance < best_distance:
            best_distance = distance
            best_phash = row[0]

    conn.close()

    print(f"Best Hamming Distance: {best_distance}")

    if best_distance == 0:
        return "EXACT_DUPLICATE", best_phash

    elif best_distance <= HAMMING_THRESHOLD:
        return "NEAR_DUPLICATE", best_phash

    return "NEW_IMAGE", None