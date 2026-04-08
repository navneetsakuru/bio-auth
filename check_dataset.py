import os
from PIL import Image

BASE_DIR = "data"
FINGER_DIR = os.path.join(BASE_DIR, "fingerprint")
IRIS_DIR = os.path.join(BASE_DIR, "iris")

def check_images(modality_dir, modality_name):
    print(f"\nChecking {modality_name} dataset...")
    persons = sorted(os.listdir(modality_dir))

    if len(persons) == 0:
        print("❌ No persons found!")
        return

    for person in persons:
        person_path = os.path.join(modality_dir, person)
        if not os.path.isdir(person_path):
            continue

        images = os.listdir(person_path)
        print(f"\n{modality_name} -> {person}: {len(images)} images")

        for img_name in images:
            img_path = os.path.join(person_path, img_name)
            try:
                img = Image.open(img_path)
                img.verify()  # check corruption
                print(f"  ✅ {img_name}")
            except Exception as e:
                print(f"  ❌ {img_name} : {e}")

check_images(FINGER_DIR, "Fingerprint")
check_images(IRIS_DIR, "Iris")

print("\nDataset check completed.")
