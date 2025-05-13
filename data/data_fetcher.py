from data.strava_api import fetch_strava_segments
from data.osm_api import fetch_osm_data
import os
import pandas as pd

class DataFetcher:
    def __init__(self, bounds, sub_bounds, activity_type, use_cached=True):
        self.bounds = bounds
        self.sub_bounds = sub_bounds    
        self.activity_type = activity_type
        self.use_cached = use_cached
        self.data_path = f"cache/strava_segments_{activity_type}.parquet"

    def fetch_data(self):
        """Fetch Strava segments and OSM data."""
        strava_data = self._fetch_strava_segments()
        osm_data = fetch_osm_data(self.bounds)
        return strava_data, osm_data

    def _fetch_strava_segments(self):
        """Fetch Strava segments and return a DataFrame."""

        # Check if cached data exists and load it
        if self.use_cached and os.path.exists(self.data_path):
            print("📂 Lade Strava-Daten aus Cache-Datei...")
            df = pd.read_parquet(self.data_path)
            return df.to_dict(orient="records")  # <- Liste von Dicts

        # If no cached data, fetch from Strava API
        print("🌐 Rufe Strava API auf...")
        all_segments = []
        seen_ids = set()
        for bounding_box in self.sub_bounds:
            segments_response = fetch_strava_segments(bounding_box, self.activity_type)
            for seg in segments_response.get("segments", []):
                if seg["id"] not in seen_ids:
                    seen_ids.add(seg["id"])
                    all_segments.append(seg)

        # Process the segments into a DataFrame in case of API call
        df = pd.DataFrame(all_segments)
        os.makedirs("cache", exist_ok=True)
        df.to_parquet(self.data_path)
        print(f"💾 Gespeichert unter {self.data_path}")
        return df