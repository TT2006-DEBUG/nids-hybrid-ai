# AI-Powered Network Intrusion Detection (NSL-KDD)

A hybrid intrusion detection system that combines a supervised Random Forest with an Isolation Forest anomaly detector, served through a Flask API and a browser dashboard.

## How it works
- **Supervised model:** a Random Forest trained on labeled normal and attack connections.
- **Anomaly model:** an Isolation Forest trained on normal traffic only, so it can flag attack types it has never seen.
- **Hybrid rule:** a connection raises an alert if either model flags it.
- **Dashboard:** shows detection rates by attack family on the full test set, plus a live batch of random connections with each verdict and which model raised it.

## Results (NSL-KDD test set, 22,544 connections)

| Attack family | Connections | Detected |
|---|---|---|
| DoS | 7,460 | 86.8% |
| Probe | 2,421 | 95.4% |
| R2L | 2,752 | 5.9% |
| U2R | 200 | 34.0% |
| Normal traffic (false alarms) | 9,711 | 2.96% |

Overall, the hybrid detects 70.2% of attacks at a 2.96% false alarm rate. The supervised model alone detects 60.8% at 2.74%.

## Key findings
- The test file contains attack types that never appear in training, so a supervised model cannot recognize them. For example, 89% of the R2L training rows are one attack type (warezclient) that does not appear in the test set.
- The anomaly model caught 1,212 attacks the supervised model missed, at a cost of only 21 extra false alarms.
- R2L is the limit: it accounts for about two thirds of the attacks still missed. These attacks look like ordinary connections in the 41 features.
- A validation split from the training data badly underestimated false alarms (0.06% for the supervised model, against 2.74% on the test set), because the test file's normal traffic differs from the training file's.

## Limitations
- NSL-KDD is derived from late-1990s traffic, so these numbers say little about modern networks.
- The models use 41 pre-computed connection features, not raw packets.
- I looked at test-set results while comparing settings, so the final figures are slightly optimistic.

## Run it
Download the NSL-KDD dataset (University of New Brunswick) and put `KDDTrain+.txt` and `KDDTest+.txt` in a `data/` folder.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python save_models.py
python app.py
```

Then open http://127.0.0.1:5000

## Files
- `config.py`, `preprocess.py`: column names, attack-family mapping, data preparation
- `train.py`, `binary.py`, `anomaly.py`, `hybrid.py`, `validate.py`, `check_unseen.py`: the experiments
- `save_models.py`: trains and saves the final models
- `app.py`, `templates/index.html`: Flask API and dashboard