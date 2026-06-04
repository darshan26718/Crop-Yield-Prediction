import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("data/data_season.csv")

print("Dataset Shape:", df.shape)

# --------------------------------------------------
# REMOVE MISSING VALUES
# --------------------------------------------------

df = df.dropna()

# --------------------------------------------------
# FEATURES & TARGET
# --------------------------------------------------

X = df.drop("yeilds", axis=1)
y = df["yeilds"]

# --------------------------------------------------
# COLUMN GROUPS
# --------------------------------------------------

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

# --------------------------------------------------
# PREPROCESSOR
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)

# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

print("Training Model...")

pipeline.fit(X_train, y_train)

print("Training Completed")

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

y_pred = pipeline.predict(X_test)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5

r2 = r2_score(y_test, y_pred)

print("\nModel Performance")
print("-" * 40)

print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    pipeline,
    "model/crop_yield_model.pkl"
)

print("\nModel Saved Successfully")
print("Path: model/crop_yield_model.pkl")

# --------------------------------------------------
# SAMPLE PREDICTION
# --------------------------------------------------

sample = X.iloc[[0]]

prediction = pipeline.predict(sample)

print("\nSample Prediction")
print("Predicted Yield:", prediction[0])
