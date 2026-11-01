import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix
from preprocess import X_train, y_train, X_test, y_test

y_test_bin = (y_test != "normal").astype(int)
X_normal = X_train[y_train == "normal"]

for c in [0.01, 0.05, 0.10]:
    model = IsolationForest(n_estimators=200, contamination=c, random_state=42, n_jobs=-1)
    model.fit(X_normal)
    preds = (model.predict(X_test) == -1).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test_bin, preds).ravel()
    print("=" * 50)
    print("contamination:", c)
    print("Detection rate:", round(tp / (tp + fn), 4))
    print("False alarm rate:", round(fp / (fp + tn), 4))

    results = pd.DataFrame({"category": y_test.values, "flagged": preds})
    attacks = results[results["category"] != "normal"]
    print(attacks.groupby("category")["flagged"].mean().round(3))