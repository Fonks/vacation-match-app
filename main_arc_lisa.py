import streamlit as st
import pandas as pd
import pydeck as pdk

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Allgemeine Schrift & Layout */
    html, body, .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #e6f2e6;
        color: #1a331a;
    }

    .stApp {
        padding: 2rem;
    }

    /* Zentrierte Titel und Texte */
    h1, h2, h3, p, .markdown-text-container {
        text-align: center;
    }

    /* Sidebar-Hintergrund */
    section[data-testid="stSidebar"] {
        background-color: #d4ecd4;
        color: #1a331a;
    }

    /* Sidebar-Labels */
    label[data-testid="stWidgetLabel"] {
        color: #1a331a !important;
    }

    /* Auswahlrahmen und Fokusgrün */
    div[data-baseweb="select"] > div {
        border-color: #2d572c !important;
    }

    div[data-baseweb="select"]:hover > div {
        border-color: #2d572c !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: #2d572c !important;
        box-shadow: 0 0 0 0.2rem rgba(45, 87, 44, 0.25) !important;
    }

    /* ✅ Multiselect-Tags (Chips) dunkelgrün */
    div[data-baseweb="tag"] {
        background-color: #2d572c !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        border: none !important;
    }

    /* X-Icon in Chips */
    div[data-baseweb="tag"] svg {
        fill: white !important;
        color: white !important;
    }

    /* Hover-Effekt für Chips */
    div[data-baseweb="tag"]:hover {
        background-color: #244722 !important;
    }

    /* Checkbox, Slider, Radio (aktiv) */
    .stSlider > div[data-testid="stTickBar"],
    .stCheckbox > div > div,
    .stRadio > div > label > div {
        accent-color: #2d572c;
    }

    /* Primary-Buttons dunkelgrün */
    button[kind="primary"] {
        background-color: #2d572c !important;
        color: white !important;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }

    button[kind="primary"]:hover {
        background-color: #244722 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar-thumb {
        background-color: #2d572c;
    }
    </style>
""", unsafe_allow_html=True)


# ----------------------------
# Dummy-Daten
# ----------------------------

city_coords = {
    "München": [48.1371, 11.5754],
    "Berlin": [52.5200, 13.4050],
    "Hamburg": [53.5511, 9.9937]
}

segments_df = pd.DataFrame({
    "city": ["München", "München", "Berlin", "Hamburg"],
    "name": ["Isar Trail", "Englischer Garten", "Tempelhofer Feld", "Alster Runde"],
    "lat": [48.13, 48.15, 52.49, 53.56],
    "lon": [11.57, 11.60, 13.41, 9.99],
    "surface": ["gravel", "asphalt", "asphalt", "dirt"]
})

pois_df = pd.DataFrame({
    "city": ["München", "München", "Berlin", "Hamburg", "Berlin"],
    "name": ["Café A", "Park B", "Café X", "Park Y", "Aussichtspunkt Z"],
    "type": ["cafe", "park", "cafe", "park", "viewpoint"],
    "lat": [48.136, 48.145, 52.518, 53.558, 52.52],
    "lon": [11.574, 11.61, 13.402, 9.995, 13.40]
})

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("🌿 Einstellungen")

selected_cities = st.sidebar.multiselect(
    "Gebe bis zu 3 Städte für deinen Vergleich ein", list(city_coords.keys()), default=["München"], max_selections=3
)

sportart = st.sidebar.selectbox(
    "Wähle deine Sportart", ["Laufen", "Radfahren"]
)

selected_surfaces = st.sidebar.multiselect(
    "Bevorzugter Untergrund", ["asphalt", "gravel", "dirt", "paved", "unpaved"],
    default=["asphalt", "gravel"]
)

selected_poi_types = st.sidebar.multiselect(
    "Welche POI-Typen interessieren dich?", ["cafe", "park", "viewpoint"],
    default=["cafe", "park"]
)

map_city = st.sidebar.selectbox(
    "Welche Stadt soll auf der Karte angezeigt werden?", selected_cities
)

# ----------------------------
# Hauptbereich
# ----------------------------

st.markdown("<h1 style='color:green;'>VacationMatch!</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color:green;'>Städtevergleich & Karte</h1>", unsafe_allow_html=True)

st.markdown(f"""
**Gewählte Städte:** {', '.join(selected_cities)}  
**Sportart:** *{sportart}*  
**Untergrund:** {', '.join(selected_surfaces)}  
""")

# ----------------------------
# Daten filtern
# ----------------------------

# Für Karte: nur ausgewählte Stadt
filtered_segments = segments_df[
    (segments_df["city"] == map_city) &
    (segments_df["surface"].isin(selected_surfaces))
]

filtered_pois_map = pois_df[
    (pois_df["city"] == map_city) &
    (pois_df["type"].isin(selected_poi_types))
]

# Für Tabelle: alle ausgewählten Städte
filtered_pois_table = pois_df[
    (pois_df["city"].isin(selected_cities)) &
    (pois_df["type"].isin(selected_poi_types))
]

# ----------------------------
# Karte
# ----------------------------

st.subheader(f"🗺️ Karte von {map_city}")

segment_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_segments,
    get_position='[lon, lat]',
    get_radius=60,
    get_fill_color='[0, 180, 50, 160]',  # grün
    pickable=True
)

poi_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_pois_map,
    get_position='[lon, lat]',
    get_radius=80,
    get_fill_color='[0, 100, 250, 160]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=city_coords[map_city][0],
    longitude=city_coords[map_city][1],
    zoom=12
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[segment_layer, poi_layer],
    tooltip={"text": "{name}"}
))

# ----------------------------
# Tabelle mit POIs aller Städte
# ----------------------------

st.subheader("📋 Vergleichstabelle: POIs in gewählten Städten")

poi_summary = filtered_pois_table.groupby(["city", "type"]).size().reset_index(name="count")
pivot = poi_summary.pivot(index="type", columns="city", values="count").fillna(0).astype(int)

st.dataframe(pivot)

# ----------------------------
# Detail-Tabelle POIs der Karte
# ----------------------------

st.subheader(f"📍 POI-Details in {map_city}")
st.dataframe(filtered_pois_map[["name", "type"]])