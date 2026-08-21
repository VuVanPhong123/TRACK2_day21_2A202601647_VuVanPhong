# Manual screenshots required

Browser automation was unavailable in this environment, so no screenshots were fabricated. Do not capture the historical `0.68` runs as final evidence. Capture these views only after a new compliant `0.70` Step 2 and Step 3 run exists:

1. `01-mlflow-runs.png`: open `http://127.0.0.1:5000`, choose experiment `wine-quality-random-forest`, and show at least three runs with `accuracy`, `f1_score`, model type, and hyperparameters.
2. `02-step2-actions-green.png`: open the new `0.70`-gate Step 2 run and show Unit Test, Train, Eval, Deploy all green.
3. `03-step3-actions-green.png`: open the new data-trigger Step 3 run using `0.70` and show the four green jobs plus its pointer-only commit.
4. `04-cloud-storage.png`: open bucket `track2-day21-2a202601647-mlops-20260821` and show `dvc/` plus `models/latest/model.pkl`.
5. `05-api-curl.png`: show the real `GET /health`, `POST /predict`, and HTTP 400 response for an invalid feature length at `http://136.115.109.5:8000`.
