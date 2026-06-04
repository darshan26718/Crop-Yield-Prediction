# ============================================================
# utils/visualization.py
# Crop Yield Prediction Project
# ============================================================

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# GLOBAL SETTINGS
# ============================================================

sns.set_style("whitegrid")

# ============================================================
# DATASET OVERVIEW
# ============================================================

def plot_dataset_overview(df):

    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumns:")
    print(df.columns.tolist())


# ============================================================
# MISSING VALUES HEATMAP
# ============================================================

def plot_missing_values(df):

    plt.figure(figsize=(12, 6))

    sns.heatmap(
        df.isnull(),
        cbar=False,
        yticklabels=False
    )

    plt.title("Missing Values Heatmap")

    plt.show()


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

def plot_yield_distribution(df):

    plt.figure(figsize=(10, 5))

    sns.histplot(
        df["yeilds"],
        kde=True
    )

    plt.title("Yield Distribution")
    plt.xlabel("Yield")
    plt.ylabel("Frequency")

    plt.show()


# ============================================================
# CROP DISTRIBUTION
# ============================================================

def plot_crop_distribution(df):

    plt.figure(figsize=(15, 6))

    sns.countplot(
        x=df["Crops"],
        order=df["Crops"].value_counts().index
    )

    plt.xticks(rotation=90)

    plt.title("Crop Distribution")

    plt.show()


# ============================================================
# LOCATION DISTRIBUTION
# ============================================================

def plot_location_distribution(df):

    plt.figure(figsize=(15, 6))

    sns.countplot(
        x=df["Location"],
        order=df["Location"].value_counts().index
    )

    plt.xticks(rotation=90)

    plt.title("Location Distribution")

    plt.show()


# ============================================================
# SEASON DISTRIBUTION
# ============================================================

def plot_season_distribution(df):

    fig = px.pie(
        df,
        names="Season",
        title="Season Distribution"
    )

    return fig


# ============================================================
# TOP CROPS BY YIELD
# ============================================================

def plot_top_crops(df, top_n=10):

    crop_yield = (
        df.groupby("Crops")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        x=crop_yield.index,
        y=crop_yield.values,
        labels={
            "x": "Crop",
            "y": "Average Yield"
        },
        title=f"Top {top_n} Crops by Yield"
    )

    return fig


# ============================================================
# TOP LOCATIONS BY YIELD
# ============================================================

def plot_top_locations(df, top_n=10):

    location_yield = (
        df.groupby("Location")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        x=location_yield.index,
        y=location_yield.values,
        labels={
            "x": "Location",
            "y": "Average Yield"
        },
        title=f"Top {top_n} Locations by Yield"
    )

    return fig


# ============================================================
# SEASONAL YIELD ANALYSIS
# ============================================================

def plot_seasonal_yield(df):

    season_yield = (
        df.groupby("Season")["yeilds"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        season_yield,
        x="Season",
        y="yeilds",
        title="Average Yield by Season"
    )

    return fig


# ============================================================
# SOIL TYPE ANALYSIS
# ============================================================

def plot_soil_analysis(df):

    soil_yield = (
        df.groupby("Soil type")["yeilds"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        soil_yield,
        x="Soil type",
        y="yeilds",
        title="Yield by Soil Type"
    )

    return fig


# ============================================================
# IRRIGATION ANALYSIS
# ============================================================

def plot_irrigation_analysis(df):

    irrigation_yield = (
        df.groupby("Irrigation")["yeilds"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        irrigation_yield,
        x="Irrigation",
        y="yeilds",
        title="Yield by Irrigation Type"
    )

    return fig


# ============================================================
# RAINFALL VS YIELD
# ============================================================

def plot_rainfall_vs_yield(df):

    fig = px.scatter(
        df,
        x="Rainfall",
        y="yeilds",
        color="Season",
        hover_data=["Crops"],
        title="Rainfall vs Yield"
    )

    return fig


# ============================================================
# TEMPERATURE VS YIELD
# ============================================================

def plot_temperature_vs_yield(df):

    fig = px.scatter(
        df,
        x="Temperature",
        y="yeilds",
        color="Season",
        hover_data=["Crops"],
        title="Temperature vs Yield"
    )

    return fig


# ============================================================
# HUMIDITY VS YIELD
# ============================================================

def plot_humidity_vs_yield(df):

    fig = px.scatter(
        df,
        x="Humidity",
        y="yeilds",
        color="Season",
        hover_data=["Crops"],
        title="Humidity vs Yield"
    )

    return fig


# ============================================================
# AREA VS YIELD
# ============================================================

def plot_area_vs_yield(df):

    fig = px.scatter(
        df,
        x="Area",
        y="yeilds",
        color="Crops",
        title="Area vs Yield"
    )

    return fig


# ============================================================
# PRICE VS YIELD
# ============================================================

def plot_price_vs_yield(df):

    fig = px.scatter(
        df,
        x="price",
        y="yeilds",
        color="Season",
        title="Price vs Yield"
    )

    return fig


# ============================================================
# CORRELATION HEATMAP
# ============================================================

def plot_correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    correlation = numeric_df.corr()

    fig = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return fig


# ============================================================
# BOXPLOT OF YIELD
# ============================================================

def plot_yield_boxplot(df):

    fig = px.box(
        df,
        y="yeilds",
        title="Yield Outlier Detection"
    )

    return fig


# ============================================================
# SEASON-WISE BOXPLOT
# ============================================================

def plot_season_boxplot(df):

    fig = px.box(
        df,
        x="Season",
        y="yeilds",
        color="Season",
        title="Yield Distribution by Season"
    )

    return fig


# ============================================================
# TREEMAP ANALYSIS
# ============================================================

def plot_crop_treemap(df):

    fig = px.treemap(
        df,
        path=["Season", "Crops"],
        values="yeilds",
        title="Crop Yield Treemap"
    )

    return fig


# ============================================================
# KPI METRICS
# ============================================================

def calculate_kpis(df):

    kpis = {
        "Total Records": len(df),
        "Average Yield": round(
            df["yeilds"].mean(),
            2
        ),
        "Average Rainfall": round(
            df["Rainfall"].mean(),
            2
        ),
        "Average Temperature": round(
            df["Temperature"].mean(),
            2
        ),
        "Average Humidity": round(
            df["Humidity"].mean(),
            2
        )
    }

    return kpis


# ============================================================
# INSIGHT GENERATOR
# ============================================================

def generate_visual_insights(df):

    insights = {}

    insights["Best Crop"] = (
        df.groupby("Crops")["yeilds"]
        .mean()
        .idxmax()
    )

    insights["Best Location"] = (
        df.groupby("Location")["yeilds"]
        .mean()
        .idxmax()
    )

    insights["Best Season"] = (
        df.groupby("Season")["yeilds"]
        .mean()
        .idxmax()
    )

    return insights


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "../data/data_season.csv"
    )

    print("Visualization Module Loaded")

    print(calculate_kpis(df))

    print(generate_visual_insights(df))
