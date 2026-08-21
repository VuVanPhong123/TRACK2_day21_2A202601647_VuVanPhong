from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


FEATURES = [
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


def main() -> None:
    train_df = pd.read_csv("data/train_phase1.csv")
    eval_df = pd.read_csv("data/eval.csv")
    assert len(train_df) == 2998, len(train_df)
    assert len(eval_df) == 500, len(eval_df)
    assert list(train_df.drop(columns=["target"]).columns) == FEATURES
    assert list(eval_df.drop(columns=["target"]).columns) == FEATURES

    params = {
        "n_estimators": 300,
        "max_depth": 30,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "criterion": "gini",
        "bootstrap": True,
        "class_weight": {0: 1.25, 1: 0.75, 2: 0.75},
        "n_jobs": -1,
        "random_state": 42,
    }
    model = RandomForestClassifier(**params)
    model.fit(train_df[FEATURES], train_df["target"])

    probabilities = model.predict_proba(eval_df[FEATURES])
    predictions = model.classes_[probabilities.argmax(axis=1)]
    order = probabilities.argsort(axis=1)
    top1 = probabilities[range(len(eval_df)), order[:, -1]]
    top2 = probabilities[range(len(eval_df)), order[:, -2]]

    analysis = eval_df.copy()
    analysis.insert(len(FEATURES), "true_class", eval_df["target"].astype(int))
    analysis["predicted_class"] = predictions.astype(int)
    analysis["correct"] = analysis["true_class"] == analysis["predicted_class"]
    analysis["confidence"] = top1
    analysis["margin"] = top1 - top2
    analysis["prob_class_0"] = probabilities[:, 0]
    analysis["prob_class_1"] = probabilities[:, 1]
    analysis["prob_class_2"] = probabilities[:, 2]
    analysis = analysis.drop(columns=["target"])

    output = Path("tmp/rf_error_analysis.csv")
    output.parent.mkdir(exist_ok=True)
    analysis.to_csv(output, index=False)

    accuracy = float(accuracy_score(eval_df["target"], predictions))
    weighted_f1 = float(f1_score(eval_df["target"], predictions, average="weighted"))
    matrix = confusion_matrix(eval_df["target"], predictions, labels=[0, 1, 2])
    error_rows = analysis.loc[~analysis["correct"]]
    lowest_confidence = error_rows.sort_values(["confidence", "margin"]).head(20)
    lowest_margin = error_rows.sort_values(["margin", "confidence"]).head(20)

    summary = {
        "rows_train": len(train_df),
        "rows_eval": len(eval_df),
        "accuracy": accuracy,
        "weighted_f1": weighted_f1,
        "correct_count": int(analysis["correct"].sum()),
        "error_count": int((~analysis["correct"]).sum()),
        "confusion_matrix_labels_0_1_2": matrix.tolist(),
        "params": params,
        "lowest_confidence_error_indices": lowest_confidence.index.tolist(),
        "lowest_margin_error_indices": lowest_margin.index.tolist(),
    }
    Path("tmp/rf_error_analysis_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"rows_train={len(train_df)} rows_eval={len(eval_df)}")
    print(f"accuracy={accuracy:.6f} weighted_f1={weighted_f1:.6f}")
    print(f"correct={int(analysis['correct'].sum())}/500 errors={len(error_rows)}")
    print("confusion_matrix_labels_0_1_2=")
    print(matrix)
    print("lowest_confidence_errors=")
    print(lowest_confidence[["true_class", "predicted_class", "confidence", "margin"]].to_string())
    print("lowest_margin_errors=")
    print(lowest_margin[["true_class", "predicted_class", "confidence", "margin"]].to_string())


if __name__ == "__main__":
    main()
