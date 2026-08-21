# Báo cáo Day 21 MLOps

## Bước 1 – MLflow

Đã tạo dữ liệu thật đúng kích thước `2998 / 500 / 2998` và ghi nhận 16 MLflow runs trong experiment `wine-quality-random-forest`. Cấu hình tốt nhất trong các run là:

```yaml
n_estimators: 300
max_depth: null
min_samples_split: 2
max_features: sqrt
class_weight: {0: 1.25, 1: 0.75, 2: 0.75}
n_jobs: -1
```

Run tốt nhất: `bd9db57d9a8646c98b89873811022f8c`; accuracy `0.694`, F1 weighted `0.692202`. Cấu hình này được chọn vì có accuracy/F1 cao nhất trong các thí nghiệm hợp lệ, nhưng vẫn thấp hơn eval gate `0.70`; không hạ threshold và không dùng `eval.csv` để huấn luyện.

## Bước 2 và Bước 3

Đã dispatch một Actions run thật `32447145525`. Unit Test thành công; Train dừng tại bước xác thực vì repository chưa có secret `CLOUD_CREDENTIALS`, nên Eval/Deploy chưa chạy. Account GCP hiện authenticated nhưng project active là `track2-day16-2a202601647` (project của Day 16), không có project Day 21 phù hợp để tạo bucket/VM. Vì vậy chưa có Step 2/Step 3 metrics, VM endpoint hoặc GCS model.

Khó khăn chính là accuracy của RandomForest trên held-out dataset này chưa đạt `0.70`, cùng với thiếu project GCP riêng cho lab. Đã pin `setuptools<82` vì MLflow 2.13 cần `pkg_resources`.
