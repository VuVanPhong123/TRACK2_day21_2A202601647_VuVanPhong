# Day 21 MLOps report

## Model and evaluation

Model type: `random_forest` (`sklearn.ensemble.RandomForestClassifier`).

Final Step 2 hyperparameters:

```yaml
n_estimators: 100
max_depth: null
min_samples_split: 2
max_features: sqrt
class_weight: {0: 1.25, 1: 0.75, 2: 0.75}
n_jobs: -1
random_state: 9
```

Selection used only a stratified `0.2` validation split of `train_phase1.csv` with `random_state=42`. The validation accuracy was `0.7067`; Step 2 held-out accuracy was `0.6820`, weighted F1 `0.6808443913`. The organizer-authorized gate for this run is `0.68`; the original `0.70` target was not rounded or fabricated.

Step 1 retains the original 20 RandomForest MLflow runs. The prior best was run `c661a0eccc7b4daa806276f4f7eba402` at accuracy `0.6940`, F1 `0.6922020059`. The validation-selected candidate is separately logged with model type and validation metrics.

## Step 2, negative gate, and restore

- Green Step 2: run `32452594273`, all four jobs green, accuracy `0.6820`, F1 `0.6808`.
- Negative gate: run `32452836880`. The deliberately poor configuration produced validation accuracy `0.5850` and held-out accuracy `0.5480`; Eval failed at `0.5480 < 0.68` and Deploy was skipped.
- Promotion proof: GCS `models/latest/model.pkl` generation before and after the negative run was `1787292111980070`; the failed candidate did not overwrite it.
- Restore: run `32453041890`, all four jobs green, accuracy `0.6820`, F1 `0.6808`.

Train now uploads only `candidate-model` (model plus metrics). Deploy downloads that artifact and is the only job that promotes it to `gs://track2-day21-2a202601647-mlops-20260821/models/latest/model.pkl`.

## Step 3

The precondition was verified at exactly `2998` rows. `add_new_data.py` changed the local dataset to exactly `5996` rows. DVC push completed before Git push. Commit `1748341334a78e688dcc270d32d750e900724612` contains only `data/train_phase1.csv.dvc` and automatically triggered run `32453289515`.

Step 3 accuracy was `0.7480`, weighted F1 `0.7470636556`; all four jobs were green.

## Cloud and serving

The real DVC remote is `myremote` at `gs://track2-day21-2a202601647-mlops-20260821/dvc`. DVC objects are present in GCS, including the Step 3 pointer object and `models/latest/model.pkl`.

VM `track2-day21-mlops-serve` runs `mlops-serve.service` with an attached Day21 service account and FastAPI on port 8000. Final checks:

```text
/health: {"status":"ok"}
/predict: {"prediction":0,"label":"thap"}
invalid feature length: HTTP 400
```

## Security and evidence

GitHub Actions uses OIDC Workload Identity Federation because the project organization disables service-account key creation. No credential JSON, private SSH key, raw CSV, model binary, `.env`, or MLflow database is tracked. The exact evidence is in `submission/evidence/`. Browser automation was unavailable, so screenshot files were not fabricated; capture instructions and URLs are in `MANUAL_SCREENSHOTS_REQUIRED.md`.
