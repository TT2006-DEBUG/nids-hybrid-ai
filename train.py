from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from preprocess import X_train, y_train, X_test, y_test

models = {
  "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Decision Tree (balanced)": DecisionTreeClassifier(random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "Random Forest (balanced)": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight="balanced")   
}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print("=" * 60)
    print(name)
    print("Accuracy:", round(accuracy_score(y_test, preds), 4))
    print(classification_report(y_test, preds, zero_division=0))
    print(confusion_matrix(y_test, preds, labels=["normal", "DoS", "Probe", "R2L", "U2R"]))