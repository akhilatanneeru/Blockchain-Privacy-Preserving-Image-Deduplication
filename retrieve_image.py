from csp.retrieval import retrieve_and_verify

from csp.database import (
    get_user_images
)

uploader_id = input(
    "Enter User ID: "
)

print("\n----- RETRIEVAL TEST -----")

images = get_user_images(
    uploader_id
)

if not images:

    print(
        "No images found for this user."
    )

else:

    print(
        "\nAvailable Images:\n"
    )

    for i, image in enumerate(
        images,
        start=1
    ):

        print(
            f"{i}. {image[1]}"
        )

    choice = int(
        input(
            "\nChoose Image: "
        )
    )

    target_file_id = images[
        choice - 1
    ][0]

    image_name = images[
        choice - 1
    ][1]

    success, message, image_bytes = retrieve_and_verify(
        target_file_id,
        uploader_id
    )

    print(message)

    if success:

        output_file = (
            r"C:\Users\Hp\Downloads\\"
            + image_name
        )

        with open(
            output_file,
            "wb"
        ) as f:

            f.write(
                image_bytes
            )

        print(
            f"Image downloaded successfully: {output_file}"
        )
