import streamlit as st

class SidebarController:
    def __init__(self):
        # Hauptgruppen von POIs – das kannst du beliebig erweitern
        self.poi_groups = ["Natur", "Kultur", "Erholung", "Sport"]

    def select_poi_categories(self):
        st.sidebar.title("🌿 VacationMatch Einstellungen")
        st.sidebar.header("📂 POI-Kategorien")

        selected_groups = st.sidebar.multiselect(
            "Wähle die übergeordneten Kategorien von Orten, die dich interessieren:",
            options=self.poi_groups,
            default=["Natur", "Kultur"]
        )
        return selected_groups
