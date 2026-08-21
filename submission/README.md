# Submission checklist

## Metadata

- Repository: https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong
- Local evidence/code commit: `79587e99dac137e36d1030adcc4d343079c8f186`
- Step 1 MLflow experiment: `wine-quality-random-forest`
- Best MLflow run: `bd9db57d9a8646c98b89873811022f8c`
- Step 2 run URL/ID: [32447145525](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32447145525); Unit Test success, Train failed at missing `CLOUD_CREDENTIALS`
- Eval-gate negative run URL/ID: chưa có; mới kiểm tra local với accuracy `0.694`
- Step 3 data-trigger run URL/ID: chưa có
- GCS bucket: chưa tạo (thiếu project Day 21 được cấp phép)
- VM name/IP: chưa tạo/chưa có
- `GET /health`: chưa verify trên VM
- `POST /predict`: chưa verify trên VM

## Rubric → evidence

- MLflow >= 3 runs: `experiment_results.csv` (16 runs thật; UI screenshot còn manual)
- Accuracy/F1 và best params: `experiment_results.csv`, `report.md`, `params.yaml`
- DVC pointers: `data/*.dvc`; remote cloud chưa cấu hình vì chưa có bucket hợp lệ
- Eval gate: `evidence/local-eval-gate.txt`; chưa có Actions negative run
- Step 2 pipeline: run thật đã kiểm tra; blocked at cloud authentication because no repository secrets
- Step 3 data-trigger: chưa chạy vì Step 2 cloud baseline chưa khả dụng

## Cleanup after grading

Sau khi grading xong, có thể xóa bucket, VM, firewall và service account lab theo resource names thực tế được tạo. Chưa thực hiện cleanup.
