from data.strava_api import fetch_strava_segments
from data.osm_api import fetch_osm_data
import os
import json
import pandas as pd

class DataFetcher:
    def __init__(self, bounds, sub_bounds, activity_type, use_cached=True):
        self.bounds = bounds
        self.sub_bounds = sub_bounds    
        self.activity_type = activity_type
        self.use_cached = use_cached
        self.data_path = f"cache/strava_segments_{activity_type}.json"  # JSON für Cache mit Metadaten

    def fetch_data(self):
        """Fetch Strava segments and OSM data."""
        strava_data = self._fetch_strava_segments()
        osm_data = fetch_osm_data(self.bounds)
        return strava_data, osm_data

    def _fetch_strava_segments(self):
        """Fetch Strava segments intelligently using cache."""
        os.makedirs("cache", exist_ok=True)
        all_segments = []
        seen_ids = set()
        cache = {"segments": [], "bounds": []}

        # Cache laden, falls vorhanden
        if self.use_cached and os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                cache = json.load(f)
            print("📂 Vorhandene Cache-Datei geladen.")

        # Prüfen, welche Sub-Bounds noch nicht gecacht wurden
        for bbox in self.sub_bounds:
            if not self._is_bbox_cached(cache["bounds"], bbox):
                print(f"🌐 Rufe Strava API auf für Bereich: {bbox}")
                response = fetch_strava_segments(bbox, self.activity_type)
                new_segments = response.get("segments", [])
                for seg in new_segments:
                    if seg["id"] not in {s["id"] for s in cache["segments"]}:
                        cache["segments"].append(seg)
                cache["bounds"].append(bbox)

        # Cache aktualisieren
        with open(self.data_path, "w") as f:
            json.dump(cache, f)
        print(f"💾 Cache aktualisiert unter {self.data_path}")

        # Nur Segmente zurückgeben, die in aktuellen sub_bounds liegen
        for seg in cache["segments"]:
            start = seg.get("start_latlng")
            if start:
                for bbox in self.sub_bounds:
                    if self._bbox_contains(bbox, start):
                        if seg["id"] not in seen_ids:
                            seen_ids.add(seg["id"])
                            all_segments.append(seg)
                        break  # Nur einmal pro Segment prüfen

        return all_segments  # Als Liste von Dicts zurückgeben

    def _is_bbox_cached(self, cached_bounds, bbox):
        """Check if a bounding box is already in the cache."""
        return any(bbox == cached_bbox for cached_bbox in cached_bounds)

    def _bbox_contains(self, bbox, point):
        """Check if a point is inside a bounding box."""
        south, west, north, east = bbox
        lat, lon = point
        return south <= lat <= north and west <= lon <= east
