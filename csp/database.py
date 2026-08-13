import sqlite3

DB_PATH = "storage/metadata/images.db"


def create_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        file_id TEXT PRIMARY KEY,
        phash TEXT,
        encrypted_data BLOB
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT,
        owner_id TEXT,
        role TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_keys (
        file_id TEXT PRIMARY KEY,
        aes_key BLOB
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_metadata (
        file_id TEXT PRIMARY KEY,
        image_name TEXT
    )
    """)
    conn.commit()
    conn.close()


def store_image(file_id, phash, encrypted_data):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO images
    (file_id, phash, encrypted_data)
    VALUES (?, ?, ?)
    """, (
        file_id,
        phash,
        encrypted_data
    ))

    conn.commit()
    conn.close()


def get_file_id_by_phash(phash):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_id
        FROM images
        WHERE phash = ?
        """,
        (phash,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def store_owner(file_id, owner_id, role):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO file_owners
    (file_id, owner_id, role)
    VALUES (?, ?, ?)
    """, (
        file_id,
        owner_id,
        role
    ))

    conn.commit()
    conn.close()


def owner_exists(file_id, owner_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
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


def store_file_key(file_id, aes_key):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO file_keys
    (file_id, aes_key)
    VALUES (?, ?)
    """, (
        file_id,
        aes_key
    ))

    conn.commit()
    conn.close()


def get_file_key(file_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT aes_key
    FROM file_keys
    WHERE file_id = ?
    """, (file_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None
def store_image_metadata(
    file_id,
    image_name
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO image_metadata
    (file_id, image_name)
    VALUES (?, ?)
    """, (
        file_id,
        image_name
    ))

    conn.commit()
    conn.close()
def get_user_images(
    owner_id
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        m.file_id,
        m.image_name
    FROM image_metadata m
    JOIN file_owners o
        ON m.file_id = o.file_id
    WHERE o.owner_id = ?
    """, (
        owner_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_file_id_by_name(
    image_name
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT file_id
    FROM image_metadata
    WHERE image_name = ?
    """, (
        image_name,
    ))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None