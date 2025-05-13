import requests


class PreProcessor:

    ## === Was alles in der Klasse enthalten ist ===
    # Initialisierung der Klasse
    def __init__(self, city, radius):
        self.city = city
        self.radius = radius
        self.lat_radius = None
        self.lon_radius = None
        self.bounds = None
        self.sub_bounds = None
        self.rows = 2 # split the map/bounds 
        self.cols = 2 # split the map/bounds 


    def geocode_city(self):
        """
        Accepts a city name string.
        Returns latitude and longitude as floats.
        """

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": self.city,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "vacation-match-app/1.0"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            self.lat_radius = float(data[0]["lat"])
            self.lon_radius = float(data[0]["lon"])
            return self.lat_radius, self.lon_radius
        else:
            raise ValueError(f"City not found: {self.city}")
            

    # == Hier wird die Funktion create_bounding_box definiert, um eine Bounding Box zu erstellen ==

    def create_bounding_box(self):
        """
        Returns a bounding box around (lat, lon) with radius_km.
        Format: [south, west, north, east]
        """
        delta = self.radius / 111  # Roughly 1° latitude ~ 111 km
        self.bounds = [self.lat_radius - delta, self.lon_radius - delta, self.lat_radius + delta, self.lon_radius + delta]
        print(f"Bounding box pre: {self.bounds}")
        return self.bounds


    # == Hier wird die Funktion split_bounds definiert, um die bounds in kleinere Bereiche zu unterteilen ==

    def split_bounds(self):
        print(f"Bounding box: {self.bounds}")
        south, west, north, east = self.bounds
        lat_step = (north - south) / self.rows
        lon_step = (east - west) / self.cols

        self.sub_bounds = []
        for i in range(self.rows):
            for j in range(self.cols):
                sub_south = south + i * lat_step
                sub_north = sub_south + lat_step
                sub_west = west + j * lon_step
                sub_east = sub_west + lon_step
                self.sub_bounds.append([sub_south, sub_west, sub_north, sub_east])
        return self.sub_bounds