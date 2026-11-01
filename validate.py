from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from preprocess import X_train, y_train

y_bin = (y_train != "normal").astype(int)

X_fit, X_val, y_fit, y_val, yb_fit, yb_val = train_test_split(
    X_train, y_train, y_bin, test_size=0.2, stratify=y_train, random_state=42
)

rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_fit, yb_fit)
rf_pred = rf.predict(X_val)

X_fit_normal = X_fit[y_fit == "normal"]
val_normal = (y_val == "normal").values

print("Supervised false alarm rate on held-out normal:",
      round(rf_pred[val_normal].mean(), 4))

for c in [0.005, 0.01, 0.02, 0.05]:
    iso = IsolationForest(n_estimators=200, contamination=c, random_state=42, n_jobs=-1)
    iso.fit(X_fit_normal)
    iso_pred = (iso.predict(X_val) == -1).astype(int)
    hybrid = rf_pred | iso_pred

    print("contamination:", c)
    print("  Anomaly false alarm rate:", round(iso_pred[val_normal].mean(), 4))
    print("  Hybrid false alarm rate:", round(hybrid[val_normal].mean(), 4))