# ============================================================
# utils/preprocessing.py
# Crop Yield Prediction Project
# ============================================================

import pandas as pd
import numpy as np

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler
)

# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(filepath):
    """
    Load CSV dataset
    """

    df = pd.read_csv(filepath)

    return df


# ============================================================
# DATASET SUMMARY
# ============================================================

def dataset_summary(df):
    """
    Dataset summary information
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }

    return summary


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

def handle_missing_values(df):

    for col in df.columns:

        if df[col].dtype == "object":

            df[col].fillna(
                df[col].mode()[0],
                inplace=True
            )

        else:

            df[col].fillna(
                df[col].median(),
                inplace=True
            )

    return df


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):

    df = df.drop_duplicates()

    return df


# ============================================================
# COLUMN CLEANING
# ============================================================

def clean_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ============================================================
# LABEL ENCODING
# ============================================================

def label_encode_columns(
        df,
        categorical_columns
):

    encoders = {}

    for col in categorical_columns:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(
            df[col]
        )

        encoders[col] = encoder

    return df, encoders


# ============================================================
# STANDARD SCALING
# ============================================================

def standard_scale_features(
        df,
        numerical_columns
):

    scaler = StandardScaler()

    df[numerical_columns] = scaler.fit_transform(
        df[numerical_columns]
    )

    return df, scaler


# ============================================================
# MINMAX SCALING
# ============================================================

def minmax_scale_features(
        df,
        numerical_columns
):

    scaler = MinMaxScaler()

    df[numerical_columns] = scaler.fit_transform(
        df[numerical_columns]
    )

    return df, scaler


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_feature_engineering(df):

    if (
        "rainfall" in df.columns and
        "temperature" in df.columns
    ):

        df["rainfall_temp_ratio"] = (
            df["rainfall"] /
            (df["temperature"] + 1)
        )

    if (
        "humidity" in df.columns and
        "temperature" in df.columns
    ):

        df["humidity_temp_ratio"] = (
            df["humidity"] /
            (df["temperature"] + 1)
        )

    return df


# ============================================================
# OUTLIER REMOVAL
# ============================================================

def remove_outliers(
        df,
        column
):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR

    upper_bound = Q3 + 1.5 * IQR

    df = df[
        (df[column] >= lower_bound)
        &
        (df[column] <= upper_bound)
    ]

    return df


# ============================================================
# TRAINING DATA PREPARATION
# ============================================================

def prepare_training_data(df):

    target_column = "yeilds"

    X = df.drop(
        target_column,
        axis=1
    )

    y = df[target_column]

    return X, y


# ============================================================
# COMPLETE PREPROCESSING PIPELINE
# ============================================================

def preprocess_dataset(filepath):

    df = load_dataset(filepath)

    df = handle_missing_values(df)

    df = remove_duplicates(df)

    summary = dataset_summary(df)

    return df, summary


# ============================================================
# DISPLAY DATASET INFO
# ============================================================

def print_dataset_info(df):

    print("=" * 60)

    print("DATASET INFORMATION")

    print("=" * 60)

    print("Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("=" * 60)


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    filepath = "data/data_season.csv"

    df = load_dataset(filepath)

    print_dataset_info(df)

    df, summary = preprocess_dataset(filepath)

    print("\nSummary")

    print(summary)

    print("\nPreprocessing Completed Successfully")
