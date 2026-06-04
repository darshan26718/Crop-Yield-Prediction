# ============================================================
# model/train_model.py
# Crop Yield Prediction Model Training
# ============================================================

import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================================================
# LOAD DATA
# ============================================================

def load_dataset():

    df = pd.read_csv(
        "data/data_season.csv"
    )

    return df


# ============================================================
# PREPROCESS DATA
# ============================================================

def prepare_data(df):

    X = df.drop(
        "yeilds",
        axis=1
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
# BUILD MODEL PIPELINE
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
        n_estimators=300,
        max_depth=20,
        random_state=42,
        n_jobs=-1
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

    pipeline.fit(X, y)

    return pipeline


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model():

    df = load_dataset()

    (
        X,
        y,
        categorical_features,
        numerical_features
    ) = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    pipeline = build_pipeline(
        categorical_features,
        numerical_features
    )

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        y_test,
        predictions
    )

    results = {

        "MAE": round(mae, 2),

        "MSE": round(mse, 2),

        "RMSE": round(rmse, 2),

        "R2 Score": round(r2, 4)

    }

    return results


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def get_feature_importance():

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

    model = pipeline.named_steps[
        "model"
    ]

    importances = model.feature_importances_

    return importances


# ============================================================
# SINGLE PREDICTION
# ============================================================

def predict_yield(
        year,
        location,
        area,
        rainfall,
        temperature,
        soil_type,
        irrigation,
        humidity,
        crop,
        price,
        season
):

    model = train_model()

    sample = pd.DataFrame([{

        "Year": year,

        "Location": location,

        "Area": area,

        "Rainfall": rainfall,

        "Temperature": temperature,

        "Soil type": soil_type,

        "Irrigation": irrigation,

        "Humidity": humidity,

        "Crops": crop,

        "price": price,

        "Season": season

    }])

    prediction = model.predict(
        sample
    )

    return round(
        float(prediction[0]),
        2
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

def model_summary():

    df = load_dataset()

    summary = {

        "Rows":
            df.shape[0],

        "Columns":
            df.shape[1],

        "Target":
            "yeilds",

        "Model":
            "RandomForestRegressor",

        "Features":
            len(df.columns) - 1

    }

    return summary


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CROP YIELD MODEL TRAINING")
    print("=" * 60)

    model = train_model()

    print("\nModel Trained Successfully")

    print("\nModel Summary")

    print(model_summary())

    print("\nEvaluation Metrics")

    metrics = evaluate_model()

    for key, value in metrics.items():

        print(
            f"{key}: {value}"
        )

    print("\nSample Prediction")

    prediction = predict_yield(

        year=2025,

        location="Hassan",

        area=100,

        rainfall=900,

        temperature=28,

        soil_type="Loamy",

        irrigation="Drip",

        humidity=70,

        crop="Rice",

        price=2500,

        season="Kharif"

    )

    print(
        f"Predicted Yield: {prediction}"
    )

    print("\nTraining Completed Successfully")
