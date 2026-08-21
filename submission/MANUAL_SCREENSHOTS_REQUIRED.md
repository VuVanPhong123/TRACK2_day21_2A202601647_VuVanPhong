# Manual screenshots required

Browser automation was unavailable in this environment, so no screenshots were fabricated. Capture these real views manually after opening the listed URLs:

1. `01-mlflow-runs.png`: open `http://127.0.0.1:5000`, choose experiment `wine-quality-random-forest`, and show at least three runs with `accuracy`, `f1_score`, model type, and hyperparameters.
2. `02-step2-actions-green.png`: open [green Step 2 run 32452594273](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32452594273) and show Unit Test, Train, Eval, Deploy all green.
3. `03-step3-actions-green.png`: open [Step 3 run 32453289515](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32453289515) and show the four green jobs plus commit `1748341334a78e688dcc270d32d750e900724612`.
4. `04-cloud-storage.png`: open bucket `track2-day21-2a202601647-mlops-20260821` and show `dvc/` plus `models/latest/model.pkl`.
5. `05-api-curl.png`: show the real `GET /health`, `POST /predict`, and HTTP 400 response for an invalid feature length at `http://136.115.109.5:8000`.
