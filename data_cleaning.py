# data_cleaning.py

def clean_osm_data(osm_data, relevant_amenities=None):
    if relevant_amenities is None:
        relevant_amenities = ["cafe", "drinking_water", "toilets", "viewpoint"]

    cleaned = []
    for el in osm_data.get("elements", []):
        tags = el.get("tags", {})
        amenity = tags.get("amenity")
        if amenity not in relevant_amenities:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat and lon:
            cleaned.append({
                "Type": el.get("type"),
                "Amenity": amenity,
                "Name": tags.get("name", "n/a"),
                "Lat": lat,
                "Lon": lon
            })
    return cleaned

def clean_strava_segments(segment_data, min_distance=100.0, max_grade=20.0):
    cleaned = []
    for seg in segment_data.get("segments", []):
        dist = seg.get("distance", 0)
        grade = abs(seg.get("avg_grade", 0))
        if dist < min_distance or grade > max_grade:
            continue
        cleaned.append(seg)
    return cleaned
