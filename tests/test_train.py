import json
import os

import joblib
import numpy as np
import pandas as pd

from src.train import train


FEATURE_NAMES = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "wine_type",
]


def _make_temp_data(tmp_path):
    """Create a small Wine Quality-shaped dataset for unit tests."""
    rng = np.random.default_rng(0)
    n = 200

    X = rng.random((n, len(FEATURE_NAMES)))
    y = rng.integers(0, 3, size=n)

    df = pd.DataFrame(X, columns=FEATURE_NAMES)
    df["target"] = y

    train_path = str(tmp_path / "train.csv")
    eval_path = str(tmp_path / "eval.csv")
    df.iloc[:160].to_csv(train_path, index=False)
    df.iloc[160:].to_csv(eval_path, index=False)

    return train_path, eval_path


def test_train_returns_float(tmp_path):
    """train() returns a float accuracy in the expected range."""
    train_path, eval_path = _make_temp_data(tmp_path)

    accuracy = train(
        {"n_estimators": 10, "max_depth": 3},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert isinstance(accuracy, float)
    assert 0.0 <= accuracy <= 1.0


def test_metrics_file_created(tmp_path):
    """Training writes a metrics file containing both rubric metrics."""
    train_path, eval_path = _make_temp_data(tmp_path)
    train(
        {"n_estimators": 10, "max_depth": 3},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert os.path.exists("outputs/metrics.json")
    with open("outputs/metrics.json", encoding="utf-8") as f:
        metrics = json.load(f)

    assert "accuracy" in metrics
    assert "f1_score" in metrics
    assert 0.0 <= float(metrics["accuracy"]) <= 1.0
    assert 0.0 <= float(metrics["f1_score"]) <= 1.0


def test_model_file_created(tmp_path):
    """Training writes the model artifact consumed by deployment."""
    train_path, eval_path = _make_temp_data(tmp_path)
    train(
        {"n_estimators": 10, "max_depth": 3},
        data_path=train_path,
        eval_path=eval_path,
    )

    assert os.path.exists("models/model.pkl")


def test_feature_engineering_pipeline_is_serialized(tmp_path):
    """The configured deterministic feature families remain in the saved pipeline."""
    train_path, eval_path = _make_temp_data(tmp_path)
    train(
        {
            "model_type": "random_forest",
            "feature_engineering": {
                "families": ["density_alcohol", "sulfur_alcohol"],
            },
            "model_params": {"n_estimators": 10, "max_depth": 3},
        },
        data_path=train_path,
        eval_path=eval_path,
    )

    model = joblib.load("models/model.pkl")
    assert model.named_steps["feature_engineering"].families == (
        "density_alcohol",
        "sulfur_alcohol",
    )
    eval_features = pd.read_csv(eval_path).drop(columns=["target"])
    assert len(model.predict(eval_features)) == 40
