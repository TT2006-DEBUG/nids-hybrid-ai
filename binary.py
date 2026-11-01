import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from preprocess import X_train, y_train, X_test, y_test

y_train_bin = (y_train != "normal").astype(int)
y_test_bin = (y_test != "normal").astype(int)

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train_bin)
preds = model.predict(X_test)

tn, fp, fn, tp = confusion_matrix(y_test_bin, preds).ravel()

print("Accuracy:", round(accuracy_score(y_test_bin, preds), 4))
print("Detection rate (attacks caught):", round(tp / (tp + fn), 4))
print("False alarm rate (normal flagged):", round(fp / (fp + tn), 4))
print("Missed attacks:", fn, "of", tp + fn)

results = pd.DataFrame({"category": y_test.values, "flagged": preds})
attacks = results[results["category"] != "normal"]
print(attacks.groupby("category")["flagged"].mean().round(3))