# ============================================================
# utils/insights.py
# Crop Yield Prediction Project
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# BEST CROP
# ============================================================

def get_best_crop(df):

    crop = (
        df.groupby("Crops")["yeilds"]
        .mean()
        .sort_values(ascending=False)
    )

    return crop.index[0], round(crop.iloc[0], 2)


# ============================================================
# BEST LOCATION
# ============================================================

def get_best_location(df):

    location = (
        df.groupby("Location")["yeilds"]
        .mean()
        .sort_values(ascending=False)
    )

    return location.index[0], round(location.iloc[0], 2)


# ============================================================
# BEST SEASON
# ============================================================

def get_best_season(df):

    season = (
        df.groupby("Season")["yeilds"]
        .mean()
        .sort_values(ascending=False)
    )

    return season.index[0], round(season.iloc[0], 2)


# ============================================================
# TOP CROPS
# ============================================================

def get_top_crops(df, top_n=10):

    return (
        df.groupby("Crops")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


# ============================================================
# TOP LOCATIONS
# ============================================================

def get_top_locations(df, top_n=10):

    return (
        df.groupby("Location")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


# ============================================================
# SEASON PERFORMANCE
# ============================================================

def get_season_performance(df):

    return (
        df.groupby("Season")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )


# ============================================================
# SOIL PERFORMANCE
# ============================================================

def get_soil_performance(df):

    return (
        df.groupby("Soil type")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )


# ============================================================
# IRRIGATION PERFORMANCE
# ============================================================

def get_irrigation_performance(df):

    return (
        df.groupby("Irrigation")["yeilds"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )


# ============================================================
# RAINFALL INSIGHTS
# ============================================================

def rainfall_insights(df):

    avg_rainfall = round(
        df["Rainfall"].mean(),
        2
    )

    max_rainfall = round(
        df["Rainfall"].max(),
        2
    )

    min_rainfall = round(
        df["Rainfall"].min(),
        2
    )

    return {
        "Average Rainfall": avg_rainfall,
        "Maximum Rainfall": max_rainfall,
        "Minimum Rainfall": min_rainfall
    }


# ============================================================
# TEMPERATURE INSIGHTS
# ============================================================

def temperature_insights(df):

    avg_temp = round(
        df["Temperature"].mean(),
        2
    )

    max_temp = round(
        df["Temperature"].max(),
        2
    )

    min_temp = round(
        df["Temperature"].min(),
        2
    )

    return {
        "Average Temperature": avg_temp,
        "Maximum Temperature": max_temp,
        "Minimum Temperature": min_temp
    }


# ============================================================
# HUMIDITY INSIGHTS
# ============================================================

def humidity_insights(df):

    avg_humidity = round(
        df["Humidity"].mean(),
        2
    )

    max_humidity = round(
        df["Humidity"].max(),
        2
    )

    min_humidity = round(
        df["Humidity"].min(),
        2
    )

    return {
        "Average Humidity": avg_humidity,
        "Maximum Humidity": max_humidity,
        "Minimum Humidity": min_humidity
    }


# ============================================================
# PRICE INSIGHTS
# ============================================================

def price_insights(df):

    avg_price = round(
        df["price"].mean(),
        2
    )

    max_price = round(
        df["price"].max(),
        2
    )

    min_price = round(
        df["price"].min(),
        2
    )

    return {
        "Average Price": avg_price,
        "Maximum Price": max_price,
        "Minimum Price": min_price
    }


# ============================================================
# CORRELATION INSIGHTS
# ============================================================

def correlation_insights(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    correlation = numeric_df.corr()

    yield_corr = (
        correlation["yeilds"]
        .sort_values(ascending=False)
    )

    return yield_corr


# ============================================================
# DATASET SUMMARY
# ============================================================

def dataset_summary(df):

    return {
        "Total Records": len(df),
        "Total Locations":
            df["Location"].nunique(),
        "Total Crops":
            df["Crops"].nunique(),
        "Total Seasons":
            df["Season"].nunique(),
        "Average Yield":
            round(df["yeilds"].mean(), 2)
    }


# ============================================================
# SMART RECOMMENDATIONS
# ============================================================

def generate_recommendations(df):

    recommendations = []

    avg_yield = df["yeilds"].mean()

    avg_rainfall = df["Rainfall"].mean()

    avg_temp = df["Temperature"].mean()

    avg_humidity = df["Humidity"].mean()

    if avg_yield < 50:
        recommendations.append(
            "Improve irrigation and soil management practices."
        )

    if avg_rainfall < 800:
        recommendations.append(
            "Consider additional irrigation support during dry periods."
        )

    if avg_temp > 30:
        recommendations.append(
            "Use heat-resistant crop varieties."
        )

    if avg_humidity < 50:
        recommendations.append(
            "Monitor crop water requirements closely."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Current agricultural conditions appear favorable."
        )

    return recommendations


# ============================================================
# COMPLETE INSIGHT REPORT
# ============================================================

def generate_full_report(df):

    best_crop, crop_yield = get_best_crop(df)

    best_location, location_yield = get_best_location(df)

    best_season, season_yield = get_best_season(df)

    report = {
        "Best Crop": best_crop,
        "Best Crop Yield": crop_yield,

        "Best Location": best_location,
        "Best Location Yield": location_yield,

        "Best Season": best_season,
        "Best Season Yield": season_yield,

        "Dataset Summary":
            dataset_summary(df),

        "Rainfall Insights":
            rainfall_insights(df),

        "Temperature Insights":
            temperature_insights(df),

        "Humidity Insights":
            humidity_insights(df),

        "Price Insights":
            price_insights(df),

        "Recommendations":
            generate_recommendations(df)
    }

    return report


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "../data/data_season.csv"
    )

    print("=" * 60)
    print("SMART INSIGHTS REPORT")
    print("=" * 60)

    report = generate_full_report(df)

    for key, value in report.items():
        print(f"\n{key}")
        print(value)

    print("\nInsights Module Executed Successfully")
