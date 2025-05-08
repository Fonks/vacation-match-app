# vacation_match_app/main.py

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from vacation_match_app.ui.sidebar import display_sidebar
from vacation_match_app.data.fetcher import fetch_strava_segments, fetch_osm_pois
from vacation_match_app.data.geo_utils import geocode_city, get_bounding_box
from vacation_match_app.map.visualizer import render_map
from vacation_match_app.domain.filters import filter_data_for_map_strava, filter_data_for_map_osm, filter_data_for_table

# Set up custom styling for Streamlit UI
st.markdown("""
    <style>
    html, body, .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #e6f2e6;
        color: #1a331a;
    }
    .stApp {
        padding: 2rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #d4ecd4;
        color: #1a331a;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar - User Input
# ----------------------------

selected_cities, sportart, selected_poi_types, map_city = display_sidebar()

# ----------------------------
# API-Datenabruf
# ----------------------------

if selected_cities:
    try:
        # Geokoordinaten und Bounding Boxes abrufen
        city_coords = {city: geocode_city(city) for city in selected_cities}
        bounds = {city: get_bounding_box(city) for city in selected_cities}

        # Strava-Segmente und OSM-POIs abrufen
        strava_data = {
            city: fetch_strava_segments(bounds[city], sportart.lower()) for city in selected_cities
        }

        osm_data = {}
        for city in selected_cities:
            south, west, north, east = bounds[city]
            osm_data[city] = fetch_osm_pois(south, west, north, east, selected_poi_types)

        # ----------------------------
        # Daten filtern
        # ----------------------------

        filtered_segments = filter_data_for_map_strava(strava_data, map_city)
        filtered_pois_map = filter_data_for_map_osm(osm_data, selected_poi_types, map_city)
        filtered_pois_table = filter_data_for_table(osm_data, selected_poi_types, selected_cities)

        # ----------------------------
        # Hauptbereich
        # ----------------------------

        st.title("🏃‍♂️ Vacation Match: Dein Städtevergleich & Karte")

        st.subheader(f"🗺️ Karte von {map_city}")
        render_map(
            lat=city_coords[map_city][0],
            lon=city_coords[map_city][1],
            segments=filtered_segments,
            pois=filtered_pois_map
        )

        st.subheader("📋 Vergleichstabelle: POIs in gewählten Städten")
        st.dataframe(filtered_pois_table)

        st.subheader(f"📌 POIs in {map_city}")
        st.dataframe(filtered_pois_map)

    except Exception as e:
        st.error(f"Es gab einen Fehler beim Abrufen der Daten: {e}")
else:
    st.warning("Bitte gib mindestens eine Stadt ein.")
