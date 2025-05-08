# vacation_match_app/domain/poi.py

# kapselt die Datenstrukturen und Logik für POIs

from collections import defaultdict

class POI:
    def __init__(self, poi_id, name, lat, lon, city, poi_type):
        self.id = poi_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.city = city
        self.type = poi_type

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "city": self.city,
            "type": self.type
        }

def group_pois_by_category(pois):
    """
    Gruppiert POIs in Kategorien wie 'Essen & Trinken', 'Verkehr', 'Gesundheit', etc.

    Returns:
        dict: {"Essen & Trinken": [POI, POI], ...}
    """
    categories = defaultdict(list)

    category_map = {
        "cafe": "Essen & Trinken",
        "restaurant": "Essen & Trinken",
        "fast_food": "Essen & Trinken",
        "bar": "Essen & Trinken",
        "pub": "Essen & Trinken",
        "ice_cream": "Essen & Trinken",
        "viewpoint": "Natur & Aussicht",
        "park": "Natur & Aussicht",
        "fountain": "Natur & Aussicht",
        "drinking_water": "Versorgung",
        "toilets": "Versorgung",
        "atm": "Geld & Bank",
        "bank": "Geld & Bank",
        "hospital": "Gesundheit",
        "clinic": "Gesundheit",
        "pharmacy": "Gesundheit",
        "police": "Sicherheit",
        "fire_station": "Sicherheit",
        "bus_station": "Verkehr",
        "parking": "Verkehr",
        "bicycle_parking": "Verkehr",
        "car_rental": "Verkehr",
        "train_station": "Verkehr"
        # ...weitere mappings möglich
    }

    for poi in pois:
        group = category_map.get(poi.type, "Sonstige")
        categories[group].append(poi)

    return dict(categories)
