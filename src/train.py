import json
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

EVAL_THRESHOLD = 0.70
TARGET_COLUMN = "target"
DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "wine-quality-random-forest"


def _load_dataset(path: str) -> pd.DataFrame:
    """Load a CSV dataset and validate the target column."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Dataset {dataset_path} must contain target column '{TARGET_COLUMN}'."
        )
    return df


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """Train a RandomForest model, track metrics, and persist CI artifacts."""
    if not isinstance(params, dict) or not params:
        raise ValueError("params must be a non-empty dictionary")

    df_train = _load_dataset(data_path)
    df_eval = _load_dataset(eval_path)

    X_train = df_train.drop(columns=[TARGET_COLUMN])
    y_train = df_train[TARGET_COLUMN]
    X_eval = df_eval.drop(columns=[TARGET_COLUMN])
    y_eval = df_eval[TARGET_COLUMN]

    if list(X_train.columns) != list(X_eval.columns):
        raise ValueError("Training and evaluation feature columns must match exactly.")

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", DEFAULT_TRACKING_URI)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    run_name = (
        f"rf_n{params.get('n_estimators', 'default')}"
        f"_depth{params.get('max_depth', 'default')}"
        f"_split{params.get('min_samples_split', 'default')}"
    )

    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params)

        model = RandomForestClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_eval)
        accuracy = float(accuracy_score(y_eval, predictions))
        f1 = float(f1_score(y_eval, predictions, average="weighted"))

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        outputs_dir = Path("outputs")
        models_dir = Path("models")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        models_dir.mkdir(parents=True, exist_ok=True)

        metrics = {"accuracy": accuracy, "f1_score": f1}
        with (outputs_dir / "metrics.json").open("w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        joblib.dump(model, models_dir / "model.pkl")

        print(f"Accuracy: {accuracy:.4f} | F1: {f1:.4f}")

    return accuracy


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        model_params = yaml.safe_load(f)
    train(model_params)
