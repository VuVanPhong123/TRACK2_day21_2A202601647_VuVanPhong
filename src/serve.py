import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from pydantic import BaseModel

app = FastAPI(title="Wine Quality Inference API")

GCS_BUCKET = os.environ["GCS_BUCKET"]
GCS_MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = Path(os.path.expanduser("~/models/model.pkl"))
EXPECTED_FEATURE_COUNT = 12
LABELS = {0: "thap", 1: "trung_binh", 2: "cao"}


def download_model() -> None:
    """Download the latest model artifact from GCS to the VM."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(GCS_MODEL_KEY)
    blob.download_to_filename(str(MODEL_PATH))

    print(
        f"Downloaded gs://{GCS_BUCKET}/{GCS_MODEL_KEY} "
        f"to {MODEL_PATH}"
    )


download_model()
model = joblib.load(MODEL_PATH)


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    """Return service health for deployment verification."""
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    """Predict the Wine Quality class for exactly 12 numeric features."""
    if len(req.features) != EXPECTED_FEATURE_COUNT:
        raise HTTPException(
            status_code=400,
            detail="Expected 12 features (wine quality)",
        )

    prediction = int(model.predict([req.features])[0])
    if prediction not in LABELS:
        raise HTTPException(
            status_code=500,
            detail=f"Model returned unsupported class: {prediction}",
        )

    return {"prediction": prediction, "label": LABELS[prediction]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
