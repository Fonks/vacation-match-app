# This module will handle OSM queries, e.g. via Overpass API
# Developer note: Requires implementation using Overpass API or another OSM source

import requests

def fetch_osm_data(bounding_box):
    """
    Fetch all OSM elements with an 'amenity' tag within the given bounding box.
    
    bounding_box: tuple in the format (south, west, north, east)
    Returns: JSON response from Overpass API
    """
    west, south, east, north = bounding_box[1], bounding_box[0], bounding_box[3], bounding_box[2]
    url = "https://overpass-api.de/api/interpreter"

    # Overpass QL query
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"]({south},{west},{north},{east});
      way["amenity"]({south},{west},{north},{east});
      relation["amenity"]({south},{west},{north},{east});
    );
    out center;
    """

    headers = {
        "User-Agent": "vacation-match-app/1.0"
    }

    response = requests.post(url, data={"data": query}, headers=headers)
    response.raise_for_status()
    return response.json()

def group_osm_tags(osm_elements):
    # Mapping von OSM-Tags in Kategorien
    categories = {
        "Food & Drink": {
            "restaurant", "cafe", "fast_food", "pub", "bar", "ice_cream", "biergarten", "bbq", "hookah_lounge"
        },
        "Health & Medical": {
            "doctors", "dentist", "pharmacy", "clinic", "hospital", "first_aid_school"
        },
        "Mobility & Transport": {
            "parking", "bicycle_parking", "motorcycle_parking", "car_rental", "car_wash",
            "parking_entrance", "bus_station", "taxi", "car_sharing", "charging_station",
            "bicycle_rental", "vehicle_inspection"
        },
        "Leisure & Culture": {
            "theatre", "cinema", "music_venue", "arts_centre", "studio", "community_centre",
            "nightclub", "events_venue", "clubhouse", "dancing_school", "dojo", "casino", "gambling"
        },
        "Nature & Relaxation": {
            "bench", "fountain", "lounger", "shelter", "telescope", "kneipp_water_cure"
        },
        "Public Services & Safety": {
            "fire_station", "police", "rescue_station", "townhall", "courthouse", "prison",
            "social_facility", "nursing_home", "animal_shelter", "waste_disposal", "waste_transfer_station"
        },
        "Education": {
            "school", "kindergarten", "university", "college", "language_school", "music_school", "driving_school"
        },
        "Spiritual & Memorial": {
            "place_of_worship", "monastery", "grave_yard"
        },
        "Shopping & Everyday Needs": {
            "vending_machine", "atm", "post_box", "post_office", "marketplace", "parcel_locker",
            "give_box", "letter_box", "locker", "luggage_locker", "public_bookcase"
        },
        "Sanitation & Water": {
            "toilets", "drinking_water", "shower", "water_point", "sanitary_dump_station"
        },
        "Other / Infrastructure": {
            "recycling", "waste_basket", "grit_bin", "bell", "clock", "traffic_park", "trolley_bay",
            "building_yard", "weighbridge", "photo_booth", "post_depot", "public_building"
        }
    }

    # Ergebnisstruktur
    grouped = {category: [] for category in categories}

    # Gruppiere OSM-Objekte anhand ihres "amenity"-Tags
    for element in osm_elements:
        tag = element.get("tags", {}).get("amenity")
        if not tag:
            continue
        for category, tags in categories.items():
            if tag in tags:
                grouped[category].append(element)
                break

    # Filter leere Kategorien
    grouped = {k: v for k, v in grouped.items() if v}
    return grouped

