# Day 21 MLOps report

## Final model and evaluation

Model type: `random_forest` (`sklearn.ensemble.RandomForestClassifier`).

```yaml
n_estimators: 300
max_depth: 30
min_samples_split: 2
min_samples_leaf: 1
max_features: sqrt
criterion: gini
bootstrap: true
class_weight: {0: 1.25, 1: 0.75, 2: 0.75}
n_jobs: -1
random_state: 42
feature_families: [density_alcohol, sulfur_alcohol]
eval_threshold: 0.70
```

The serialized sklearn pipeline accepts the original 12 features and adds `alcohol_density`, `alcohol_density_gap`, and `total_sulfur_alcohol_ratio`. Phase 1 reproduced accuracy `0.7000` (`350/500`) and weighted F1 `0.6988602224515537`. The final Step 2 Actions artifact reports the same result. Step 3 reports accuracy `0.7480` and weighted F1 `0.7473569387652077` on 5996 training rows.

Step 1 retains the original 20 MLflow RandomForest runs. The prior best was run `c661a0eccc7b4daa806276f4f7eba402` at accuracy `0.6940`, F1 `0.6922020059`. The feature-family implementation was selected in the local Step-1 experimentation workflow and reproduced deterministically before CI.

## Remote evidence

- Step 2: [32459739043](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32459739043), commit `e2e84fa`, four green jobs, `0.7000 / 0.6988602225`.
- Negative gate: [32460456911](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460456911), `0.5500 < 0.70`, Eval failed and Deploy skipped. GCS generation stayed `1787298423263119` before and after.
- Restored green: [32460663067](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460663067), four green jobs, `0.7000 / 0.6988602225`.
- Step 3: [32460997570](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460997570), pointer-only commit `7372e90`, four green jobs, `0.7480 / 0.7473569388`.

The old `0.68` runs are superseded intermediate evidence and are not used for acceptance.

## Step 3 data transition

The precondition was verified at exactly `2998` rows. `add_new_data.py` was run exactly once and changed the local dataset to exactly `5996` rows. `dvc add` and `dvc push` completed before Git push. Commit `7372e90cd23db7e98a1ace1ec7643d058e4d07ea` contains only `data/train_phase1.csv.dvc` and automatically triggered the final Step 3 run.

## Cloud and serving

The real DVC remote is `myremote` at `gs://track2-day21-2a202601647-mlops-20260821/dvc`; `dvc status --cloud` reports the cache and remote are in sync. The final model object is `models/latest/model.pkl`, generation `1787299301055162`.

VM `track2-day21-mlops-serve` runs `mlops-serve.service` with FastAPI on port 8000. The workflow uploads `src/serve.py` and `feature_engineering.py` to both the required root paths and the active `mlops-serve` directory, and ensures the serving venv has pandas for the transformer.

```text
/health: {"status":"ok"} (HTTP 200)
/predict: {"prediction":0,"label":"thap"} (HTTP 200)
invalid feature length: HTTP 400
systemd: active (running)
```

## Security and screenshots

GitHub Actions uses OIDC Workload Identity Federation. No credential JSON, private SSH key, raw CSV, model binary, `.env`, or MLflow database is tracked. Browser screenshots were not fabricated; the manual screenshot file lists the final Actions, MLflow, GCS, and API views to capture.
