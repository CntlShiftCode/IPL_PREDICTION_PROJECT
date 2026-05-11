


#API_KEY = "8551b1c7-ecfa-4a64-a8ba-0a254fb56ff7"


import requests


# ==========================================================
# ADD YOUR API KEY
# ==========================================================

API_KEY = "8551b1c7-ecfa-4a64-a8ba-0a254fb56ff7"


# ==========================================================
# GET LIVE MATCHES
# ==========================================================

def get_live_matches():

    url = "https://api.cricapi.com/v1/currentMatches"

    params = {

        "apikey": API_KEY,

        "offset": 0

    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=10

        )

        data = response.json()

        if data.get('status') != "success":

            return []

        return data.get('data', [])

    except Exception as e:

        print(e)

        return []


# ==========================================================
# FILTER IPL MATCHES
# ==========================================================

def get_ipl_matches():

    matches = get_live_matches()

    ipl_matches = []

    for match in matches:

        series = str(

            match.get(
                'series',
                ''
            )

        )

        if 'IPL' in series.upper():

            teams = match.get(
                'teams',
                ['Team 1', 'Team 2']
            )

            ipl_matches.append({

                'Team 1':
                teams[0],

                'Team 2':
                teams[1],

                'Status':
                match.get(
                    'status',
                    'No Status'
                ),

                'Venue':
                match.get(
                    'venue',
                    'Unknown Venue'
                )

            })

    return ipl_matches