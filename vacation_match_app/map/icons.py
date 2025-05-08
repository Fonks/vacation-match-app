# vacation_match_app/map/icons.py

# Ordnet POI-Typen passende Icons (Farben oder Symbole) zu, damit sie auf der Karte 
# visuell unterschieden werden können. Optional kann dies später erweitert werden für IconLayer statt nur Farben.


def get_poi_color(poi_type: str) -> list:
    """
    Gibt eine RGBA-Farbe basierend auf dem POI-Typ zurück.
    """
    color_map = {
        "cafe": [255, 140, 0, 160],        # orange
        "park": [0, 128, 0, 160],          # grün
        "viewpoint": [70, 130, 180, 160],  # stahlblau
        "toilets": [75, 0, 130, 160],      # indigoblau
        "restaurant": [255, 0, 0, 160],    # rot
    }
    return color_map.get(poi_type, [100, 100, 100, 160])  # grau als Default


def get_icon_name(poi_type: str) -> str:
    """
    Gibt einen Symbolnamen zurück (für IconLayer oder Tooltips).
    """
    icon_map = {
        "cafe": "coffee",
        "park": "tree",
        "viewpoint": "eye",
        "toilets": "restroom",
        "drinking_water": "tint",
        "restaurant": "utensils",
        "bench": "chair",
        "shelter": "home",
        # ...
    }
    return icon_map.get(poi_type, "map-marker")



