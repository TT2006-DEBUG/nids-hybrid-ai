import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from config import columns, attack_map

app = Flask(__name__)

rf = joblib.load("models/rf_binary.joblib")
iso = joblib.load("models/iso_forest.joblib")
feature_columns = joblib.load("models/feature_columns.joblib")

CAT_COLS = ["protocol_type", "service", "flag"]
RAW_FEATURES = [c for c in columns if c not in ("label", "difficulty")]

test_df = pd.read_csv("data/KDDTest+.txt", header=None, names=columns)
test_df["category"] = test_df["label"].map(attack_map)


def prepare(records):
    df = pd.DataFrame(records)
    df = pd.get_dummies(df, columns=CAT_COLS, dtype=int)
    return df.reindex(columns=feature_columns, fill_value=0)


def run_models(records):
    X = prepare(records)
    rf_pred = rf.predict(X)
    iso_pred = (iso.predict(X) == -1).astype(int)
    scores = -iso.score_samples(X)
    return [
        {
            "supervised_flag": int(rf_pred[i]),
            "anomaly_flag": int(iso_pred[i]),
            "anomaly_score": round(float(scores[i]), 4),
            "alert": bool(rf_pred[i] or iso_pred[i]),
        }
        for i in range(len(X))
    ]


def compute_stats():
    records = test_df[RAW_FEATURES].to_dict(orient="records")
    df = pd.DataFrame(run_models(records))
    df["category"] = test_df["category"].values
    stats = {}
    for cat, g in df.groupby("category"):
        sup = g["supervised_flag"] == 1
        ano = g["anomaly_flag"] == 1
        stats[cat] = {
            "total": int(len(g)),
            "both": int((sup & ano).sum()),
            "supervised_only": int((sup & ~ano).sum()),
            "anomaly_only": int((~sup & ano).sum()),
            "not_flagged": int((~sup & ~ano).sum()),
        }
    return stats


STATS = compute_stats()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    records = request.get_json()
    if isinstance(records, dict):
        records = [records]
    for i, rec in enumerate(records):
        missing = [f for f in RAW_FEATURES if f not in rec]
        if missing:
            return jsonify({"error": f"record {i} is missing fields", "missing": missing}), 400
    return jsonify(run_models(records))


@app.route("/demo")
def demo():
    n = request.args.get("n", 20, type=int)
    n = max(1, min(n, 100))
    sample = test_df.sample(n)
    results = run_models(sample[RAW_FEATURES].to_dict(orient="records"))
    for res, (_, row) in zip(results, sample.iterrows()):
        res["label"] = row["label"]
        res["category"] = row["category"]
        res["protocol"] = row["protocol_type"]
        res["service"] = row["service"]
    return jsonify(results)


@app.route("/stats")
def stats():
    return jsonify(STATS)


if __name__ == "__main__":
    app.run(debug=False)