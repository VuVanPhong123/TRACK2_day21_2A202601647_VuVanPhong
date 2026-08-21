# Manual screenshots required

Browser automation was unavailable in this environment, so no screenshots were fabricated. Capture these real views only:

1. `01-mlflow-runs.png`: open `http://127.0.0.1:5000`, choose `wine-quality-random-forest`, and show at least three runs with accuracy, f1_score, model type, and hyperparameters.
2. `02-step2-actions-green.png`: open [Step 2 run 32459739043](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32459739043) and show Unit Test, Train, Eval, Deploy all green.
3. `03-step3-actions-green.png`: open [Step 3 run 32460997570](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460997570) and show the four green jobs, the `0.70` threshold, and pointer-only commit `7372e90`.
4. `04-cloud-storage.png`: open bucket `track2-day21-2a202601647-mlops-20260821` and show `dvc/` plus `models/latest/model.pkl`.
5. `05-api-curl.png`: show the real `GET /health`, rubric `POST /predict`, and HTTP 400 response for invalid feature length at `http://136.115.109.5:8000`.

The negative-gate and restored-green URLs are recorded in `submission/evidence/` and may be captured as supplemental evidence.
