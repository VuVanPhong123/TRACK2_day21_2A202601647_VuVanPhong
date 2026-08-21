# Manual screenshots required

Browser automation was unavailable in this environment, so no screenshots were fabricated.

1. `01-mlflow-runs.png`: mở `http://127.0.0.1:5000`, chọn experiment `wine-quality-random-forest`, hiển thị ít nhất 3 runs cùng `accuracy`, `f1_score` và hyperparameters.
2. `02-step2-actions-green.png`: mở GitHub repository → Actions → run Step 2, hiển thị Unit Test, Train, Eval, Deploy.
3. `03-step3-actions-green.png`: mở run do commit cập nhật `data/train_phase1.csv.dvc`, hiển thị cả 4 jobs và commit SHA.
4. `04-cloud-storage.png`: mở GCS bucket, hiển thị prefix `dvc/` và `models/latest/model.pkl`.
5. `05-api-curl.png`: hiển thị kết quả thật của `GET /health`, `POST /predict` và HTTP 400 cho input sai độ dài.
