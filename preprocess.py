import pandas as pd
from sklearn.preprocessing import StandardScaler
from config import columns, attack_map

train = pd.read_csv("data/KDDTrain+.txt", header=None, names=columns)
test = pd.read_csv("data/KDDTest+.txt", header=None, names=columns)

for d in (train, test):
    d["attack_category"] = d["label"].map(attack_map)

print("Unmapped labels:", train["attack_category"].isnull().sum(),
      test["attack_category"].isnull().sum())

cat_cols = ["protocol_type", "service", "flag"]
combined = pd.concat([train, test], keys=["train", "test"])
combined = pd.get_dummies(combined, columns=cat_cols, dtype=int)
train_enc = combined.loc["train"]
test_enc = combined.loc["test"]

drop_cols = ["label", "difficulty", "attack_category"]
X_train = train_enc.drop(columns=drop_cols)
y_train = train_enc["attack_category"]
X_test = test_enc.drop(columns=drop_cols)
y_test = test_enc["attack_category"]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_train.shape, X_test.shape)
print(y_test.value_counts())