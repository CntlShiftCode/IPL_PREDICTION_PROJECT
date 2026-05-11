import pandas as pd


def load_data():

    matches = pd.read_csv(
        "Data/matches.csv"
    )

    deliveries = pd.read_csv(
        "Data/deliveries.csv"
    )

    matches.columns = (
        matches.columns
        .str.strip()
        .str.lower()
    )

    deliveries.columns = (
        deliveries.columns
        .str.strip()
        .str.lower()
    )

    return matches, deliveries