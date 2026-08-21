from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


RAW_FEATURE_COLUMNS = [
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
EPSILON = 1e-9


class WineFeatureEngineer(BaseEstimator, TransformerMixin):
    """Add the selected deterministic wine-quality feature families."""

    def __init__(self, families=()):
        self.families = families

    def fit(self, X, y=None):
        return self

    def _as_frame(self, X) -> pd.DataFrame:
        if isinstance(X, pd.DataFrame):
            frame = X.copy()
            missing = [column for column in RAW_FEATURE_COLUMNS if column not in frame]
            if missing:
                raise ValueError(f"Missing raw feature columns: {missing}")
            return frame[RAW_FEATURE_COLUMNS]
        return pd.DataFrame(X, columns=RAW_FEATURE_COLUMNS)

    def transform(self, X):
        result = self._as_frame(X)
        for family in self.families:
            if family == "sulfur_alcohol":
                result["total_sulfur_alcohol_ratio"] = result["total sulfur dioxide"] / (
                    result["alcohol"] + EPSILON
                )
            elif family == "density_alcohol":
                result["alcohol_density"] = result["alcohol"] * result["density"]
                result["alcohol_density_gap"] = result["alcohol"] * (1.0 - result["density"])
            elif family == "sulfur":
                result["bound_sulfur"] = result["total sulfur dioxide"] - result["free sulfur dioxide"]
                result["free_total_sulfur_ratio"] = result["free sulfur dioxide"] / (
                    result["total sulfur dioxide"] + EPSILON
                )
            elif family == "acidity":
                result["total_acidity"] = (
                    result["fixed acidity"]
                    + result["volatile acidity"]
                    + result["citric acid"]
                )
                result["volatile_fixed_ratio"] = result["volatile acidity"] / (
                    result["fixed acidity"] + EPSILON
                )
                result["volatile_citric_ratio"] = result["volatile acidity"] / (
                    result["citric acid"] + EPSILON
                )
            elif family == "sulphate_chloride":
                result["sulphates_chlorides_ratio"] = result["sulphates"] / (
                    result["chlorides"] + EPSILON
                )
            elif family == "sugar_alcohol":
                result["sugar_alcohol_ratio"] = result["residual sugar"] / (
                    result["alcohol"] + EPSILON
                )
            elif family == "wine_type":
                result["alcohol_by_wine_type"] = result["alcohol"] * result["wine_type"]
                result["sugar_by_wine_type"] = result["residual sugar"] * result["wine_type"]
            else:
                raise ValueError(f"Unknown feature family: {family}")
        return result
