import pandas as pd


def create_features(
    matches,
    deliveries
):

    match_df = matches.copy()
    delivery_df = deliveries.copy()

    match_df['team1_win'] = (

        match_df['match_winner']
        == match_df['team1']

    ).astype(int)

    match_df['toss_win'] = (

        match_df['toss_winner']
        == match_df['team1']

    ).astype(int)

    team_stats = pd.concat([

        pd.DataFrame({

            'team': match_df['team1'],
            'win': match_df['team1_win']

        }),

        pd.DataFrame({

            'team': match_df['team2'],
            'win': 1 - match_df['team1_win']

        })

    ])

    team_win_rate = (
        team_stats.groupby('team')['win']
        .mean()
    )

    match_df['team1_win_rate'] = (
        match_df['team1']
        .map(team_win_rate)
    )

    match_df['team2_win_rate'] = (
        match_df['team2']
        .map(team_win_rate)
    )

    match_df['strength_diff'] = (

        match_df['team1_win_rate']
        -
        match_df['team2_win_rate']

    )

    venue_count = (
        match_df['venue']
        .value_counts()
    )

    match_df['venue_popularity'] = (
        match_df['venue']
        .map(venue_count)
    )

    matches_played = (

        pd.concat([
            match_df['team1'],
            match_df['team2']
        ])
        .value_counts()

    )

    match_df['team1_matches'] = (
        match_df['team1']
        .map(matches_played)
    )

    match_df['team2_matches'] = (
        match_df['team2']
        .map(matches_played)
    )

    match_df['experience_diff'] = (

        match_df['team1_matches']
        -
        match_df['team2_matches']

    )

    match_df = match_df.fillna(0)

    features = match_df[[
        'team1',
        'team2',
        'venue',
        'toss_winner',

        'toss_win',

        'team1_win_rate',
        'team2_win_rate',

        'strength_diff',

        'venue_popularity',

        'team1_matches',
        'team2_matches',

        'experience_diff',

        'team1_win'
    ]]

    return features, delivery_df