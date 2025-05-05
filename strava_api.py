import requests
import polyline

def fetch_strava_segments(bounds, activity_type, access_token):
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

def decode_polyline(encoded_str):
    return polyline.decode(encoded_str)
