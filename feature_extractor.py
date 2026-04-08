import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load CNN once
model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3)
)

def preprocess_image(pil_img):
    if not isinstance(pil_img, Image.Image):
        raise ValueError("Input must be a PIL Image")

    pil_img = pil_img.convert("RGB")   # 🔥 FIX: force 3 channels
    img_array = np.array(pil_img)

    img_array = cv2.resize(img_array, (224, 224))
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array


def extract_features(pil_img):
    """
    Extracts normalized feature vector using CNN
    """
    processed = preprocess_image(pil_img)
    features = model.predict(processed, verbose=0)
    features = features.flatten()
    features = features / np.linalg.norm(features)
    return features
