# ============================================================
# model/train_model.py
# ============================================================

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.ensemble import RandomForestRegressor


# ============================================================
# LOAD DATA
# ============================================================

def load_dataset():

    df = pd.read_csv(
        "data/data_season.csv"
    )

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    numeric_columns = [
        "Year",
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "price",
        "yeilds"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df = df.dropna()

    X = df.drop(
        columns=["yeilds"]
    )

    y = df["yeilds"]

    categorical_features = [
        "Location",
        "Soil type",
        "Irrigation",
        "Crops",
        "Season"
    ]

    numerical_features = [
        "Year",
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "price"
    ]

    return (
        X,
        y,
        categorical_features,
        numerical_features
    )


# ============================================================
# BUILD PIPELINE
# ============================================================

def build_pipeline(
    categorical_features,
    numerical_features
):

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "num",
                StandardScaler(),
                numerical_features
            ),

            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            )

        ]

    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    pipeline = Pipeline([

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )

    ])

    return pipeline


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    df = load_dataset()

    (
        X,
        y,
        categorical_features,
        numerical_features

    ) = prepare_data(df)

    pipeline = build_pipeline(
        categorical_features,
        numerical_features
    )

    pipeline.fit(
        X,
        y
    )

    return pipeline


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    model = train_model()

    print(
        "Model Trained Successfully"
    )
