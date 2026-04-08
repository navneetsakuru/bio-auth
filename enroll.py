import os
import numpy as np
from feature_extractor import extract_features

DATA_DIR = "../data"
TEMPLATE_DIR = "../templates"

os.makedirs(TEMPLATE_DIR, exist_ok=True)

def enroll_person(person_id):
    print(f"\nEnrolling {person_id}...")

    fp_dir = os.path.join(DATA_DIR, "fingerprint", person_id.strip())
    iris_dir = os.path.join(DATA_DIR, "iris", person_id.strip())

    fp_embeddings = []
    iris_embeddings = []

    for img in os.listdir(fp_dir):
        img_path = os.path.join(fp_dir, img)
        emb = extract_features(img_path)
        fp_embeddings.append(emb)

    for img in os.listdir(iris_dir):
        img_path = os.path.join(iris_dir, img)
        emb = extract_features(img_path)
        iris_embeddings.append(emb)

    person_template_dir = os.path.join(TEMPLATE_DIR, person_id)
    os.makedirs(person_template_dir, exist_ok=True)

    np.save(os.path.join(person_template_dir, "fingerprint.npy"), np.array(fp_embeddings))
    np.save(os.path.join(person_template_dir, "iris.npy"), np.array(iris_embeddings))

    print(f"Saved {len(fp_embeddings)} fingerprint & {len(iris_embeddings)} iris templates.")

def enroll_all():
    persons = [p.strip() for p in os.listdir(os.path.join(DATA_DIR, "fingerprint"))]

    for person in persons:
        enroll_person(person)

if __name__ == "__main__":
    enroll_all()
