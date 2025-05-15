import pydeck as pdk
import pandas as pd
from ui.constants import POI_CATEGORIES  # Import POI_CATEGORIES
from data.osm_api import fetch_osm_data, group_osm_tags



class MapLayer:
    @staticmethod
    def create_layers(coords, strava_list, polyline_paths, osm_data_cache, selected_osm_ids, zoom_level=13):
        """Create PyDeck layers for Strava data and OSM POIs."""
        
        # === OSM Data Processing ===
        osm_elements = osm_data_cache.get("elements", [])
        poi_data = []

        # Define color mapping for categories
        category_colors = {
            "🍽️ Essen & Trinken": [0, 128, 255],  # Blue
            "🚻 Hygiene & Sanitär": [102, 204, 0],  # Green
            "🛒 Einkauf & Versorgung": [255, 0, 0],  # Red
            "🩺 Gesundheit": [247, 199, 40],  # Yellow
            "🎓 Bildung & Kultur": [255, 0, 127],  # Magenta
            "🏛️ Öffentliche Dienste": [0, 255, 255],  # Cyan
            "📡 Kommunikation & Technik": [128, 0, 128],  # Purple
            "🚗 Verkehr & Mobilität": [255, 165, 0],  # Orange
            "🧸 Betreuung & Soziales": [128, 128, 0],  # Olive
            "🎉 Freizeit & Unterhaltung": [0, 128, 128],  # Teal
            "🪑 Ruhe & Infrastruktur": [128, 128, 128],  # Gray
        }

        for el in osm_elements:
            # Extract coordinates
            lat = el.get("lat") or (el.get("center", {}).get("lat") if el.get("center") else None)
            lon = el.get("lon") or (el.get("center", {}).get("lon") if el.get("center") else None)

            # Skip if no coordinates
            if not lat or not lon:
                continue

            # Extract amenity tag and name
            tags = el.get("tags", {})
            amenity = tags.get("amenity", "Unknown")
            name = tags.get("name", "Unnamed")

            # Check if the amenity belongs to one of the categories
            category = next(
                (cat for cat, types in POI_CATEGORIES.items() if amenity in types),
                None
            )

            # Skip if the amenity does not belong to any category
            if category is None:
                continue

            # Skip if the name is "Unnamed"
            if name == "Unnamed":
                continue

            # Add the category under the name
            name = f"{name} \n ({category})"

            # Add to POI data
            poi_data.append({
                "lat": lat,
                "lon": lon,
                "amenity": amenity,
                "name": name,
                "category": category,
                "color": category_colors.get(category, [0, 0, 0])  # Default to black if no color is found
            })

        # Convert to DataFrame
        poi_df = pd.DataFrame(poi_data)

        # Calculate size scale based on zoom level
        def calculate_size_scale(zoom):
            # Adjust the multiplier as needed for your map
            return max(1, 20 / zoom)

        size_scale = calculate_size_scale(zoom_level)

        # Create a ScatterplotLayer for OSM POIs
        poi_layer = pdk.Layer(
            "ScatterplotLayer",
            data=poi_df,
            get_position='[lon, lat]',
            get_fill_color='color',  # Use the color column for color coding
            get_radius=5 * size_scale,  # Adjust radius dynamically
            opacity=0.8,
            pickable=True
        )

        # === Strava Data Processing ===
        lats = [c[0] for c in coords]
        lons = [c[1] for c in coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        strava_scatter = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame({
                "lat": lats,
                "lon": lons,
                "name": [s["Name"] for s in strava_list]
            }),
            get_position='[lon, lat]',
            get_fill_color='[255, 178, 102]',  # Orange for Strava points
            get_radius=13 * size_scale,  # Adjust radius dynamically
            pickable=True
        )

        strava_paths = pdk.Layer(
            "PathLayer",
            data=polyline_paths,
            get_path="path",
            get_width=5,
            get_color=[255, 128, 0],  # Orange for paths
            opacity=0.6,
            pickable=True
        )

        # Combine layers
        layers = [poi_layer, strava_scatter, strava_paths]

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom_level,  # Pass the zoom level
            pitch=0
        )

        return layers, view_state









