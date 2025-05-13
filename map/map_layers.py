import pydeck as pdk
import pandas as pd
import streamlit as st

class MapLayer:
    @staticmethod
    def create_layers(coords, strava_list, polyline_paths, osm_data_cache, selected_osm_ids):
        """Create PyDeck layers for Strava data and OSM POIs."""
        
        osm_elements = osm_data_cache.get("elements", [])
        
        if osm_elements:
            poi_df = pd.DataFrame(osm_elements)
            print("Spalten im POI-DataFrame:", poi_df.columns)

            # ID-Spalte bestimmen
            id_column = "@id" if "@id" in poi_df.columns else "id" if "id" in poi_df.columns else None

            # Extrahiere numerische IDs aus z.B. "node_12345" oder "way_67890"
            selected_ids = {
                int(id_str.split("_")[1]) for id_str in selected_osm_ids if "_" in id_str and id_str.split("_")[1].isdigit()
            }
            print("Gefilterte POI-IDs:", selected_ids)

            if id_column:
                poi_df = poi_df[poi_df[id_column].isin(selected_ids)]

                poi_df["lat"] = poi_df.apply(
                    lambda row: row["lat"] if pd.notnull(row.get("lat")) else (
                        row["center"]["lat"] if isinstance(row.get("center"), dict) and "lat" in row["center"] else None
                    ),
                    axis=1
                )
                poi_df["lon"] = poi_df.apply(
                    lambda row: row["lon"] if pd.notnull(row.get("lon")) else (
                        row["center"]["lon"] if isinstance(row.get("center"), dict) and "lon" in row["center"] else None
                    ),
                    axis=1
                )

                poi_df = poi_df.dropna(subset=["lat", "lon"])
                print("POIs mit Koordinaten:", poi_df[["lat", "lon"]].head())

                poi_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=poi_df,
                    get_position='[lon, lat]',
                    get_fill_color='[0, 0, 255, 160]',
                    get_radius=30,
                    pickable=True
                )

            else:
                print("Keine gültige ID-Spalte gefunden.")
                poi_layer = None
        else:
            print("Keine OSM-Elemente gefunden.")
            poi_layer = None

        # Strava-Daten
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
            get_fill_color='[255, 0, 0, 160]',
            get_radius=30,
            pickable=True
        )

        strava_paths = pdk.Layer(
            "PathLayer",
            data=polyline_paths,
            get_path="path",
            get_width=20,
            get_color=[255, 0, 0],
            opacity=0.6,
            pickable=True
        )

        layers = [strava_scatter, strava_paths]
        if poi_layer:
            layers.append(poi_layer)

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=13,
            pitch=0
        )

        return layers, view_state
