# vacation_match_app/domain/segment.py

# kapselt die Datenstrukturen und Logik für Strava-Segmente

class Segment:
    def __init__(self, segment_id, name, lat, lon, city, activity_type, surface):
        self.id = segment_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.city = city
        self.activity_type = activity_type
        self.surface = surface

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "city": self.city,
            "activity_type": self.activity_type,
            "surface": self.surface
        }

def filter_segments(segments, city=None, activity=None, surfaces=None):
    """
    Filtert eine Liste von Segmenten nach Stadt, Aktivität und Oberfläche.
    """
    return [
        seg for seg in segments
        if (city is None or seg.city == city)
        and (activity is None or seg.activity_type == activity)
        and (surfaces is None or seg.surface in surfaces)
    ]
