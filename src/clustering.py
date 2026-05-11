from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def player_clustering(deliveries):

    df = deliveries.copy()

    print(df.columns)

    # =========================
    # TOTAL RUNS
    # =========================

    df['total_runs'] = (
        df['runs_of_bat']
        + df['extras']
    )

    # =========================
    # PLAYER STATS
    # =========================

    player_stats = (
        df.groupby('striker')
        .agg({
            'total_runs': 'sum'
        })
    )

    # balls faced
    player_stats['balls_faced'] = (
        df.groupby('striker')
        .size()
    )

    player_stats = player_stats.reset_index()

    # =========================
    # STRIKE RATE
    # =========================

    player_stats['strike_rate'] = (
        player_stats['total_runs']
        / player_stats['balls_faced']
    ) * 100

    # =========================
    # FEATURES
    # =========================

    X = player_stats[[
        'total_runs',
        'strike_rate'
    ]]

    # =========================
    # SCALE FEATURES
    # =========================

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # =========================
    # KMEANS
    # =========================

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    player_stats['cluster'] = (
        kmeans.fit_predict(X_scaled)
    )

    return player_stats