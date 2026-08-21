import json
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import (
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

EVAL_THRESHOLD = 0.70
TARGET_COLUMN = "target"
DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "wine-quality-random-forest"

MODEL_TYPES = {
    "random_forest": RandomForestClassifier,
    "extra_trees": ExtraTreesClassifier,
    "hist_gradient_boosting": HistGradientBoostingClassifier,
    "gradient_boosting": GradientBoostingClassifier,
}


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


def _normalise_config(params: dict) -> tuple[str, dict, dict]:
    """Support the original flat RF config and the extensible model schema."""
    if not isinstance(params, dict) or not params:
        raise ValueError("params must be a non-empty dictionary")

    if "model_type" in params:
        model_type = str(params["model_type"])
        model_params = dict(params.get("model_params", {}))
        validation = dict(params.get("validation", {}))
    else:
        model_type = "random_forest"
        model_params = dict(params)
        validation = {}

    if model_type not in MODEL_TYPES:
        supported = ", ".join(sorted(MODEL_TYPES))
        raise ValueError(f"Unsupported model_type {model_type!r}; use one of: {supported}")

    validation.setdefault("test_size", 0.2)
    validation.setdefault("random_state", 42)
    model_params.setdefault("random_state", 42)
    return model_type, model_params, validation


def _build_model(model_type: str, model_params: dict):
    """Build a supported sklearn estimator from the tracked configuration."""
    return MODEL_TYPES[model_type](**model_params)


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """Select with a train-only validation split, then fit and score the candidate."""
    model_type, model_params, validation = _normalise_config(params)

    df_train = _load_dataset(data_path)
    df_eval = _load_dataset(eval_path)

    X_train = df_train.drop(columns=[TARGET_COLUMN])
    y_train = df_train[TARGET_COLUMN]
    X_eval = df_eval.drop(columns=[TARGET_COLUMN])
    y_eval = df_eval[TARGET_COLUMN]

    if list(X_train.columns) != list(X_eval.columns):
        raise ValueError("Training and evaluation feature columns must match exactly.")

    X_fit, X_validation, y_fit, y_validation = train_test_split(
        X_train,
        y_train,
        test_size=validation["test_size"],
        stratify=y_train,
        random_state=validation["random_state"],
    )

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", DEFAULT_TRACKING_URI)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    run_name = (
        f"{model_type}_n{model_params.get('n_estimators', 'default')}"
        f"_depth{model_params.get('max_depth', 'default')}"
        f"_split{model_params.get('min_samples_split', 'default')}"
    )

    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("model_type", model_type)
        mlflow.log_params(
            {f"model_params.{key}": value for key, value in model_params.items()}
        )
        mlflow.log_params(
            {
                "validation.test_size": validation["test_size"],
                "validation.random_state": validation["random_state"],
            }
        )

        validation_model = _build_model(model_type, model_params)
        validation_model.fit(X_fit, y_fit)
        validation_predictions = validation_model.predict(X_validation)
        validation_accuracy = float(
            accuracy_score(y_validation, validation_predictions)
        )
        validation_f1 = float(
            f1_score(y_validation, validation_predictions, average="weighted")
        )

        model = _build_model(model_type, model_params)
        model.fit(X_train, y_train)

        predictions = model.predict(X_eval)
        accuracy = float(accuracy_score(y_eval, predictions))
        f1 = float(f1_score(y_eval, predictions, average="weighted"))

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("validation_accuracy", validation_accuracy)
        mlflow.log_metric("validation_f1_score", validation_f1)
        mlflow.sklearn.log_model(model, "model")

        outputs_dir = Path("outputs")
        models_dir = Path("models")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        models_dir.mkdir(parents=True, exist_ok=True)

        metrics = {
            "accuracy": accuracy,
            "f1_score": f1,
            "validation_accuracy": validation_accuracy,
            "validation_f1_score": validation_f1,
            "model_type": model_type,
            "eval_threshold": EVAL_THRESHOLD,
        }
        with (outputs_dir / "metrics.json").open("w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        joblib.dump(model, models_dir / "model.pkl")

        print(
            f"Model: {model_type} | "
            f"Validation accuracy: {validation_accuracy:.4f} | "
            f"Held-out accuracy: {accuracy:.4f} | F1: {f1:.4f}"
        )

    return accuracy


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        model_params = yaml.safe_load(f)
    train(model_params)
