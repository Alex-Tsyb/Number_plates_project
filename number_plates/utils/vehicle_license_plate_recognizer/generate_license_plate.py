import random

# from PIL import Image, ImageDraw, ImageFont

FIRST_LETTER = [
    "DI",
    "PD",
    "ED",
    "DC",
    "AK",
    "KK",
    "AB",
    "KB",
    "AC",
    "KC",
    "AE",
    "KE",
    "AН",
    "KН",
    "AM",
    "KM",
    "AO",
    "KO",
    "AР",
    "KР",
    "AT",
    "KT",
    "AA",
    "KA",
    "AI",
    "KI",
    "ВA",
    "НA",
    "ВВ",
    "НВ",
    "ВС",
    "НС",
    "ВE",
    "НE",
    "ВН",
    "НН",
    "ВI",
    "НI",
    "ВК",
    "НK",
    "СН",
    "IН",
    "ВМ",
    "НM",
    "ВO",
    "НO",
    "AH",
    "KH",
    "ВТ",
    "НT",
    "ВH",
    "НH",
    "СA",
    "IA",
    "СВ",
    "IВ",
    "СE",
    "IE",
]
NUMBERS = "0123456789"
LAST_LETTER = "ABCEHIKMOPTX"


def generate_random_license_plate_vehicle():
    random_first_letters = random.choice(FIRST_LETTER)
    random_numbers = "".join(random.choice(NUMBERS) for _ in range(4))
    random_last_letters = "".join(random.choice(LAST_LETTER) for _ in range(2))

    return " ".join([random_first_letters, random_numbers, random_last_letters])


# def get_image_random_vehicle_license_plate():

#     result = generate_random_license_plate_vehicle()

#     # Load the image
#     img = Image.open("license_plate_ua.png")
#     img_width, img_height = img.size

#     # Create a drawing object
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype("arial.ttf", 70)  # Установка жирного шрифта

#     # Add text to the image
#     _, _, text_width, text_height = draw.textbbox((0, 0), text=result, font=font)
#     draw.text(
#         # ((img_width - text_width) / 2, (img_height - text_height) / 2 + 8),
#         ((img_width - text_width) / 2 + 8, (img_height - text_height) / 2),
#         result,
#         fill="black",
#         font=font,
#         stroke_width=1,
#     )

#     # Save or display the image
#     img.show(title="Номер")  # display image
