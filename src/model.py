from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

import pandas as pd


def train_model(df):

    X = df.drop('team1_win', axis=1)
    y = df['team1_win']

    categorical_cols = [
        'team1',
        'team2',
        'venue',
        'toss_winner'
    ]

    numeric_cols = [
        'toss_win',
        'team1_win_rate',
        'team2_win_rate',
        'strength_diff',
        'venue_popularity',
        'team1_matches',
        'team2_matches',
        'experience_diff'
    ]

    preprocessor = ColumnTransformer([
        (
            'cat',
            OneHotEncoder(handle_unknown='ignore'),
            categorical_cols
        ),
        (
            'num',
            'passthrough',
            numeric_cols
        )
    ])

    model = Pipeline([
        ('preprocessor', preprocessor),

        ('classifier', XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            random_state=42
        ))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)

    print(f"Accuracy: {accuracy:.2f}")

    return model


def predict_match(
    model,
    team1,
    team2,
    venue,
    toss_winner
):

    input_df = pd.DataFrame([{

        'team1': team1,
        'team2': team2,
        'venue': venue,
        'toss_winner': toss_winner,

        'toss_win':
        1 if toss_winner == team1 else 0,

        'team1_win_rate': 0.55,
        'team2_win_rate': 0.50,

        'strength_diff': 0.05,

        'venue_popularity': 50,

        'team1_matches': 100,
        'team2_matches': 100,

        'experience_diff': 0

    }])

    probs = model.predict_proba(input_df)[0]

    return {

        'team1': team1,

        'team1_win_prob':
        round(probs[1] * 100, 2),

        'team2': team2,

        'team2_win_prob':
        round(probs[0] * 100, 2)
    }