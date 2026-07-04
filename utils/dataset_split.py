# Dataset splitting utility
import os
import shutil
import random
from PIL import Image

# ==========================
# 📌 CONFIGURATION
# ==========================
SOURCE_DIR = "dataset/rawdata"
TRAIN_DIR = "dataset/train"
VAL_DIR = "dataset/validation"
TEST_DIR = "dataset/test"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

IMG_EXTENSIONS = (".jpg", ".jpeg")
TARGET_FORMAT = ".jpg"


# ==========================
# 📂 CONVERT PNG TO JPG
# ==========================
def convert_png_to_jpg(source_dir):
    converted_count = 0
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if not os.path.isdir(class_path):
            continue
        for file in os.listdir(class_path):
            if file.lower().endswith(".png"):
                old_path = os.path.join(class_path, file)
                new_name = file[:-4] + TARGET_FORMAT
                new_path = os.path.join(class_path, new_name)
                try:
                    with Image.open(old_path) as img:
                        if img.mode == "RGBA":
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[3])
                            img = background
                        elif img.mode != "RGB":
                            img = img.convert("RGB")
                    img.save(new_path, "JPEG", quality=95)
                    os.remove(old_path)
                    converted_count += 1
                except Exception as e:
                    print(f"[ERR] Convert failed: {file} - {e}")
    return converted_count


# ==========================


# ==========================
# 📂 GET IMAGE FILES
# ==========================
def get_image_files(class_path):
    return [
        file for file in os.listdir(class_path) if file.lower().endswith(IMG_EXTENSIONS)
    ]


# ==========================
# 📂 CLEAR AND CREATE DIRS
# ==========================
def clear_and_create_dirs(force_clear=False):
    if not force_clear:
        has_content = False
        for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
            if os.path.exists(dir_path) and os.listdir(dir_path):
                has_content = True
                break
        if has_content:
            print("[DIR] Using existing directories (skipping clear)")
            for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
                os.makedirs(dir_path, exist_ok=True)
            return

    for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if os.path.exists(dir_path):
            try:
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for name in files:
                        file_path = os.path.join(root, name)
                        try:
                            os.chmod(file_path, 0o777)
                            os.remove(file_path)
                        except:
                            pass
                    for name in dirs:
                        dir_path_to_remove = os.path.join(root, name)
                        try:
                            os.chmod(dir_path_to_remove, 0o777)
                            os.rmdir(dir_path_to_remove)
                        except:
                            pass
                os.chmod(dir_path, 0o777)
                os.rmdir(dir_path)
            except:
                pass
        os.makedirs(dir_path, exist_ok=True)
    print("[DIR] directories created/cleared")


# ==========================
# 📊 SPLIT DATA
# ==========================
def split_dataset():
    print("[INFO] Converting PNG images to JPG...")
    converted = convert_png_to_jpg(SOURCE_DIR)
    print(f"[OK] Converted {converted} PNG images to JPG")

    clear_and_create_dirs(force_clear=False)

    total_classes = 0
    total_images = 0

    for class_name in os.listdir(SOURCE_DIR):
        class_path = os.path.join(SOURCE_DIR, class_name)

        if not os.path.isdir(class_path):
            continue

        images = get_image_files(class_path)

        if len(images) == 0:
            print(f"[WARN] Skipping {class_name} (no images found)")
            continue

        random.shuffle(images)

        total = len(images)

        train_split = int(TRAIN_RATIO * total)
        val_split = int(VAL_RATIO * total)

        train_images = images[:train_split]
        val_images = images[train_split : train_split + val_split]
        test_images = images[train_split + val_split :]

        # Create class folders
        os.makedirs(os.path.join(TRAIN_DIR, class_name), exist_ok=True)
        os.makedirs(os.path.join(VAL_DIR, class_name), exist_ok=True)
        os.makedirs(os.path.join(TEST_DIR, class_name), exist_ok=True)

        # Copy images
        for img in train_images:
            shutil.copy(
                os.path.join(class_path, img), os.path.join(TRAIN_DIR, class_name, img)
            )

        for img in val_images:
            shutil.copy(
                os.path.join(class_path, img), os.path.join(VAL_DIR, class_name, img)
            )

        for img in test_images:
            shutil.copy(
                os.path.join(class_path, img), os.path.join(TEST_DIR, class_name, img)
            )

        print(f"[OK] {class_name} -> {total} images split")

        total_classes += 1
        total_images += total

    print("\n==============================")
    print(f"[STAT] Total Classes: {total_classes}")
    print(f"[IMG] Total Images: {total_images}")
    print("[DONE] Dataset split completed!")
    print("==============================")


# ==========================
# ▶ MAIN
# ==========================
if __name__ == "__main__":
    split_dataset()
