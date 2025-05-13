import streamlit as st
import pandas as pd
from ui.constants import POI_CATEGORIES  # Import the POI_CATEGORIES constant

class OSMFeatureSelector:
    def __init__(self, osm_data_cache, selected_osm_ids):
        self.osm_data_cache = osm_data_cache
        self.selected_osm_ids = selected_osm_ids


    # = Katogorisierung der POIs in OSM = 
        # Gruppiert die Kategorien in POI_CATEGORIES und gibt sie zurück.
    def group_osm_tags(self, osm_elements):
        """
        Group OSM elements by predefined POI categories with optional subcategories.

        Args:
            osm_elements (list): List of OSM elements (dictionaries) to be grouped.

        Returns:
            dict: A dictionary where keys are POI categories and values are dictionaries
                of subcategories containing lists of OSM elements.
        """
        # Initialisiere die Hauptkategorien aus POI_CATEGORIES
        grouped = {category: {} for category in POI_CATEGORIES.keys()}
        grouped["Other"] = {}  # Fallback-Kategorie für nicht zugeordnete Elemente

        for el in osm_elements:
            tags = el.get("tags", {})  # Hole die Tags des Elements

            # Filtere Elemente mit 'n/a'-Werten in relevanten Feldern
            if tags.get("name", "n/a") == "n/a" or tags.get("amenity", "n/a") == "n/a":
                continue  # Überspringe Elemente mit ungültigen Werten
            if not (el.get("lat") or el.get("center", {}).get("lat")):  # Latitude muss vorhanden sein
                continue
            if not (el.get("lon") or el.get("center", {}).get("lon")):  # Longitude muss vorhanden sein
                continue

            categorized = False  # Flag, um zu prüfen, ob das Element kategorisiert wurde

            # Prüfe, ob das Element einer Hauptkategorie zugeordnet werden kann
            for category, types in POI_CATEGORIES.items():
                if any(tags.get(key) in types for key in ["amenity", "leisure", "tourism", "shop"]):
                    # Bestimme die Subkategorie (z. B. basierend auf dem "amenity"-Tag)
                    sub_category = tags.get("amenity", "Other")
                    if sub_category not in grouped[category]:
                        grouped[category][sub_category] = []  # Initialisiere die Subkategorie
                    grouped[category][sub_category].append(el)  # Füge das Element hinzu
                    categorized = True
                    break

            # Falls keine Hauptkategorie passt, füge das Element zur "Other"-Kategorie hinzu
            if not categorized:
                sub_category = tags.get("amenity", "Other")
                if sub_category not in grouped["Other"]:
                    grouped["Other"][sub_category] = []  # Initialisiere die Subkategorie
                grouped["Other"][sub_category].append(el)  # Füge das Element hinzu

        return grouped

    # = Anzeige der POIs in den Kategorien =
        # Hier wird die Anzeige der POIs in den Kategorien gemacht.
    def display_osm_features(self):
        """
        Display OSM features grouped by category and subcategory in the Streamlit interface.

        This function uses Streamlit expanders to display the categories of OSM elements.
        Each subcategory is displayed with a checkbox to toggle the visibility of its items.
        """
        if not self.osm_data_cache:
            st.warning("No OSM data available.")  # Zeige Warnung, wenn keine Daten vorhanden sind
            return

        # Gruppiere die OSM-Elemente nach Kategorien und Subkategorien
        grouped_osm = self.group_osm_tags(self.osm_data_cache.get("elements", []))
        st.subheader("🗺️ OSM POIs nach Kategorien")

        # Iteriere über die Hauptkategorien
        for category, subcategories in grouped_osm.items():
            if not subcategories:
                continue  # Überspringe leere Kategorien

            # Hauptkategorie als aufklappbaren Bereich darstellen
            with st.expander(f"{category} ({sum(len(items) for items in subcategories.values())})", expanded=False):
                for sub_category, items in subcategories.items():
                    if not items:
                        continue  # Überspringe leere Subkategorien

                    # Checkbox für die Subkategorie
                    show_items = st.checkbox(
                        f"{sub_category} ({len(items)})",
                        value=False,
                        key=f"{category}_{sub_category}_show"
                    )

                    if show_items:  # Zeige die Items nur, wenn die Checkbox aktiviert ist
                        rows = []

                        # IDs aller Elemente in dieser Subkategorie
                        category_ids = [f"{category}_{el.get('id')}" for el in items]
                        currently_selected = [cid for cid in category_ids if cid in self.selected_osm_ids]
                        all_selected = len(currently_selected) == len(category_ids)

                        # Checkbox, um alle Elemente in der Subkategorie auszuwählen/abzuwählen
                        select_all = st.checkbox(
                            f"Select all ({sub_category})",
                            value=all_selected,
                            key=f"{sub_category}_select_all"
                        )

                        for el in items:
                            el_id = f"{category}_{el.get('id')}"
                            tags = el.get("tags", {})
                            lat_osm = el.get("lat") or el.get("center", {}).get("lat")
                            lon_osm = el.get("lon") or el.get("center", {}).get("lon")

                            # Überspringe Elemente ohne gültige Koordinaten
                            if not (lat_osm and lon_osm):
                                continue

                            # Update selection status basierend auf "Select all"-Checkbox
                            if select_all and el_id not in self.selected_osm_ids:
                                self.selected_osm_ids.add(el_id)
                            elif not select_all and el_id in self.selected_osm_ids:
                                self.selected_osm_ids.discard(el_id)

                            # Individuelle Checkbox für jedes Element
                            checked = el_id in self.selected_osm_ids
                            checked = st.checkbox(
                                label=tags.get("name", "Unknown"),
                                key=el_id,
                                value=checked
                            )

                            # Aktualisiere die Auswahl basierend auf der individuellen Checkbox
                            if checked:
                                self.selected_osm_ids.add(el_id)
                                rows.append({
                                    "Name": tags.get("name", "Unknown"),
                                    "Amenity": tags.get("amenity", "Unknown"),
                                    "Latitude": lat_osm,
                                    "Longitude": lon_osm
                                })
                            else:
                                self.selected_osm_ids.discard(el_id)

                        # Zeige die ausgewählten Elemente in einer Tabelle an
                        if rows:
                            df = pd.DataFrame(rows)
                            st.dataframe(df, use_container_width=True)

        # Save the selected OSM IDs in the session state
        st.session_state.selected_osm_ids = self.selected_osm_ids    
    