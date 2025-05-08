# vacation_match_app/ui/user_input.py

# Kümmert sich um die Benutzereingabe von Städten/Koordinaten und Auswahloptionen im Hauptbereich.

import streamlit as st

def get_user_locations_input(max_entries: int = 3) -> list:
    """
    Nimmt bis zu `max_entries` Städte- oder Koordinatenangaben vom User entgegen.
    Gibt eine Liste zurück (z. B. ["Berlin", "48.13,11.57"])
    """
    st.sidebar.markdown("### 🌍 Städte oder Koordinaten")
    st.sidebar.info("Gebe bis zu Städte oder GeländeKoordinaten zum Vergleich ein, anschließend bekommst du die vorhandenen Möglichkeiten angezeigt.")
    
    inputs = []
    for i in range(max_entries):
        value = st.sidebar.text_input(f"Ort {i + 1}", "")
        if value.strip():
            inputs.append(value.strip())
    
    return inputs

def get_activity_type_selector(city_options: list) -> tuple:
    """
    Fragt zuerst nach Stadt, dann nach Sportart (abhängig davon).
    Gibt (city_name, activity_type) zurück.
    """
    st.markdown("### Stadt & Aktivität wählen")
    selected_city = st.selectbox("Wähle eine Stadt", city_options)
    activity_type = st.radio("Aktivitätstyp", ["running", "riding"], horizontal=True)
    
    return selected_city, activity_type
