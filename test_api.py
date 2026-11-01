import pandas as pd
import requests
from config import columns

test = pd.read_csv("data/KDDTest+.txt", header=None, names=columns)
sample = test.sample(15, random_state=1)

records = sample.drop(columns=["label", "difficulty"]).to_dict(orient="records")
response = requests.post("http://127.0.0.1:5000/predict", json=records)
results = response.json()

for label, r in zip(sample["label"], results):
    print(label, "->", r)