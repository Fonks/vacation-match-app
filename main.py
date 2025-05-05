import streamlit as st
from user_input import geocode_city, create_bounding_box
from strava_api import fetch_strava_segments, decode_polyline
from streamlit_folium import st_folium
import folium

st.title("🏃‍♂️ VacationMatch: Sport Segment Explorer")

# User inputs
city = st.text_input("Enter a city", "Aschaffenburg")
radius = st.slider("Select radius (km)", 1, 30, 10)
activity_type = st.selectbox("Choose activity type", ["running", "riding"])

# Access token placeholder
access_token = st.text_input("Enter your Strava API Access Token", type="password")

if st.button("Explore Segments"):
    try:
        lat, lon = geocode_city(city)
        bounds = create_bounding_box(lat, lon, radius)
        segments = fetch_strava_segments(bounds, activity_type, access_token)
        
        if "segments" in segments and segments["segments"]:
            st.success(f"Found {len(segments['segments'])} segments!")
            
            # Initialize folium map
            fmap = folium.Map(location=[lat, lon], zoom_start=13)

            for seg in segments["segments"]:
                st.subheader(seg["name"])
                st.write(f"Distance: {seg['distance']} m")
                st.write(f"Average grade: {seg['avg_grade']}%")

                try:
                    coords = decode_polyline(seg["polyline"])
                    folium.PolyLine(locations=coords, color="blue", weight=3).add_to(fmap)
                except Exception as e:
                    st.warning(f"Could not decode polyline: {e}")

            st_data = st_folium(fmap, width=700, height=500)
        else:
            st.warning("No segments found or invalid token.")
    except Exception as e:
        st.error(f"Error: {e}")
