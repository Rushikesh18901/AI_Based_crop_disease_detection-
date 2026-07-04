# ==============================
# MODEL TRAINING SCRIPT (UPDATED)
# ==============================

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import json
import os

# ==============================
# PATHS
# ==============================
train_dir = "dataset/train"
val_dir = "dataset/validation"

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10   # Phase 1

# ==============================
# DATA AUGMENTATION (IMPROVED)
# ==============================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.6, 1.4]
)

val_datagen = ImageDataGenerator(rescale=1./255)

# ==============================
# LOAD DATA
# ==============================
train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_data = val_datagen.flow_from_directory(
    val_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# ==============================
# SAVE LABEL MAPPING
# ==============================
os.makedirs("models", exist_ok=True)

class_indices = train_data.class_indices

with open("models/label_mapping.json", "w") as f:
    json.dump(class_indices, f)

print("✅ Label mapping saved")

# ==============================
# BUILD MODEL (MobileNetV2)
# ==============================
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze base model (Phase 1)
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

outputs = layers.Dense(train_data.num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=outputs)

# ==============================
# COMPILE MODEL
# ==============================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==============================
# CALLBACKS (VERY IMPORTANT 🔥)
# ==============================
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=2,
    min_lr=1e-6
)

# ==============================
# TRAIN PHASE 1
# ==============================
print("🚀 Training Phase 1 (Frozen base model)...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr]
)

# ==============================
# FINE-TUNING PHASE 🔥
# ==============================
print("🔥 Fine-tuning started...")

# Unfreeze top layers
for layer in base_model.layers[-50:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=15,
    callbacks=[early_stop, reduce_lr]
)

# ==============================
# SAVE MODEL
# ==============================
model.save("models/crop_disease_model.h5")

print("✅ Model + labels saved successfully!")