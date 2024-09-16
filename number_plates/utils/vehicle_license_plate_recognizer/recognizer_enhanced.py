import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import re
from pathlib import Path
import numpy as np
import keras_cv
import keras
import tensorflow as tf
import cv2
from PIL import Image, UnidentifiedImageError
import pytesseract


# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


model_path = Path(__file__).parent.joinpath("model")

prediction_decoder_plate_position = keras_cv.layers.NonMaxSuppression(
    bounding_box_format="xyxy",
    from_logits=True,
    max_detections=1
)
model_plate_position = keras.models.load_model(
    model_path.joinpath('plate_recogn_based_on_yolo_xs.keras'),
    compile=False
)
model_plate_position.prediction_decoder = prediction_decoder_plate_position

prediction_decoder_symbols_positions = keras_cv.layers.NonMaxSuppression(
    bounding_box_format="xyxy",
    from_logits=True,
    # Decrease the required threshold to make predictions get pruned out
    # iou_threshold=0.2,
    # Tune confidence threshold for predictions to pass NMS
    confidence_threshold=0.65,
    max_detections=8
)
model_symbols_positions = keras.models.load_model(
    model_path.joinpath('smbls_position.keras'),
    compile=False
)
model_symbols_positions.prediction_decoder = prediction_decoder_symbols_positions


model_chars_recognition = keras.models.load_model(
    model_path.joinpath("smbls_recogn_based_on_captcha_method.keras"),
    compile=False
)

characters = [ch for ch in " -0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

char_to_num = keras.layers.StringLookup(
    vocabulary=list(characters), mask_token=None
)

num_to_char = keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)


def ctc_decode(y_pred, input_length, greedy=True, beam_width=100, top_paths=1):
    input_shape = keras.ops.shape(y_pred)
    num_samples, num_steps = input_shape[0], input_shape[1]
    y_pred = keras.ops.log(
        keras.ops.transpose(y_pred, axes=[1, 0, 2]) + keras.backend.epsilon()
    )
    input_length = keras.ops.cast(input_length, dtype="int32")

    if greedy:
        (decoded, log_prob) = tf.nn.ctc_greedy_decoder(
            inputs=y_pred, sequence_length=input_length
        )
    else:
        (decoded, log_prob) = tf.compat.v1.nn.ctc_beam_search_decoder(
            inputs=y_pred,
            sequence_length=input_length,
            beam_width=beam_width,
            top_paths=top_paths,
        )
    decoded_dense = []
    for st in decoded:
        st = tf.SparseTensor(st.indices, st.values, (num_samples, num_steps))
        decoded_dense.append(tf.sparse.to_dense(sp_input=st, default_value=-1))
    return (decoded_dense, log_prob)


# A utility function to decode the output of the network
def decode_batch_predictions(pred):
    max_length = 8
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text


def recognize_chars(
        img: Image,
        model: keras.models = model_chars_recognition
) -> str:

    img_width = 128
    img_height = 32

    # make image preprocessing before model input
    img = tf.convert_to_tensor(img)
    img = tf.image.rgb_to_grayscale(img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = keras.ops.image.resize(img, [img_height, img_width])
    img = keras.ops.transpose(img, axes=[1, 0, 2])
    img = tf.reshape(img, [1, 128, 32, 1])

    # make prediction
    preds = model.predict(img, verbose=0)
    preds = decode_batch_predictions(preds)[0]

    # if prediction contains [UNK] - recogintion failed, return None
    return None if preds.find("[UNK]") != -1 else preds


def crop_plate(img: Image, bbox: list) -> Image:
    size = max(img.width, img.height)
    img_resized = Image.new(mode="RGB", size=(size, size))
    img_resized.paste(img, (0, 0))
    # crop a little bit more
    x = 0.01
    return img_resized.crop(
        (
            img_resized.width * (bbox[1] - x),
            img_resized.height * (bbox[0] - x),
            img_resized.width * (bbox[3] + x),
            img_resized.height * (bbox[2] + x)
        )
    )


def recognize_symbols_with_tesseract(plate_clean: Image.Image) -> str:
    symbols = "0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    plate_text = pytesseract.image_to_string(plate_clean).upper()
    plate_text = re.sub(f"[^{symbols}]", "", plate_text)
    return plate_text


def split_to_chars(
        plate_image: Image.Image,
        model: keras.models = model_symbols_positions
) -> tuple[Image.Image, tuple[Image.Image]]:
    plate = np.array(plate_image)
    
    # make image preprocessing before model input
    resizer = keras.Sequential(
    layers=[
            # keras_cv.layers.Grayscale(output_channels=3),
            # keras_cv.layers.Equalization(value_range=[0,255]),
            keras_cv.layers.Resizing(
                256,
                256,
                pad_to_aspect_ratio=True,
                bounding_box_format="xyxy",
            )
        ]
    )
    plate = resizer([plate])

    # make prediction
    y_pred = model.predict((plate), verbose=0)

    plate_with_boxes = plate[0].numpy().astype("uint8")
    
    # extract symbols images
    symbols = {int(symbol[0]): symbol for symbol in y_pred["boxes"][0]}
    symbols_imgs = []
    plate_clean = Image.new(mode="RGB", size=(256, 256), color=(255, 255, 255))
    for symbol in sorted(symbols.items()):
        x_min = int(symbol[1][0])
        y_min = int(symbol[1][1]) - 3 # cut a little bit more - need further check
        x_max = int(symbol[1][2])
        y_max = int(symbol[1][3]) + 3 # cut a little bit more - need further check
        y_min = y_min if y_min >=0 else 0
        y_max = y_max if y_max <= plate[0].shape[0] else plate[0].shape[0]
        cv2.rectangle(plate_with_boxes,
            (x_min, y_min),
            (x_max, y_max),
            (255, 255, 0),
            2
        )
        symbol_img = Image.fromarray(
            plate[0][y_min:y_max, x_min:x_max].numpy().astype("uint8")
            )
        symbols_imgs.append(symbol_img)
        plate_clean.paste(symbol_img, (x_min, y_min))
    
    # crop plate_with_boxes to original aspect and convert to Image
    x_aspect = plate_image.width / max(plate_image.size)
    y_aspect = plate_image.height / max(plate_image.size)
    width = int(x_aspect * plate_with_boxes.shape[1])
    height = int(y_aspect * plate_with_boxes.shape[0])
    plate_with_boxes = Image.fromarray(
        plate_with_boxes[0:height, 0:width]
    )

    plate_clean = plate_clean.crop((0, 0, width, height))

    return plate_with_boxes, plate_clean, symbols_imgs


def recognize_plate(
        image: Image.Image,
        model: keras.models = model_plate_position
) -> tuple[Image.Image]:

    # make image preprocessing before model input
    img = np.array(image)
    img_with_box = img.copy()
    resizer = keras_cv.layers.Resizing(
        640,
        640,
        pad_to_aspect_ratio=True
    )
    img = resizer([img])

    # make prediction
    y_pred = model.predict((img), verbose=0)

    y_pred = keras_cv.bounding_box.convert_format(
        y_pred,
        images=img,
        source="xyxy",
        target="rel_yxyx",
    )

    # draw box on original image
    size = max(img_with_box.shape)
    box_xmin = int(y_pred["boxes"][0][0][1] * size)
    box_xmax = int(y_pred["boxes"][0][0][3] * size)
    box_ymin = int(y_pred["boxes"][0][0][0] * size)
    box_ymax = int(y_pred["boxes"][0][0][2] * size)
    cv2.rectangle(
        img_with_box,
        (box_xmin, box_ymin),
        (box_xmax, box_ymax),
        (255, 255, 0),
        3
    )
    
    img_with_box = Image.fromarray(img_with_box)
    plate = crop_plate(image, y_pred["boxes"][0][0].numpy().tolist())
    return img_with_box, plate


def recognize(img: Image, direct_recognition: bool = True) -> tuple:
    img_with_box, plate = recognize_plate(img)
    
    if direct_recognition:
        plate_text = recognize_chars(plate)
    else:
        plate_with_boxes, plate_clean, symbols_list = split_to_chars(plate)
        plate_text = recognize_symbols_with_tesseract(plate_clean)
        plate = plate_with_boxes
    return img_with_box, plate, plate_text


def get_license_plate_vehicle(image_path) -> str:
    path = Path(image_path)

    if not path.exists:
        return None

    try:
        image = Image.open(path)
    except UnidentifiedImageError:
        return None

    _, _, plate_text = recognize(image)
    return plate_text
