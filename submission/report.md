# Báo cáo Day 21 – CI/CD cho AI Systems

## 1. Mô hình và kết quả thực nghiệm

Bài toán sử dụng bộ dữ liệu Wine Quality và mô hình
`RandomForestClassifier`. Sau nhiều lần thử nghiệm trên MLflow với các bộ
siêu tham số khác nhau, cấu hình cuối cùng được chọn là:

- `n_estimators = 300`
- `max_depth = 30`
- `min_samples_split = 2`
- `max_features = sqrt`
- `class_weight = {0: 1.25, 1: 0.75, 2: 0.75}`
- `random_state = 42`

Ngoài 12 đặc trưng gốc, pipeline bổ sung một số đặc trưng xác định từ dữ liệu
đầu vào, gồm `alcohol_density`, `alcohol_density_gap` và
`total_sulfur_alcohol_ratio`.

Cấu hình này được chọn vì RandomForest chỉ với các đặc trưng gốc đạt tốt nhất
khoảng `0.696` accuracy và chưa vượt qua ngưỡng Eval `0.70`. Sau khi bổ sung
feature engineering, mô hình đạt `0.7000` accuracy và `0.6989` weighted F1 trên
500 mẫu đánh giá, đủ điều kiện triển khai ở Bước 2.

## 2. Pipeline CI/CD và DVC

Dữ liệu được quản lý bằng DVC với Google Cloud Storage làm remote. GitHub
Actions gồm bốn job theo thứ tự:

`Unit Test → Train → Eval → Deploy`.

Eval gate sử dụng ngưỡng `accuracy >= 0.70`. Run Bước 2 đạt `0.7000` và cả bốn
job đều thành công. Một kiểm thử với mô hình yếu đạt `0.5500` đã làm Eval thất
bại và Deploy bị bỏ qua, xác nhận gate hoạt động đúng.

Ở Bước 3, 2.998 mẫu dữ liệu mới được bổ sung vào tập huấn luyện, tăng tổng số
mẫu từ `2.998` lên `5.996`. File DVC pointer được commit và push đã tự động kích
hoạt toàn bộ pipeline. Mô hình mới đạt `0.7480` accuracy và `0.7474` weighted
F1, sau đó được triển khai thành công.

## 3. Khó khăn và cách giải quyết

Khó khăn lớn nhất là mô hình RandomForest ban đầu không đạt được ngưỡng
accuracy `0.70` dù đã thử nhiều bộ siêu tham số. Thay vì hạ ngưỡng hoặc thay đổi
dữ liệu đánh giá, tôi giữ nguyên RandomForest và bổ sung feature engineering
deterministic. Transformer được đóng gói cùng mô hình trong sklearn Pipeline để
đảm bảo cùng một preprocessing được sử dụng khi train trong GitHub Actions và
khi inference trên VM.

Một khó khăn khác là model pickle có custom transformer cần đúng module và
dependency trên VM. Workflow deploy được cập nhật để đồng bộ
`feature_engineering.py` và các dependency cần thiết trước khi restart service.

Kết quả cuối cùng, FastAPI trên VM trả về thành công tại `/health` và
`/predict`, DVC remote hoạt động, Step 2 và Step 3 đều hoàn thành với Eval gate
`0.70`.