import pandas as pd
import polyline


class DataProcessor:
    @staticmethod
    def process_strava_data(strava_segments):
        """Process Strava segments into a DataFrame and visualization data."""
        strava_list = []
        coords = []
        polyline_paths = []

        for seg in strava_segments:
            start = seg.get("start_latlng")
            if start is not None and len(start) == 2:
                coords.append(start)

            strava_list.append({
                "Name": seg.get("name"),
                "Distance (m)": round(seg.get("distance", 0), 1),
                "Avg Grade (%)": seg.get("avg_grade"),
                "Elevation Difference": seg.get("elev_difference"),
                "Start Lat/Lon": start,
                "End Lat/Lon": seg.get("end_latlng")
            })

            polyline_str = seg.get("points")
            if polyline_str:
                decoded = polyline.decode(polyline_str)
                path = [[lon, lat] for lat, lon in decoded]
                polyline_paths.append({
                    "name": seg.get("name", "Unnamed Segment"),
                    "path": path
                })

        return pd.DataFrame(strava_list), coords, polyline_paths