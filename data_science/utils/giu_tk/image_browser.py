# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

from pathlib import Path

from license_plate_recornizer import get_license_plate_vehicle

current_image_number = 0

button_forward = None
button_back = None

def add_result_detection(contures_img , detected_caracters: list, predict_caracters: list, predict_license_plate: str):

    for widget in frame_data.winfo_children():
        widget.destroy()

    detect_license_plate = Label(frame_data, text=predict_license_plate)
    detect_license_plate.grid(row=0, column=0)

    image_contures_img = Image.fromarray(contures_img)
    # image_c.show()
    new_label = Label(frame_data, image=ImageTk.PhotoImage(image_contures_img))
    new_label.grid(row=1, column= 0)

    frame_detection = Frame(frame_data)
    frame_detection.grid(row=2, column=0, sticky=S)

    
    for idx, detected_caracter in enumerate(detected_caracters):        
        # image_c = Image.fromarray(detected_caracter)
        # image_c.show()

        new_label = Label(frame_detection, image=ImageTk.PhotoImage(Image.fromarray(detected_caracter)))
        new_label.grid(row=0, column= idx, sticky=S)

    for idx, predict_caracter in enumerate(predict_caracters):
        
        new_label = Label(frame_detection, text=predict_caracters[idx])
        new_label.grid(row=1, column= idx, sticky=S)


def update_image(img_no):
    # global label
    # global label2

    global current_image_number

    current_image_number = img_no

    if len(List_images) == 0:
        image = start_image
        license_plate_detected = start_image
    else:
        path_to_image = List_images[current_image_number]

        label_file_name.configure(text=path_to_image.name)

        image = ImageTk.PhotoImage(Image.open(str(path_to_image)))
        license_plate_detected, license_plate_img, detected_caracters, predict_caracters, predict_license_plate = (
            get_license_plate_vehicle(path_to_image)
        )
        if license_plate_detected is None:
            license_plate_detected = image
        else:
            license_plate_detected = ImageTk.PhotoImage(Image.fromarray(license_plate_detected))

        add_result_detection(license_plate_img, detected_caracters, predict_caracters, predict_license_plate)

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

    List_images = [file for file in path_to_images.glob("*.jpg")]


def select_folder():
    global path_source

    path = filedialog.askdirectory()

    if path != "":
        path_source.set(path)

        get_list_images()

        next_image(current_image_number)


root = Tk()
root.title("Image Viewer")
root.geometry("930x500")

path_source = StringVar(
    value=str(Path(__file__).parent)
)  # Path(__file__).parent  # / "image_for_detect_in parking_"

List_images = []

get_list_images()

label_folder = Label(root, text="Folder")
label_folder.grid(row=0, column=0, pady=5, sticky=E)

entry_folder = Entry(root, textvariable=str(path_source))
entry_folder.grid(row=0, column=1, columnspan=5, ipadx=200, pady=5, sticky=W)

label_file_name = Label(root, text="")
label_file_name.grid(row=1)


button_folder = Button(root, text="Browse", command=select_folder)
button_folder.grid(row=0, column=6, sticky=W)

start_image = ImageTk.PhotoImage(Image.new("RGB", (460, 350)))

label = Label(image=start_image)
label.grid(row=2, column=0, columnspan=3)
label2 = Label(image=start_image)
label2.grid(row=2, column=5, columnspan=3)

frame_data = Frame(root)
frame_data.grid(row=6, column=0)

button_back = Button(
    root,
    text="Back",
    command=lambda: next_image(current_image_number - 1),
    state=DISABLED,
)

button_exit = Button(root, text="Exit", command=root.quit)

button_forward = Button(
    root,
    text="Forward",
    command=lambda: next_image(current_image_number + 1),
    state=DISABLED,
)


button_back.grid(row=9, column=0, sticky=W)
# button_exit.grid(row=5, column=, sticky=E)
button_forward.grid(row=9, column=2, sticky=E)

next_image(current_image_number)

root.mainloop()
