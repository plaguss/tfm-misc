"""AWS lambda to get the predictions of a crossfit movement clip.
"""

import base64
import json
import tempfile
import zipfile
from pathlib import Path
from typing import *
import os

import numpy as np
import requests
import s3fs
import tensorflow as tf
import tensorflow_hub as hub
import cv2


S3_BUCKET = os.environ.get("S3_BUCKET")
print(f"S3_BUCKET: {S3_BUCKET}")
MODEL_NAME = os.environ.get("MODEL_NAME")

RESOLUTION_MOVINET_A2_BASE = (224, 224)


def labels_from_gist() -> List[str]:
    url = r"https://gist.github.com/plaguss/58091caefee6acb39ae51cbc241b3cf9/raw/labels.txt"
    resp = requests.get(url=url)
    if resp.status_code == 200:
        return resp.content.decode("utf-8").splitlines()
    print("Couldn't load the labels from gist.")


def load_model(
    path_to_model: Union[str, Path]
) -> "tf.keras.engine.functional.Functional":
    if isinstance(path_to_model, Path):
        path_to_model = str(path_to_model)

    keras_layer = hub.KerasLayer(path_to_model)

    inputs = tf.keras.layers.Input(shape=[None, None, None, 3], dtype=tf.float32)
    inputs = dict(image=inputs)
    outputs = keras_layer(inputs)

    model = tf.keras.Model(inputs, outputs)
    model.build([1, 1, 1, 1, 3])

    return model


labels = labels_from_gist()


def get_model_from_s3(model_name: str):
    def is_aws_env():
        # Copy from:
        # https://unbiased-coder.com/detect-aws-env-python-nodejs/
        return os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or os.environ.get('AWS_EXECUTION_ENV')

    with tempfile.TemporaryDirectory() as tempdir:
        # FIXME: Running the container locally detects the ENV vars and doesn't work
        # if is_aws_env():  # Whe shouldn't need the credentials to the s3 bucket from aws.
        fs = s3fs.S3FileSystem()
        # else:
        # fs = s3fs.S3FileSystem(
        #     key=os.environ.get("AWS_ACCESS_KEY"),
        #     secret=os.environ.get("AWS_SECRET_KEY"),
        #     token=os.environ.get("AWS_TOKEN_KEY")
        # )
        # Fetch and save the zip file to the temporary directory
        print(f"Trying to obtain the model: {f'{S3_BUCKET}/{model_name}.zip'}")
        fs.get(f"{S3_BUCKET}/{model_name}.zip", f"{tempdir}/{model_name}.zip")

        # Extract the model zip file within the temporary directory
        with zipfile.ZipFile(f"{tempdir}/{model_name}.zip", "r") as zip_ref:
            zip_ref.extractall(f"{tempdir}")

        return load_model(f"{tempdir}/{model_name}")


model = get_model_from_s3(MODEL_NAME)


def get_top_k(probs, k=5, label_map=labels):
    """Outputs the top k model labels and probabilities on the given video."""
    # If a video is sent as a batch, remove that dimension.
    if probs.ndim == 2:
        probs = probs[0]

    top_predictions = tf.argsort(probs, axis=-1, direction="DESCENDING")[:k]
    top_labels = tf.gather(label_map, top_predictions, axis=-1)
    top_labels = [label.decode("utf8") for label in top_labels.numpy()]
    top_probs = tf.gather(probs, top_predictions, axis=-1).numpy()
    return tuple(zip(top_labels, top_probs))


def predict_top_k(model, video, k=5, label_map=labels):
    """Outputs the top k model labels and probabilities on the given video."""
    outputs = model.predict(video[tf.newaxis])[0]
    probs = tf.nn.softmax(outputs)
    return get_top_k(probs, k=k, label_map=label_map)


class NumpyFloatEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.float32):
            if o % 1 == 0:
                return int(o)
            else:
                return round(float(o), 12)
        return super().default(o)


def jsonify(obj, statusCode=200):
    return {
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "statusCode": statusCode,
        "body": json.dumps(obj, cls=NumpyFloatEncoder),
    }


# def parse_video_from_bytes(video_encoded: bytes) -> tf.Tensor:
#     # FIXME: Can't make this to work inside an AWS Linux docker image,
#     # it seems an error quen loading .so files from tensorflow-io.
#     return tfio.experimental.ffmpeg.decode_video(base64.b64decode(video_encoded))


def load_video(path: str, max_frames: int = 0, resize: Tuple[int, int] = (224, 224), scaling_factor: float = 255.) -> tf.Tensor:
    """Loads a video in a format ready to be used by the model to be predicted.

    Args:
        path (str): Path to the video.
        max_frames (int): Defaults to 0.
        resize Tuple[int, int]: The second parameter.
        scaling_factor (float): Value to scale the pixels of the video. Defaults to 255.

    Returns:
        tensorflow.python.framework.ops.EagerTensor: tensor video.
    """
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()

    return tf.image.resize(tf.cast(np.array(frames), tf.float32), resize) / scaling_factor


def read_video_encoded(video_encoded: bytes, resolution: Tuple[int, int] = (224, 224)):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(f'{tempdir}/parsed_clip.mp4', 'wb') as f:
            f.write(base64.b64decode(video_encoded))
        video = load_video(f'{tempdir}/parsed_clip.mp4', resize=resolution, scaling_factor=225.)
    return video


def handler(event, context):
    try:
        video = event["video"]
        # Version using tensorflow-io
#        video = parse_video_from_bytes(video)
        # video = tf.image.resize(video, RESOLUTION_MOVINET_A2_BASE)
        video = read_video_encoded(video, resolution=RESOLUTION_MOVINET_A2_BASE)
        # resize_video to have the expected size for the trained model

        prediction = predict_top_k(model, video, label_map=tf.constant(labels))
        
    except Exception as exc:
        print("Couldn't get the prediction from the video. Returning default prediction.")
        print(f"exception: {exc}")
        prediction = ((("ERROR", -1.),) * 5)

    return jsonify({"prediction": prediction})
