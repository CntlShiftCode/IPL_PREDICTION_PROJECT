from fastapi import FastAPI
from pydantic import BaseModel

from src.data_loader import load_data
from src.preprocessing import clean_data
from src.feature_engineering import create_features
from src.model import train_model, predict_match

app = FastAPI()

matches, deliveries = load_data()
matches, deliveries = clean_data(matches, deliveries)
features, deliveries = create_features(
    matches,
    deliveries
)

model = train_model(features)


class MatchRequest(BaseModel):
    team1: str
    team2: str
    venue: str
    toss_winner: str


@app.get('/')
def home():
    return {
        'message': 'IPL API Running'
    }

@app.post('/predict')
def predict(data: MatchRequest):

    team1_rate = 0.55
    team2_rate = 0.50
    venue_popularity = 20

    result = predict_match(
    model,
    data.team1,
    data.team2,
    data.venue,
    data.toss_winner
    )

    return result



#streamlit run dashboard/app.py