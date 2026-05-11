import sys
import os

# ==========================================================
# FIX IMPORT PATH
# ==========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_data
from src.preprocessing import clean_data
from src.feature_engineering import create_features
from src.model import train_model, predict_match
from src.live_data import simulate_live_match

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="IPL Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# TITLE
# ==========================================================

st.title(
    "🏏 IPL Command Center : AI Analytics & Match Intelligence"
)

# ==========================================================
# LOAD DATA
# ==========================================================

matches, deliveries = load_data()

matches, deliveries = clean_data(
    matches,
    deliveries
)

features, deliveries = create_features(
    matches,
    deliveries
)

model = train_model(features)

teams = sorted(
    matches['team1']
    .dropna()
    .unique()
)

venues = sorted(
    matches['venue']
    .dropna()
    .unique()
)

# ==========================================================
# KPI CARDS
# ==========================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Matches",
    len(matches)
)

k2.metric(
    "Runs",
    int(deliveries['runs_of_bat'].sum())
)

k3.metric(
    "Fours",
    int(
        (
            deliveries['runs_of_bat']
            == 4
        ).sum()
    )
)

k4.metric(
    "Sixes",
    int(
        (
            deliveries['runs_of_bat']
            == 6
        ).sum()
    )
)

st.markdown("---")

# ==========================================================
# SIDEBAR
# ==========================================================

page = st.sidebar.selectbox(

    "Choose Section",

    [

        "Match Prediction",
        "Stats",
        "Team Stats",
        "Live Match Simulation"

    ]
)

# ==========================================================
# MATCH PREDICTION
# ==========================================================

if page == "Match Prediction":

    st.header(
        "🤖 AI Match Win Prediction"
    )

    c1, c2, c3 = st.columns(3)

    team1 = c1.selectbox(
        "Select Team 1",
        teams
    )

    team2 = c2.selectbox(
        "Select Team 2",
        teams
    )

    venue = c3.selectbox(
        "Select Venue",
        venues
    )

    if team1 == team2:

        st.warning(
            "Please select two different teams"
        )

        st.stop()

    toss_winner = st.selectbox(
        "Select Toss Winner",
        [team1, team2]
    )

    prediction = predict_match(
        model,
        team1,
        team2,
        venue,
        toss_winner
    )

    prob1 = prediction['team1_win_prob']
    prob2 = prediction['team2_win_prob']

    c4, c5 = st.columns(2)

    c4.metric(
        team1,
        f"{prob1:.2f}%"
    )

    c5.metric(
        team2,
        f"{prob2:.2f}%"
    )

    # ======================================================
    # MATCH COMPARISON
    # ======================================================

    st.subheader(
        "📊 Match Intelligence Comparison"
    )

    comparison_df = pd.DataFrame({

        'Metric': [

            'Win Probability',
            'Batting Strength',
            'Bowling Strength',
            'Powerplay',
            'Death Overs',
            'Momentum',
            'Fielding',
            'Pressure Handling'

        ],

        team1: np.random.randint(
            60,
            95,
            8
        ),

        team2: np.random.randint(
            60,
            95,
            8
        )

    })

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    # ======================================================
    # BAR GRAPH
    # ======================================================

    bar_fig = go.Figure()

    bar_fig.add_trace(go.Bar(

        x=comparison_df['Metric'],
        y=comparison_df[team1],

        name=team1,

        marker_color='royalblue'

    ))

    bar_fig.add_trace(go.Bar(

        x=comparison_df['Metric'],
        y=comparison_df[team2],

        name=team2,

        marker_color='orange'

    ))

    bar_fig.update_layout(

        barmode='group',

        title='Advanced Match Comparison',

        xaxis_title='Metrics',

        yaxis_title='Performance Score'

    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )

    # ======================================================
    # RADAR GRAPH
    # ======================================================

    radar_fig = go.Figure()

    radar_fig.add_trace(go.Scatterpolar(

        r=comparison_df[team1],

        theta=comparison_df['Metric'],

        fill='toself',

        name=team1,

        line=dict(color='royalblue')

    ))

    radar_fig.add_trace(go.Scatterpolar(

        r=comparison_df[team2],

        theta=comparison_df['Metric'],

        fill='toself',

        name=team2,

        line=dict(color='orange')

    ))

    radar_fig.update_layout(

        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),

        showlegend=True,

        title='Team Radar Intelligence'
    )

    st.plotly_chart(
        radar_fig,
        use_container_width=True
    )

# ==========================================================
# OVERALL STATS
# ==========================================================

elif page == "Stats":

    st.header(
        "📊 Overall IPL Statistics"
    )

    # ======================================================
    # TEAM POINTS TABLE
    # ======================================================

    st.subheader(
        "🏆 IPL Points Table"
    )

    points_table = (

        matches['match_winner']
        .value_counts()
        .reset_index()

    )

    points_table.columns = [
        'Team',
        'Wins'
    ]

    points_table['Points'] = (
        points_table['Wins'] * 2
    )

    points_table = points_table.sort_values(
        by='Points',
        ascending=False
    )

    c1, c2 = st.columns(2)

    c1.dataframe(
        points_table,
        use_container_width=True
    )

    fig1 = px.bar(

        points_table,

        x='Team',
        y='Points',

        color='Points',

        text='Points',

        title='IPL Points Table'
    )

    c2.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ======================================================
    # HIGHEST RUN SCORERS
    # ======================================================

    st.subheader(
        "🔥 Highest Run Scorers"
    )

    batting = (

        deliveries.groupby(
            ['striker', 'batting_team']
        )

        .agg(

            runs=('runs_of_bat', 'sum'),
            balls=('runs_of_bat', 'count')

        )

        .reset_index()

    )

    batting['strike_rate'] = (

        batting['runs']
        /
        batting['balls']

    ) * 100

    batting = batting.sort_values(
        by='runs',
        ascending=False
    ).head(10)

    c3, c4 = st.columns(2)

    c3.dataframe(
        batting,
        use_container_width=True
    )

    fig2 = px.bar(

        batting,

        x='striker',
        y='runs',

        color='strike_rate',

        text='runs',

        title='Highest Run Scorers'
    )

    c4.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ======================================================
    # TOP WICKET TAKERS
    # ======================================================

    st.subheader(
        "🎯 Top 10 Wicket Takers"
    )

    wickets = (

        deliveries[
            deliveries[
                'player_dismissed'
            ].notna()
        ]

        .groupby(
            ['bowler', 'bowling_team']
        )

        .size()

        .reset_index(name='wickets')

        .sort_values(
            by='wickets',
            ascending=False
        )

        .head(10)

    )

    c5, c6 = st.columns(2)

    c5.dataframe(
        wickets,
        use_container_width=True
    )

    fig3 = px.bar(

        wickets,

        x='bowler',
        y='wickets',

        color='wickets',

        text='wickets',

        title='Top Wicket Takers'
    )

    c6.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ======================================================
    # BEST BOWLING FIGURES
    # ======================================================

    st.subheader(
        "🔥 Best Bowling Figures"
    )

    bowling_figures = (

        deliveries[
            deliveries[
                'player_dismissed'
            ].notna()
        ]

        .groupby(
            ['bowler', 'bowling_team']
        )

        .agg(

            wickets=(
                'player_dismissed',
                'count'
            ),

            runs_given=(
                'runs_of_bat',
                'sum'
            )

        )

        .reset_index()

    )

    bowling_figures['figures'] = (

        bowling_figures['wickets']
        .astype(str)

        + "/"

        +

        bowling_figures['runs_given']
        .astype(str)

    )

    bowling_figures = bowling_figures.sort_values(

        by=['wickets', 'runs_given'],

        ascending=[False, True]

    ).head(10)

    c7, c8 = st.columns(2)

    c7.dataframe(

        bowling_figures[
            [
                'bowler',
                'bowling_team',
                'figures'
            ]
        ],

        use_container_width=True
    )

    fig4 = px.bar(

        bowling_figures,

        x='bowler',

        y='runs_given',

        color='wickets',

        text='figures',

        title='Best Bowling Figures'

    )

    c8.plotly_chart(
        fig4,
        use_container_width=True
    )

    # ======================================================
    # BOWLING AVERAGE
    # ======================================================

    st.subheader(
        "🎳 Best Bowling Average"
    )

    bowling_avg = wickets.copy()

    runs_given = (

        deliveries.groupby('bowler')
        ['runs_of_bat']
        .sum()

    )

    bowling_avg['runs_given'] = (
        bowling_avg['bowler']
        .map(runs_given)
    )

    bowling_avg['bowling_avg'] = (

        bowling_avg['runs_given']
        /
        bowling_avg['wickets']

    )

    bowling_avg = bowling_avg.sort_values(
        by='bowling_avg'
    ).head(10)

    c9, c10 = st.columns(2)

    c9.dataframe(

        bowling_avg[
            [
                'bowler',
                'bowling_team',
                'bowling_avg'
            ]
        ],

        use_container_width=True
    )

    fig5 = px.bar(

        bowling_avg,

        x='bowler',
        y='bowling_avg',

        color='bowling_avg',

        text='bowling_avg',

        title='Bowling Average'
    )

    c10.plotly_chart(
        fig5,
        use_container_width=True
    )

    # ======================================================
    # SIX HITTERS
    # ======================================================

    st.subheader(
        "🚀 Top Six Hitters"
    )

    sixes = (

        deliveries[
            deliveries['runs_of_bat']
            == 6
        ]

        .groupby(
            ['striker', 'batting_team']
        )

        .size()

        .reset_index(name='sixes')

        .sort_values(
            by='sixes',
            ascending=False
        )

        .head(10)

    )

    c11, c12 = st.columns(2)

    c11.dataframe(
        sixes,
        use_container_width=True
    )

    fig6 = px.bar(

        sixes,

        x='striker',
        y='sixes',

        color='sixes',

        text='sixes',

        title='Top Six Hitters'
    )

    c12.plotly_chart(
        fig6,
        use_container_width=True
    )

    # ======================================================
    # FOUR HITTERS
    # ======================================================

    st.subheader(
        "🏏 Top Four Hitters"
    )

    fours = (

        deliveries[
            deliveries['runs_of_bat']
            == 4
        ]

        .groupby(
            ['striker', 'batting_team']
        )

        .size()

        .reset_index(name='fours')

        .sort_values(
            by='fours',
            ascending=False
        )

        .head(10)

    )

    c13, c14 = st.columns(2)

    c13.dataframe(
        fours,
        use_container_width=True
    )

    fig7 = px.bar(

        fours,

        x='striker',
        y='fours',

        color='fours',

        text='fours',

        title='Top Four Hitters'
    )

    c14.plotly_chart(
        fig7,
        use_container_width=True
    )

    # ======================================================
    # BOUNDARY HITTERS
    # ======================================================

    st.subheader(
        "💥 Top Boundary Hitters"
    )

    boundaries = (

        deliveries[
            deliveries[
                'runs_of_bat'
            ].isin([4, 6])
        ]

        .groupby(
            ['striker', 'batting_team']
        )

        .size()

        .reset_index(name='boundaries')

        .sort_values(
            by='boundaries',
            ascending=False
        )

        .head(10)

    )

    c15, c16 = st.columns(2)

    c15.dataframe(
        boundaries,
        use_container_width=True
    )

    fig8 = px.bar(

        boundaries,

        x='striker',
        y='boundaries',

        color='boundaries',

        text='boundaries',

        title='Boundary Hitters'
    )

    c16.plotly_chart(
        fig8,
        use_container_width=True
    )

# ==========================================================
# TEAM STATS
# ==========================================================

elif page == "Team Stats":

    st.header(
        "📈 Team Wise Statistics"
    )

    selected_team = st.selectbox(
        "Select Team",
        teams
    )

    # ======================================================
    # TEAM MATCHES
    # ======================================================

    team_matches = matches[
        (
            matches['team1']
            == selected_team
        )
        |
        (
            matches['team2']
            == selected_team
        )
    ]

    match_ids = team_matches[
        'match_id'
    ].unique()

    team_deliveries = deliveries[
        deliveries['match_no']
        .isin(match_ids)
    ]

    # ======================================================
    # WIN LOSS
    # ======================================================

    st.subheader(
        "🏆 Win Loss Analysis"
    )

    wins = (
        team_matches['match_winner']
        == selected_team
    ).sum()

    losses = len(team_matches) - wins

    win_df = pd.DataFrame({

        'Result': [
            'Wins',
            'Losses'
        ],

        'Count': [
            wins,
            losses
        ]
    })

    c1, c2 = st.columns(2)

    c1.dataframe(
        win_df,
        use_container_width=True
    )

    fig1 = px.pie(
        win_df,
        names='Result',
        values='Count',
        title='Win Loss Ratio'
    )

    c2.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ======================================================
    # TOP 5 RUN SCORERS
    # ======================================================

    st.subheader(
        "🔥 Top 5 Run Scorers"
    )

    batting = (

        team_deliveries.groupby(
            ['striker', 'batting_team']
        )

        .agg(

            runs=('runs_of_bat', 'sum'),

            balls=('runs_of_bat', 'count')

        )

        .reset_index()

    )

    batting['strike_rate'] = (

        batting['runs']
        /
        batting['balls']

    ) * 100

    batting = batting.sort_values(
        by='runs',
        ascending=False
    ).head(5)

    c3, c4 = st.columns(2)

    c3.dataframe(
        batting,
        use_container_width=True
    )

    fig2 = px.bar(
        batting,
        x='striker',
        y='runs',
        color='strike_rate',
        text='runs',
        title='Top Run Scorers'
    )

    c4.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ======================================================
    # TOP 5 BOUNDARY HITTERS
    # ======================================================

    st.subheader(
        "💥 Top 5 Boundary Hitters"
    )

    boundaries = (

        team_deliveries[
            team_deliveries[
                'runs_of_bat'
            ].isin([4, 6])
        ]

        .groupby(
            ['striker', 'batting_team']
        )

        .size()

        .reset_index(name='boundaries')

        .sort_values(
            by='boundaries',
            ascending=False
        )

        .head(5)

    )

    c5, c6 = st.columns(2)

    c5.dataframe(
        boundaries,
        use_container_width=True
    )

    fig3 = px.bar(
        boundaries,
        x='striker',
        y='boundaries',
        color='boundaries',
        text='boundaries',
        title='Top Boundary Hitters'
    )

    c6.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ======================================================
    # TOP 5 WICKET TAKERS
    # ======================================================

    st.subheader(
        "🎯 Top 5 Wicket Takers"
    )

    wickets = (

        team_deliveries[
            team_deliveries[
                'player_dismissed'
            ].notna()
        ]

        .groupby(
            ['bowler', 'bowling_team']
        )

        .size()

        .reset_index(name='wickets')

        .sort_values(
            by='wickets',
            ascending=False
        )

        .head(5)

    )

    c7, c8 = st.columns(2)

    c7.dataframe(
        wickets,
        use_container_width=True
    )

    fig4 = px.bar(
        wickets,
        x='bowler',
        y='wickets',
        color='wickets',
        text='wickets',
        title='Top Wicket Takers'
    )

    c8.plotly_chart(
        fig4,
        use_container_width=True
    )

    # ======================================================
    # TOP 5 BOWLING AVERAGE
    # ======================================================

    st.subheader(
        "🎳 Top 5 Bowling Average"
    )

    bowling_avg = wickets.copy()

    runs_given = (

        team_deliveries.groupby('bowler')
        ['runs_of_bat']
        .sum()

    )

    bowling_avg['runs_given'] = (
        bowling_avg['bowler']
        .map(runs_given)
    )

    bowling_avg['bowling_avg'] = (

        bowling_avg['runs_given']
        /
        bowling_avg['wickets']

    )

    bowling_avg = bowling_avg.sort_values(
        by='bowling_avg'
    ).head(5)

    c9, c10 = st.columns(2)

    c9.dataframe(

        bowling_avg[
            [
                'bowler',
                'bowling_team',
                'bowling_avg'
            ]
        ],

        use_container_width=True
    )

    fig5 = px.bar(
        bowling_avg,
        x='bowler',
        y='bowling_avg',
        color='bowling_avg',
        text='bowling_avg',
        title='Top Bowling Average'
    )

    c10.plotly_chart(
        fig5,
        use_container_width=True
    )


# ==========================================================
# LIVE MATCH SIMULATION
# ==========================================================

elif page == "Live Match Simulation":

    st.header(
        "📡 Live Match Simulation"
    )

    placeholder = st.empty()

    if st.button(
        "Start Simulation"
    ):

        history = []

        for data in simulate_live_match():

            history.append(
                data['score']
            )

            with placeholder.container():

                c17, c18, c19 = st.columns(3)

                c17.metric(
                    "Score",
                    f"{data['score']}/{data['wickets']}"
                )

                c18.metric(
                    "Overs",
                    data['over']
                )

                c19.metric(
                    "Run Rate",
                    round(
                        data['score']
                        /
                        (
                            float(data['over'])
                            + 1
                        ),
                        2
                    )
                )

                momentum_df = pd.DataFrame({

                    'Ball': list(
                        range(
                            1,
                            len(history) + 1
                        )
                    ),

                    'Runs': history

                })

                fig7 = px.line(
                    momentum_df,
                    x='Ball',
                    y='Runs',
                    markers=True
                )

                st.plotly_chart(
                    fig7,
                    use_container_width=True
                )

#streamlit run dashboard/app.py