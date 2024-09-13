# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from tkinter import filedialog

import cv2
from PIL import ImageTk, Image, ImageOps

from pathlib import Path

from license_plate_recornizer import get_license_plate_vehicle

current_image_number = 0

button_forward = None
button_back = None

WIDTH_IMAGE_UI = 460
HEIGTH_IMAGE_UI = 350

def resize_image(image: Image, new_width : int = None,  new_height: int = None):
    
    if not new_width is None:
        pixels_x, pixels_y = tuple([int(new_width/image.size[0] * x)  for x in image.size])
    else:
        pixels_x, pixels_y = tuple([int(new_height/image.size[1] * x)  for x in image.size])

    return image.resize((pixels_x, pixels_y))

def add_result_detection(
    contures_img,
    detected_caracters: list,
    predict_caracters: list,
    predict_license_plate: str,
):

    for widget in frame_data.winfo_children():
        widget.destroy()

    detect_license_plate = Label(frame_data, text=predict_license_plate)
    detect_license_plate.grid(row=0, sticky=EW)

    if not contures_img is None:
        image_contures_img = resize_image(Image.fromarray(contures_img), 333)
    else:
        image_contures_img = Image.new("RGB", (333, 75))

    image_contures_img = ImageTk.PhotoImage(image_contures_img)

    new_label = Label(
        frame_data,
        image=image_contures_img,
        padx=10,
        bd=2,
        relief="solid",
        bg="red"
    )
    new_label.grid(row=1, column=0)

    new_label.image = image_contures_img

    frame_detection = Frame(frame_data)
    frame_detection.grid(row=1, column=1, padx=5, sticky=EW)

    for idx, detected_caracter in enumerate(detected_caracters):
        image_c = ImageTk.PhotoImage(Image.fromarray(detected_caracter))

        new_label = Label(
            frame_detection,
            image=image_c,
            bd=2,
            relief="solid",
        )
        new_label.grid(
            row=0,
            column=idx,
            sticky=S,
            padx=10
        )

        new_label.image = image_c



    for idx, predict_caracter in enumerate(predict_caracters):

        new_label = Label(frame_detection, text=predict_caracter)
        new_label.grid(row=1, column=idx, sticky=S)


def update_image(img_no):
    # global label
    # global label2

    global current_image_number

    current_image_number = img_no

    if len(List_images) == 0:
        image = start_image
        license_plate_detected = start_image
        current_file_name.set("")
    else:
        path_to_image = List_images[current_image_number]

        current_file_name.set(path_to_image.name)

        image = ImageTk.PhotoImage(resize_image(Image.open(str(path_to_image)), new_height=HEIGTH_IMAGE_UI)) 

        (
            license_plate_detected,
            license_plate_img,
            detected_caracters,
            predict_caracters,
            predict_license_plate,
        ) = get_license_plate_vehicle(path_to_image)
        if license_plate_detected is None:
            license_plate_detected = image
        else:
            license_plate_detected = ImageTk.PhotoImage(
                resize_image(Image.fromarray(license_plate_detected, mode="RGB"), new_height=HEIGTH_IMAGE_UI)
            )

        add_result_detection(
            license_plate_img,
            detected_caracters,
            predict_caracters,
            predict_license_plate,
        )

    label.configure(image=image)
    label2.configure(image=license_plate_detected)

    label.image = image
    label2.image = license_plate_detected


def next_image(img_no):
    global button_forward
    global button_back

    update_image(img_no)

    def update_state_button(button: Button, state):
        if button is None:
            return
        if button["state"] == state:
            return
        button.configure(state=state)

    update_state_button(
        button_forward,
        (
            DISABLED
            if (img_no == len(List_images) - 1 or len(List_images) == 0)
            else NORMAL
        ),
    )
    update_state_button(button_back, DISABLED if img_no == 0 else NORMAL)


def get_list_images():
    global path_source
    global List_images
    global current_image_number

    current_image_number = 0

    path_to_images = Path(path_source.get())

    ext_list = ["*.jpg", "*.jpeg", "*.png"]
    List_images = []

    _ = [
        List_images.extend([file for file in path_to_images.glob(ext)])
        for ext in ext_list
    ]


def select_folder():
    global path_source

    path = filedialog.askdirectory()

    if path != "":
        path_source.set(path)

        get_list_images()

        next_image(current_image_number)


root = Tk()
root.title("Licence Plate Viewer")
root.geometry("930x515")

path_source = StringVar(
    value=str(Path(__file__).parent)
)

start_image = ImageTk.PhotoImage(Image.new("RGB", (WIDTH_IMAGE_UI, HEIGTH_IMAGE_UI)))

current_file_name = StringVar()

List_images = []

get_list_images()

frame_file = Frame(root, relief="solid")
frame_file.grid(row=0, sticky=EW)

label_folder = Label(frame_file, text="Folder")
label_folder.grid(row=0, column=0, pady=5, padx=5, sticky=E)

entry_folder = Entry(frame_file, textvariable=path_source)
entry_folder.grid(row=0, column=1, columnspan=1, ipadx=200, pady=5, sticky=W)

button_folder = Button(frame_file, text="Browse", command=select_folder)
button_folder.grid(row=0, column=2, sticky=W)

label_file_name = Label(frame_file, text="File name")
label_file_name.grid(row=0, column=3, sticky=W)
entry_file_name = Entry(frame_file, textvariable=current_file_name)
entry_file_name.grid(row=0, column=4, sticky=W)


frame_image = Frame(root, relief="solid")
frame_image.grid(row=1, sticky=EW)

label = Label(frame_image, image=start_image)
label.grid(row=0, column=0, columnspan=3)
label2 = Label(frame_image, image=start_image)
label2.grid(row=0, column=5, columnspan=3)

frame_data = Frame(root, bd=1, relief="solid", height=102)
frame_data.grid(row=3, sticky=EW)

frame_control = Frame(root, relief="solid")
frame_control.grid(row=4, sticky=EW, ipady=20)

button_back = Button(
    frame_control,
    text="Back",
    command=lambda: next_image(current_image_number - 1),
    state=DISABLED,
)
button_back.grid(row=0, column=0, padx=5, sticky=W)

button_exit = Button(frame_control, text="Exit", command=root.quit)

label_space = Label(frame_control)
label_space.grid(row=0, column=1, ipadx=408, sticky=EW)

button_forward = Button(
    frame_control,
    text="Forward",
    command=lambda: next_image(current_image_number + 1),
    state=DISABLED,
)
button_forward.grid(row=0, column=2, padx=5, sticky=E)

root.bind("<Left>", lambda event: next_image(current_image_number - 1))
root.bind("<Right>", lambda event: next_image(current_image_number + 1))

# button_exit.grid(row=5, column=, sticky=E)

next_image(current_image_number)

root.mainloop()
