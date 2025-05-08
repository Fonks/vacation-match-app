# vacation_match_app/data/strava_api.py

import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

TOKEN_URL = "https://www.strava.com/oauth/token"
EXPLORER_URL = "https://www.strava.com/api/v3/segments/explore"

_access_token = None


def get_strava_token():
    """
    Refresh and return a valid Strava access token.
    """
    global _access_token
    if _access_token:
        return _access_token

    response = requests.post(TOKEN_URL, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": STRAVA_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    })

    if response.status_code == 200:
        _access_token = response.json().get("access_token")
        return _access_token
    else:
        logging.error(f"Failed to refresh Strava token: {response.text}")
        raise RuntimeError("Strava authentication failed")


def fetch_strava_segments(bounds: list, activity_type="running"):
    """
    Fetch segments from Strava's Segment Explorer API.

    Args:
        bounds (list): Bounding box in the form [south, west, north, east].
        activity_type (str): 'running' or 'riding'.

    Returns:
        list: List of segments.
    """
    token = get_strava_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "bounds": ",".join(map(str, bounds)),
        "activity_type": activity_type
    }

    response = requests.get(EXPLORER_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("segments", [])
    else:
        logging.error(f"Failed to fetch segments: {response.text}")
        return []
