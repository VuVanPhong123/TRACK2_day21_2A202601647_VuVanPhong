# Day 21 submission evidence

Repository: https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong

The organizer-authorized eval gate for this run is `0.68`. The model is selected from a stratified validation split of `data/train_phase1.csv`; `data/eval.csv` is only scored after the candidate is fixed.

## Real resources

- DVC remote: `myremote -> gs://track2-day21-2a202601647-mlops-20260821/dvc`
- Bucket: `track2-day21-2a202601647-mlops-20260821`
- Service account: `track2-day21-mlops-sa@track2-day16-2a202601647.iam.gserviceaccount.com`
- VM: `track2-day21-mlops-serve`, `136.115.109.5`
- Firewall: `track2-day21-allow-8000`
- GitHub authentication uses OIDC/WIF; no service-account key is stored in the repository.

## Actions evidence

- Step 2 green: [run 32452594273](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32452594273) — all 4 jobs green; accuracy `0.6820`, F1 `0.6808`.
- Negative gate: [run 32452836880](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32452836880) — Unit Test/Train green, Eval failed at `0.5480 < 0.68`, Deploy skipped; `latest` generation remained unchanged.
- Restored green: [run 32453041890](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32453041890) — all 4 jobs green; accuracy `0.6820`, F1 `0.6808`.
- Step 3 data-trigger: [run 32453289515](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32453289515) — automatically triggered by commit `1748341334a78e688dcc270d32d750e900724612`; all 4 jobs green; accuracy `0.7480`, F1 `0.7471`.

## API evidence

- `GET http://136.115.109.5:8000/health` -> `{"status":"ok"}`
- `POST /predict` with the rubric sample -> `{"prediction":0,"label":"thap"}`
- Invalid feature length -> HTTP `400`

See `report.md`, `metrics-comparison.md`, and `evidence/` for the detailed records. Screenshots were not fabricated; the manual capture instructions remain in `MANUAL_SCREENSHOTS_REQUIRED.md`.
