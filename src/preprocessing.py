def clean_data(
    matches,
    deliveries
):

    matches = matches.dropna(
        subset=['match_winner']
    ).copy()

    cols = [

        'team1',
        'team2',
        'match_winner',
        'toss_winner',
        'venue'

    ]

    for col in cols:

        matches[col] = (
            matches[col]
            .astype(str)
            .str.strip()
            .str.title()
        )

    return matches, deliveries
