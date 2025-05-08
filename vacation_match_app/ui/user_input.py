import streamlit as st

class UserInputHandler:
    def __init__(self):
        # Du kannst hier Defaults setzen oder dynamisch übergeben
        self.available_cities = ["München", "Berlin", "Hamburg"]
        self.available_activities = ["Laufen", "Radfahren", "Wandern"]

    def get_selected_cities(self):
        st.sidebar.header("🏙️ Städteauswahl")
        cities = st.sidebar.multiselect(
            "Welche Städte möchtest du vergleichen?",
            options=self.available_cities,
            default=["München"]
        )
        return cities

    def get_selected_activity(self):
        st.sidebar.header("🏃 Aktivität")
        activity = st.sidebar.selectbox(
            "Wähle deine Sportart",
            options=self.available_activities,
            index=0
        )
        return activity

    def get_selected_poi_subcategories(self, selected_groups: list[str]):
        st.sidebar.header("📌 POI-Filter")
        # Mapping von Gruppen zu Subtypen (kann auch aus filters.py kommen)
        group_to_types = {
            "Natur": ["park", "viewpoint", "forest"],
            "Kultur": ["museum", "monument", "theatre"],
            "Erholung": ["cafe", "spa", "bench"],
            "Sport": ["stadium", "gym", "swimming_pool"]
        }

        # Sammle mögliche Typen
        subtypes = []
        for group in selected_groups:
            subtypes.extend(group_to_types.get(group, []))

        # Entferne Duplikate
        subtypes = sorted(set(subtypes))

        # POI-Filterauswahl
        selected_types = st.sidebar.multiselect(
            "Welche spezifischen Orte interessieren dich?",
            options=subtypes,
            default=subtypes
        )
        return selected_types
