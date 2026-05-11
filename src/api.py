import requests

API_KEY = "YOUR_API_KEY"


def get_live_match():

    url = "https://api.cricapi.com/v1/currentMatches"

    params = {
        'apikey': API_KEY,
        'offset': 0
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        data = response.json()
        if data.get('status') != 'success':
            return None

        for match in data.get('data', []):
            if 'IPL' in match.get('series', ''):
                return {
                    'team1': match['teams'][0],
                    'team2': match['teams'][1],
                    'score': match.get('score', 'N/A')
                }

    except Exception as e:
        print(e)

    return None
