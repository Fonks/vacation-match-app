import streamlit as st

def display_sidebar():
    # Eingabe der Städte oder Koordinaten durch den Benutzer
    selected_cities_input = st.sidebar.text_input("Gib bis zu 3 Städte oder Koordinaten (Koordinaten durch ein Komma getrennt) ein")

    # Wenn der Benutzer die Eingabe bestätigt (Enter drückt)
    if selected_cities_input:
        selected_cities = [city.strip() for city in selected_cities_input.split(',')]

        # Nur bis zu 3 Städte oder Koordinaten zulassen
        if len(selected_cities) > 3:
            st.sidebar.error("Bitte gib maximal 3 Städte oder Koordinaten ein.")
        else:
            # Sportart-Auswahl (wird erst angezeigt, nachdem Städte eingegeben wurden)
            sportart = st.sidebar.selectbox("Wähle eine Sportart", ["Running", "Cycling"])

            # POI-Typen basierend auf den API-Daten auswählen (wird erst angezeigt, nachdem Städte eingegeben wurden)
            # Diese Optionen werden abhängig von den abgerufenen Daten angepasst
            selected_poi_types = st.sidebar.multiselect("Wähle POI-Typen", ["Restaurant", "Park", "Museum", "Cafe"])

            # Karte mit Stadt auswählen (wird auch erst nach der Auswahl der Städte angezeigt)
            map_city = st.sidebar.selectbox("Stadt für Karte", selected_cities)

            # Rückgabe der Auswahl
            return selected_cities, sportart, selected_poi_types, map_city
    else:
        # Zeige eine Nachricht an, dass der Benutzer Städte oder Koordinaten eingeben muss
        st.sidebar.info("Gib Städte oder Koordinaten ein, um fortzufahren.")
        return [], "", [], ""
