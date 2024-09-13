import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from pathlib import Path
import numpy as np
import keras_cv
import keras
import tensorflow as tf
from PIL import Image, UnidentifiedImageError


model_path = Path(__file__).parent.joinpath("model")

prediction_decoder = keras_cv.layers.NonMaxSuppression(
    bounding_box_format="xyxy",
    from_logits=True,
    max_detections=1
)
model_plate_position = keras.models.load_model(
    model_path.joinpath('plate_recogn_based_on_yolo_xs.keras'),
    compile=False
)
model_plate_position.prediction_decoder = prediction_decoder

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
    return img_resized.crop(
        (
            img_resized.width * bbox[1],
            img_resized.height * bbox[0],
            img_resized.width * bbox[3],
            img_resized.height * bbox[2]
        )
    )


def recognize_plate(
        img: Image,
        model: keras.models = model_plate_position
) -> tuple:

    # make image preprocessing before model input
    imgs = [np.array(img)]
    imgs = keras_cv.layers.Resizing(
        640,
        640,
        pad_to_aspect_ratio=True
    ).call(imgs)

    # make prediction
    y_pred = model.predict((imgs), verbose=0)

    y_pred = keras_cv.bounding_box.convert_format(
        y_pred,
        images=imgs,
        source="xyxy",
        target="rel_yxyx",
    )
    img_with_box = tf.image.draw_bounding_boxes(
        imgs, y_pred["boxes"],
        np.array([[255, 255, 0]])
    )
    img_with_box = Image.fromarray(
            img_with_box[0].numpy().astype(dtype="uint8")
        )
    return (
        img_with_box,
        crop_plate(img, y_pred["boxes"][0][0].numpy().tolist())
    )


def recognize(img: Image) -> tuple:
    img_with_box, plate = recognize_plate(img)
    if plate is None:
        return img_with_box, None, None
    plate_text = recognize_chars(plate)
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
