import requests
import os


# --- Strava API Setup ---
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")  # Use os.getenv() for environment variables
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")



# --- Refresh Strava Access Token ---
url = "https://www.strava.com/oauth/token"
payload = {
    "client_id": STRAVA_CLIENT_ID,
    "client_secret": STRAVA_CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": STRAVA_REFRESH_TOKEN
}
response = requests.post(url, data=payload)
access_token = response.json().get("access_token")




def fetch_strava_segments(bounds, activity_type):
    url = "https://www.strava.com/api/v3/segments/explore"
    params = {
        "bounds": ",".join(map(str, bounds)),
        "activity_type": activity_type,
        "min_cat": 0,
        "max_cat": 5
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

