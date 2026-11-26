"""Recompute the frequencies reported in the review from the coded dataset.

Usage:  python reproduce_results.py
Reads   ../04_Coded_Dataset/coded_dataset.csv
Writes  outputs/frequencies.csv, outputs/by_period.csv, outputs/sensitivity_recomputed.csv
Only the Python standard library is required.
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "04_Coded_Dataset" / "coded_dataset.csv"
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)

rows = list(csv.DictReader(open(DATA, encoding="utf-8-sig")))
for r in rows:
    r["metrics"] = {m.strip() for m in r["Metrics reported"].split(",")}
    r["period"] = "2020-2022" if int(r["Year"]) <= 2022 else "2023-2026"

pct = lambda k, n: round(100 * k / n, 1)

# ---------------------------------------------------------------- 1. frequencies of every coded variable
SINGLE = ["Year", "Country of the dataset", "Publication type (from bibliographic record)", "Data source",
          "Best-performing model", "Sequential model", "Validation strategy", "Probability calibration",
          "Class imbalance treatment", "Generative balancing", "Explanation method", "Fairness analysis",
          "Early warning system", "Dashboard or platform", "Operational deployment",
          "Evaluation of an intervention", "Delivery mode", "Ethics review", "Informed consent", "Anonymization",
          "Data-protection regulation cited", "Data availability", "Code availability"]
n = len(rows)
with open(OUT / "frequencies.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["variable", "category", "studies", "percent"])
    for v in SINGLE:
        for cat, k in sorted(Counter(r[v] for r in rows).items(), key=lambda x: (-x[1], x[0])):
            w.writerow([v, cat, k, pct(k, n)])
    for m, k in Counter(m for r in rows for m in r["metrics"]).most_common():
        w.writerow(["Metrics reported (multiple per study)", m, k, pct(k, n)])

# ---------------------------------------------------------------- 2. indicators used in the text
INDICATORS = {
    "SIS only": lambda r: r["Data source"] == "Student information system only",
    "Multi-source": lambda r: r["Data source"] == "Multiple sources",
    "RF best": lambda r: r["Best-performing model"] == "Random forest",
    "Decision tree best": lambda r: r["Best-performing model"] == "Decision tree",
    "No imbalance treatment": lambda r: r["Class imbalance treatment"] == "None reported",
    "Imbalance treatment": lambda r: r["Class imbalance treatment"] != "None reported",
    "Accuracy": lambda r: "Accuracy" in r["metrics"],
    "Recall": lambda r: "Recall" in r["metrics"],
    "Precision": lambda r: "Precision" in r["metrics"],
    "F1-score": lambda r: "F1" in r["metrics"],
    "AUC-ROC": lambda r: "AUC-ROC" in r["metrics"],
    "PR-AUC": lambda r: "PR-AUC" in r["metrics"],
    "Calibration": lambda r: r["Probability calibration"] == "Yes",
    "Temporal validation": lambda r: r["Validation strategy"] == "Temporal",
    "SHAP/LIME": lambda r: r["Explanation method"] in ("SHAP", "LIME"),
    "Fairness analysis (yes)": lambda r: r["Fairness analysis"] == "Yes",
    "Early warning system, dashboard or platform": lambda r: "Yes" in (r["Early warning system"], r["Dashboard or platform"]),
    "Operational deployment": lambda r: r["Operational deployment"] == "Yes",
    "Intervention evaluated": lambda r: r["Evaluation of an intervention"] == "Yes",
    "Ethics approval/exemption": lambda r: r["Ethics review"] != "Not reported",
    "Informed consent": lambda r: r["Informed consent"] == "Yes",
    "Anonymization": lambda r: r["Anonymization"] == "Reported",
    "Regulation cited": lambda r: r["Data-protection regulation cited"] != "Not reported",
    "Public data": lambda r: r["Data availability"] == "Public",
    "Public code": lambda r: r["Code availability"] == "Public",
}

def table(groups, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["indicator"] + [f"{name} (n = {len(g)})" for name, g in groups])
        for ind, fn in INDICATORS.items():
            w.writerow([ind] + [f"{sum(map(fn, g))} ({pct(sum(map(fn, g)), len(g))}%)" for _, g in groups])

# ---------------------------------------------------------------- 3. comparison by period
table([("All", rows)] + [(p, [r for r in rows if r["period"] == p]) for p in ("2020-2022", "2023-2026")], OUT / "by_period.csv")

# ---------------------------------------------------------------- 4. sensitivity analyses S1-S3
TEAM = {"ART67_SCP", "ART226_SCP"}                                   # co-authored by the review team
DISCUSSED = {"ART64_SCP", "ART323_WOS", "ART251_SCP"}  # book chapter, dropout intention, case discussed during verification
table([("Main analysis", rows),
       ("S1: without team co-authored studies", [r for r in rows if r["Study ID"] not in TEAM]),
       ("S2: without studies whose eligibility required discussion", [r for r in rows if r["Study ID"] not in DISCUSSED]),
       ("S3: journal articles only", [r for r in rows if r["Publication type (from bibliographic record)"] == "Journal article"])],
      OUT / "sensitivity_recomputed.csv")

print(f"{n} studies; wrote frequencies.csv, by_period.csv and sensitivity_recomputed.csv to {OUT}")
