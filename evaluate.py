import os
import numpy as np
from itertools import combinations
from sklearn.metrics import roc_curve, auc
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

TEMPLATE_DIR = "templates"

def cosine_score(a, b):
    return cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))[0][0]

def load_templates():
    data = {}
    for person in os.listdir(TEMPLATE_DIR):
        person_dir = os.path.join(TEMPLATE_DIR, person)
        if not os.path.isdir(person_dir):
            continue
        fp = np.load(os.path.join(person_dir, "fingerprint.npy"))
        ir = np.load(os.path.join(person_dir, "iris.npy"))
        data[person] = {"fp": fp, "ir": ir}
    return data

def generate_trials(data):
    fp_scores = []
    ir_scores = []
    labels = []

    persons = list(data.keys())

    # Genuine trials
    for person in persons:
        fp_feats = data[person]["fp"]
        ir_feats = data[person]["ir"]

        for i in range(len(fp_feats)):
            for j in range(i+1, len(fp_feats)):
                fp_scores.append(cosine_score(fp_feats[i], fp_feats[j]))
                ir_scores.append(cosine_score(ir_feats[i], ir_feats[j]))
                labels.append(1)

    # Impostor trials
    for p1, p2 in combinations(persons, 2):
        fp1 = data[p1]["fp"]
        fp2 = data[p2]["fp"]
        ir1 = data[p1]["ir"]
        ir2 = data[p2]["ir"]

        for f1 in fp1:
            for f2 in fp2:
                for i1 in ir1:
                    for i2 in ir2:
                        fp_scores.append(cosine_score(f1, f2))
                        ir_scores.append(cosine_score(i1, i2))
                        labels.append(0)

    return np.array(fp_scores), np.array(ir_scores), np.array(labels)

def compute_metrics(scores, labels):
    fpr, tpr, thresholds = roc_curve(labels, scores)
    roc_auc = auc(fpr, tpr)
    fnr = 1 - tpr
    eer = fpr[np.nanargmin(np.absolute(fnr - fpr))]
    return roc_auc, eer, fpr, tpr

def zscore_normalize(scores):
    return (scores - np.mean(scores)) / (np.std(scores) + 1e-8)

if __name__ == "__main__":
    print("Loading templates...")
    data = load_templates()

    print("Generating trials...")
    fp_scores, ir_scores, labels = generate_trials(data)

    print(f"Collected {len(labels)} trials")

    # Normalize
    fp_norm = zscore_normalize(fp_scores)
    ir_norm = zscore_normalize(ir_scores)

    print("\nEvaluating single modalities...")
    fp_auc, fp_eer, fp_fpr, fp_tpr = compute_metrics(fp_norm, labels)
    ir_auc, ir_eer, ir_fpr, ir_tpr = compute_metrics(ir_norm, labels)

    print(f"Fingerprint AUC={fp_auc:.4f}  EER={fp_eer:.4f}")
    print(f"Iris AUC={ir_auc:.4f}  EER={ir_eer:.4f}")

    print("\nTesting weighted fusion strategies...")
    best_auc = 0
    best_weight = 0
    best_fusion = None
    best_fpr = None
    best_tpr = None
    best_eer = None

    for w in np.arange(0.5, 0.95, 0.05):
        fusion = w * fp_norm + (1-w) * ir_norm
        fusion_auc, fusion_eer, fpr, tpr = compute_metrics(fusion, labels)

        print(f"Weight {w:.2f}/{1-w:.2f} → AUC={fusion_auc:.4f}  EER={fusion_eer:.4f}")

        if fusion_auc > best_auc:
            best_auc = fusion_auc
            best_weight = w
            best_fusion = fusion
            best_fpr = fpr
            best_tpr = tpr
            best_eer = fusion_eer

    print("\nBest Fusion Result:")
    print(f"Best Weight: FP={best_weight:.2f}, Iris={1-best_weight:.2f}")
    print(f"Fusion AUC={best_auc:.4f}  EER={best_eer:.4f}")

    # Plot ROC
    plt.figure()
    plt.plot(fp_fpr, fp_tpr, label=f"Fingerprint (AUC={fp_auc:.2f})")
    plt.plot(ir_fpr, ir_tpr, label=f"Iris (AUC={ir_auc:.2f})")
    plt.plot(best_fpr, best_tpr, label=f"Fusion (AUC={best_auc:.2f})")
    plt.plot([0,1],[0,1],'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve Comparison")
    plt.legend()
    plt.show()
