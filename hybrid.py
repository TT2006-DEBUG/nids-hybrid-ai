import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import confusion_matrix
from preprocess import X_train, y_train, X_test, y_test

y_train_bin = (y_train != "normal").astype(int)
y_test_bin = (y_test != "normal").astype(int)

rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train_bin)
rf_pred = rf.predict(X_test)

X_normal = X_train[y_train == "normal"]


def report(name, preds):
    tn, fp, fn, tp = confusion_matrix(y_test_bin, preds).ravel()
    print(name)
    print("  Detection rate:", round(tp / (tp + fn), 4))
    print("  False alarm rate:", round(fp / (fp + tn), 4))
    results = pd.DataFrame({"category": y_test.values, "flagged": preds})
    attacks = results[results["category"] != "normal"]
    print(" ", attacks.groupby("category")["flagged"].mean().round(3).to_dict())


report("Supervised only", rf_pred)

for c in [0.01, 0.05]:
    iso = IsolationForest(n_estimators=200, contamination=c, random_state=42, n_jobs=-1)
    iso.fit(X_normal)
    iso_pred = (iso.predict(X_test) == -1).astype(int)
    report(f"Anomaly only (contamination={c})", iso_pred)
    report(f"Hybrid: either flags (contamination={c})", rf_pred | iso_pred)