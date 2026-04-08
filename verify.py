import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .feature_extractor import extract_features

TEMPLATE_DIR = "../templates"
THRESHOLD = 0.6

def best_similarity(query_emb, stored_embs):
    sims = cosine_similarity([query_emb], stored_embs)[0]
    return np.max(sims)

def verify(fingerprint_img, iris_img):
    q_fp = extract_features(fingerprint_img)
    q_ir = extract_features(iris_img)

    best_person = None
    best_score = 0.0

    for person in os.listdir(TEMPLATE_DIR):
        person_dir = os.path.join(TEMPLATE_DIR, person)

        if not os.path.isdir(person_dir):
            continue

        fp_path = os.path.join(person_dir, "fingerprint.npy")
        ir_path = os.path.join(person_dir, "iris.npy")

        if not os.path.exists(fp_path) or not os.path.exists(ir_path):
            continue

        fp_templates = np.load(fp_path)
        ir_templates = np.load(ir_path)

        fp_score = best_similarity(q_fp, fp_templates)
        ir_score = best_similarity(q_ir, ir_templates)

        fused_score = 0.5 * fp_score + 0.5 * ir_score

        print(f"{person}: FP={fp_score:.3f}, IR={ir_score:.3f}, FUSED={fused_score:.3f}")

        if fused_score > best_score:
            best_score = fused_score
            best_person = person

    if best_score >= THRESHOLD:
        return True, best_person, best_score
    else:
        return False, None, best_score


if __name__ == "__main__":
    test_fp = "../data/fingerprint/person1/fp1.BMP"
    test_ir = "../data/iris/person1/1-543.JPG"

    result, person, score = verify(test_fp, test_ir)

    if result:
        print(f"\nACCESS GRANTED → {person} (score={score:.3f})")
    else:
        print("\nACCESS DENIED")
