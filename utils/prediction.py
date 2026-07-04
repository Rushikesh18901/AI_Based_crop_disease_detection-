# Prediction utility (UPDATED - ROBUST VERSION)

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers
import numpy as np
import cv2
import json


# ==============================
# CREATE MODEL ARCHITECTURE
# ==============================
def create_model(num_classes):
    base_model = MobileNetV2(
        input_shape=(224, 224, 3), include_top=False, weights="imagenet"
    )

    # Freeze base layers (same as training phase 1)
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    return model


# ==============================
# LOAD LABEL MAPPING
# ==============================
with open("models/label_mapping.json", "r") as f:
    class_indices = json.load(f)

num_classes = len(class_indices)
print(f"✅ Number of classes: {num_classes}")

# Reverse mapping
class_names = {v: k for k, v in class_indices.items()}


# ==============================
# LOAD MODEL WEIGHTS
# ==============================
model = create_model(num_classes)

try:
    model.load_weights("models/crop_disease_model.h5")
    print("✅ Model weights loaded successfully!")
except Exception as e:
    print("❌ Error loading model:", e)
    raise


# ==============================
# PREPROCESS FUNCTION
# ==============================
def preprocess_image(image):
    if image is None or image.size == 0:
        raise ValueError("Invalid image data")

    # Ensure 3 channels (RGB)
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Resize and normalize
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


# ==============================
# QUALITY CHECK FUNCTION
# ==============================
def is_image_valid(image):
    if image is None or image.size == 0:
        return False, "Empty image"

    # Calculate mean from only valid channels
    if len(image.shape) == 3:
        mean_val = image[:, :, :3].mean()
    else:
        mean_val = image.mean()

    if mean_val < 30:
        return False, "Image too dark"

    if mean_val > 220:
        return False, "Image too bright"

    return True, ""


# ==============================
# MAIN PREDICTION FUNCTION
# ==============================
def predict_disease(image):
    # 1️⃣ Image quality check
    valid, msg = is_image_valid(image)
    if not valid:
        return msg, 0.0

    # 2️⃣ Preprocess
    try:
        img = preprocess_image(image)
    except Exception as e:
        return f"Error preprocessing image: {str(e)}", 0.0

    # 3️⃣ Prediction
    try:
        prediction = model.predict(img, verbose=0)
        prediction = prediction[0]
    except Exception as e:
        return f"Error during prediction: {str(e)}", 0.0

    class_index = int(np.argmax(prediction))
    confidence = float(prediction[class_index])

    disease = class_names[class_index]

    # 4️⃣ Confidence check
    if confidence < 0.75:
        return "Uncertain - Upload clearer image", confidence

    return disease, confidence
