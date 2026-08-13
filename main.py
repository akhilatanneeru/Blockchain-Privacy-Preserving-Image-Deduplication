from client.upload import upload_image
from client.preprocess import generate_file_id
from client.crypto import (
    encrypt_image,
    generate_aes_key
)
from csp.database import (
    store_image_metadata,
    get_user_images
)
from csp.database import (
    store_image,
    store_owner,
    create_table,
    get_file_id_by_phash,
    store_file_key,
    owner_exists
    
)

from csp.dedup import check_duplicate

from blockchain.eth_chain import (
    record_file_on_chain,
    file_exists_on_chain
)

from csp.ownership import (
    create_ownership_challenge,
    generate_ownership_proof,
    verify_ownership_proof
)

from blockchain.blockchain import (
    create_block,
    get_previous_hash
)

image_path = "sample 25 (1).png"
uploader_id = "demo_user_5"

create_table()

image_bytes, phash = upload_image(
    image_path
)

file_id = generate_file_id(
    image_bytes
)



status, matched_phash = check_duplicate(
    phash
)

print(
    "Deduplication Status:",
    status
)
print(
    "File ID (SHA-256):",
    file_id
)

# --------------------------------------------------
# EXACT DUPLICATE
# --------------------------------------------------

if status == "EXACT_DUPLICATE":

    print(
        "Duplicate image found. Starting ownership verification..."
    )

    challenge = create_ownership_challenge()

    proof = generate_ownership_proof(
        file_id,
        challenge
    )

    if verify_ownership_proof(
        file_id,
        challenge,
        proof
    ):

        original_file_id = get_file_id_by_phash(
            matched_phash
        )

        if owner_exists(
            original_file_id,
            uploader_id
        ):

            print(
                "User already owns this image"
            )

        else:

            store_owner(
                original_file_id,
                uploader_id,
                "subsequent_uploader"
            )

            print(
                "Owner record updated in CSP"
            )

    else:

        print(
            "Ownership verification failed. Upload rejected."
        )

# --------------------------------------------------
# NEAR DUPLICATE
# --------------------------------------------------

elif status == "NEAR_DUPLICATE":

    print(
        "Near duplicate detected."
    )

    original_file_id = get_file_id_by_phash(
        matched_phash
    )

    if original_file_id:

        if owner_exists(
            original_file_id,
            uploader_id
        ):

            print(
                "User already owns this image"
            )

        else:

            store_owner(
                original_file_id,
                uploader_id,
                "subsequent_uploader"
            )

            print(
                "Near duplicate mapped to existing image"
            )

            print(
                "Owner record updated in CSP"
            )

    else:

        print(
            "Original image not found. Treating as new upload."
        )

        aes_key = generate_aes_key()

        encrypted_data = encrypt_image(
            image_bytes,
            aes_key
        )

        store_file_key(
            file_id,
            aes_key
        )

        store_image(
            file_id,
            phash,
            encrypted_data
        )
        store_image_metadata(
            file_id,
            image_path
        )
        store_owner(
            file_id,
            uploader_id,
            "initial_uploader"
        )

        previous_hash = get_previous_hash()

        block = create_block(
            file_id,
            previous_hash
        )

        chain_tx = record_file_on_chain(
            file_id
        )

        print(
            "Encrypted image stored successfully"
        )

        print(
            "Owner record updated in CSP"
        )

        

        print(
            "File recorded on Ethereum chain:",
            chain_tx
        )

# --------------------------------------------------
# NEW IMAGE
# --------------------------------------------------

else:

    print(
        "New image detected"
    )

    aes_key = generate_aes_key()

    encrypted_data = encrypt_image(
        image_bytes,
        aes_key
    )

    store_file_key(
        file_id,
        aes_key
    )

    store_image(
        file_id,
        phash,
        encrypted_data
    )
    store_image_metadata(
        file_id,
        image_path
    )

    store_owner(
        file_id,
        uploader_id,
        "initial_uploader"
    )

    previous_hash = get_previous_hash()

    block = create_block(
        file_id,
        previous_hash
    )

    chain_tx = record_file_on_chain(
        file_id
    )

    print(
        "Encrypted image stored successfully"
    )

    print(
        "Owner record updated in CSP"
    )

    

    print(
        "File recorded on Ethereum chain:",
        chain_tx
    )

    

