from django.conf import settings

from utils import get_license_plate_vehicle


def save_result_image(img, filename):

    path_to_current_image = settings.MEDIA_ROOT.joinpath("cars/recognize/" + filename)

    img.save(path_to_current_image)

    return filename


def handle_uploaded_file(file, filename):

    path_to_current_image = settings.MEDIA_ROOT.joinpath(
        "cars/images_for_recognize/" + filename
    )

    with open(path_to_current_image, "wb+") as destination:
        destination.write(file.read())

    return path_to_current_image


def predict_license_plate(file, filename):

    file_path = handle_uploaded_file(file, filename)

    detected_license_plate_img, plate_img, plate_text = get_license_plate_vehicle(
        file_path
    )

    file_name, extension = file_path.stem, file_path.suffix

    result = (
        save_result_image(
            detected_license_plate_img, f"{file_name}_detected{extension}"
        ),
        save_result_image(plate_img, f"{file_name}_plate{extension}"),
        plate_text,
    )

    return result
