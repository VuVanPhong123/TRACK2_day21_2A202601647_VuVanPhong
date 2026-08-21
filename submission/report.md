# Day 21 MLOps report

## Model and evaluation

Model type: `random_forest` (`sklearn.ensemble.RandomForestClassifier`).

Best bounded-search RandomForest candidate (not rubric-passing):

```yaml
n_estimators: 300
max_depth: 30
min_samples_split: 2
max_features: sqrt
class_weight: {0: 1.25, 1: 0.75, 2: 0.75}
n_jobs: -1
random_state: 42
```

The authoritative gate is `0.70`. The bounded local search used exactly 2998 Phase-1 rows and 500 eval rows, reproduced the historical baseline at `0.6940 / 0.6922020059`, and found a best candidate at held-out accuracy `0.6960` and weighted F1 `0.6942`. The search was stopped at its bounded budget; no metric was rounded or fabricated.

Step 1 retains the original 20 RandomForest MLflow runs. The prior best was run `c661a0eccc7b4daa806276f4f7eba402` at accuracy `0.6940`, F1 `0.6922020059`. The validation-selected candidate is separately logged with model type and validation metrics.

## Historical Step 2, negative gate, and restore (superseded 0.68 gate)

- Green Step 2: run `32452594273`, all four jobs green, accuracy `0.6820`, F1 `0.6808`.
- Negative gate: run `32452836880`. The deliberately poor configuration produced validation accuracy `0.5850` and held-out accuracy `0.5480`; Eval failed at `0.5480 < 0.68` and Deploy was skipped.
- Promotion proof: GCS `models/latest/model.pkl` generation before and after the negative run was `1787292111980070`; the failed candidate did not overwrite it.
- Restore: run `32453041890`, all four jobs green, accuracy `0.6820`, F1 `0.6808`.

Train now uploads only `candidate-model` (model plus metrics). Deploy downloads that artifact and is the only job that promotes it to `gs://track2-day21-2a202601647-mlops-20260821/models/latest/model.pkl`.

## Step 3 historical evidence (superseded 0.68 gate)

The precondition was verified at exactly `2998` rows. `add_new_data.py` changed the local dataset to exactly `5996` rows. DVC push completed before Git push. Commit `1748341334a78e688dcc270d32d750e900724612` contains only `data/train_phase1.csv.dvc` and automatically triggered run `32453289515`.

The previous Step 3 accuracy was `0.7480`, weighted F1 `0.7470636556`; all four jobs were green under the superseded `0.68` gate. No new `0.70` Step 3 run was generated because the compliant Step 2 candidate was not found.

## Cloud and serving

The real DVC remote is `myremote` at `gs://track2-day21-2a202601647-mlops-20260821/dvc`. DVC objects are present in GCS, including the Step 3 pointer object and `models/latest/model.pkl`.

VM `track2-day21-mlops-serve` runs `mlops-serve.service` with an attached Day21 service account and FastAPI on port 8000. Final checks:

```text
/health: {"status":"ok"}
/predict: {"prediction":0,"label":"thap"}
invalid feature length: HTTP 400
```

## Current blocker

The bounded RandomForest search exhausted without reaching `accuracy >= 0.70`. The repository is not submission-complete under the authoritative assignment requirement; see the untracked root `job.txt` for the exact search record and handoff.

## Security and evidence

GitHub Actions uses OIDC Workload Identity Federation because the project organization disables service-account key creation. No credential JSON, private SSH key, raw CSV, model binary, `.env`, or MLflow database is tracked. The exact evidence is in `submission/evidence/`. Browser automation was unavailable, so screenshot files were not fabricated; capture instructions and URLs are in `MANUAL_SCREENSHOTS_REQUIRED.md`.
