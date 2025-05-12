import streamlit as st
import pandas as pd
from constants import POI_CATEGORIES  # Import the POI_CATEGORIES constant

class OSMFeatureSelector:
    def __init__(self, osm_data_cache, selected_osm_ids):
        self.osm_data_cache = osm_data_cache
        self.selected_osm_ids = selected_osm_ids


    # = Katogorisierung der POIs in OSM = 
        # Gruppiert die Kategorien in POI_CATEGORIES und gibt sie zurück.
    def group_osm_tags(self, osm_elements):
        """Group OSM elements by predefined POI categories."""
        grouped = {category: [] for category in POI_CATEGORIES.keys()}
        grouped["Other"] = []  # Add a fallback category for uncategorized items

        for el in osm_elements:
            tags = el.get("tags", {})
            categorized = False

            # Checkt, ob das Element irgendeiner Kategorie in POI_CATEGORIES matcht
            # und fügt es der entsprechenden Kategorie hinzu.

            for category, types in POI_CATEGORIES.items():
                if any(tags.get(key) in types for key in ["amenity", "leisure", "tourism", "shop"]):
                    grouped[category].append(el)
                    categorized = True
                    break

            # If no category matches, add to "Other"
            if not categorized:
                grouped["Other"].append(el)

        return grouped




    # = Anzeige der POIs in den Kategorien =
        # Hier wird die Anzeige der POIs in den Kategorien gemacht.
    def display_osm_features(self):
        """Display OSM features grouped by category."""
        if not self.osm_data_cache:
            st.warning("No OSM data available.")
            return

        grouped_osm = self.group_osm_tags(self.osm_data_cache.get("elements", []))
        st.subheader("🗺️ OSM Features by Category")


        # Hier könnte man die Kategorien dynamisch anpassen!
        for category, items in grouped_osm.items():
            if not items:
                continue  # Skip empty categories

            with st.expander(f"{category} ({len(items)})", expanded=False):
                rows = []

                # All IDs in this category
                category_ids = [f"{category}_{el.get('id')}" for el in items if el.get("lat") or el.get("center")]
                currently_selected = [cid for cid in category_ids if cid in self.selected_osm_ids]
                all_selected = len(currently_selected) == len(category_ids)

                # Checkbox to select all in category
                select_all = st.checkbox(
                    f"Select all ({category})",
                    value=all_selected,
                    key=f"{category}_select_all"
                )

                for el in items:
                    el_id = f"{category}_{el.get('id')}"
                    tags = el.get("tags", {})
                    lat_osm = el.get("lat") or el.get("center", {}).get("lat")
                    lon_osm = el.get("lon") or el.get("center", {}).get("lon")
                    if not (lat_osm and lon_osm):
                        continue

                    # Update selection status
                    if select_all and el_id not in self.selected_osm_ids:
                        self.selected_osm_ids.add(el_id)
                    elif not select_all and el_id in self.selected_osm_ids:
                        self.selected_osm_ids.discard(el_id)

                    # Individual checkbox
                    checked = el_id in self.selected_osm_ids
                    checked = st.checkbox(
                        label=tags.get("name", "n/a"),
                        key=el_id,
                        value=checked
                    )

                    if checked:
                        self.selected_osm_ids.add(el_id)
                        rows.append({
                            "Name": tags.get("name", "n/a"),
                            "Amenity": tags.get("amenity", "n/a"),
                            "Latitude": lat_osm,
                            "Longitude": lon_osm
                        })
                    else:
                        self.selected_osm_ids.discard(el_id)

                # Display selected rows as a DataFrame
                if rows:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True)