def win_probability(matches, team1, team2):

    df = matches[
        ((matches['team1'] == team1) & (matches['team2'] == team2)) |
        ((matches['team1'] == team2) & (matches['team2'] == team1))
    ]

    if df.empty:
        return {
            'error': 'No matches found'
        }

    total = len(df)

    team1_wins = (df['match_winner'] == team1).sum()
    team2_wins = (df['match_winner'] == team2).sum()

    return {
        team1: round(team1_wins / total * 100, 2),
        team2: round(team2_wins / total * 100, 2)
    }
