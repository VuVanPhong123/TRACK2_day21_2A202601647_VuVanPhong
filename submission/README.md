# Day 21 submission evidence

Repository: https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong

The authoritative eval gate is `0.70`. The final model is a `RandomForestClassifier` with raw 12 inputs plus deterministic `density_alcohol` and `sulfur_alcohol` features. No metric was rounded to pass, and no dataset generation or labels were changed.

## Final Actions evidence

- Step 2 green: [run 32459739043](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32459739043), successful attempt 2; four jobs green; accuracy `0.7000`, weighted F1 `0.6988602225`.
- Negative gate: [run 32460456911](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460456911); Eval failed at `0.5500 < 0.70`, Deploy skipped, and GCS latest generation was unchanged.
- Restored green: [run 32460663067](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460663067); four jobs green; accuracy `0.7000`, weighted F1 `0.6988602225`.
- Step 3 data trigger: [run 32460997570](https://github.com/VuVanPhong123/TRACK2_day21_2A202601647_VuVanPhong/actions/runs/32460997570); pointer-only commit `7372e90`; four jobs green; accuracy `0.7480`, weighted F1 `0.7473569388`.

Historical `0.68` runs may be referenced as superseded intermediate runs, but are not final compliance evidence.

## Real resources

- DVC remote: `myremote -> gs://track2-day21-2a202601647-mlops-20260821/dvc`
- Bucket: `track2-day21-2a202601647-mlops-20260821`; final object `models/latest/model.pkl`
- Service account: `track2-day21-mlops-sa@track2-day16-2a202601647.iam.gserviceaccount.com`
- VM: `track2-day21-mlops-serve`, `136.115.109.5`, zone `us-central1-a`
- Firewall: `track2-day21-allow-8000`
- Final GCS model generation: `1787299301055162`
- GitHub authentication uses OIDC/WIF; no service-account key is stored in the repository.

## Final API evidence

- `GET http://136.115.109.5:8000/health` -> HTTP 200, `{"status":"ok"}`
- Rubric `POST /predict` -> HTTP 200, `{"prediction":0,"label":"thap"}`
- Invalid feature length -> HTTP 400
- `mlops-serve.service` is active after loading the feature-enabled model.

Final submission screenshots are stored in `submission/screenshots/`.