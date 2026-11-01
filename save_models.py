import os
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from preprocess import X_train, y_train

y_bin = (y_train != "normal").astype(int)

rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_bin)

iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42, n_jobs=-1)
iso.fit(X_train[y_train == "normal"])
os.makedirs("models", exist_ok=True)
joblib.dump(rf, "models/rf_binary.joblib", compress=3)
joblib.dump(iso, "models/iso_forest.joblib", compress=3)
joblib.dump(list(X_train.columns), "models/feature_columns.joblib")

print("Saved. Feature count:", len(X_train.columns))
print(joblib.load("models/rf_binary.joblib").predict(X_train.head(5)))