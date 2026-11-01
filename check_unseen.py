import pandas as pd
from config import columns, attack_map

train = pd.read_csv("data/KDDTrain+.txt", header=None, names=columns)
test = pd.read_csv("data/KDDTest+.txt", header=None, names=columns)

for d in (train, test):
    d["attack_category"] = d["label"].map(attack_map)

for cat in ["R2L", "U2R"]:
    print(cat)
    tr = train[train["attack_category"] == cat]["label"].value_counts()
    te = test[test["attack_category"] == cat]["label"].value_counts()
    table = pd.concat([tr.rename("train"), te.rename("test")], axis=1)
    print(table.fillna(0).astype(int))
    print()