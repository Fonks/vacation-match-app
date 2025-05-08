# vacation_match_app/ui/table_display.py

# Präsentiert eine Vergleichstabelle über POIs in mehreren Städten sowie eine Detailtabelle für die aktuell auf der Karte angezeigte Stadt.

import streamlit as st
import pandas as pd
from constants import POI_CATEGORIES

def categorize_poi(poi_type):
    for category, types in POI_CATEGORIES.items():
        if poi_type in types:
            return category
    return "Unkategorisiert"

def show_poi_comparison_table(poi_df: pd.DataFrame, selected_cities: list):
    """
    Zeigt eine Pivot-Tabelle, die POIs nach Stadt und Typ gruppiert.
    """
    st.subheader("📋 Vergleichstabelle: POIs in gewählten Städten")

    filtered = poi_df[poi_df["city"].isin(selected_cities)].copy()
    filtered["Kategorie"] = filtered["poi_type"].apply(categorize_poi)

    summary = filtered.groupby(["city", "Kategorie"]).size().reset_index(name="count")
    pivot = summary.pivot(index="Kategorie", columns="city", values="count").fillna(0).astype(int)

    st.dataframe(pivot, use_container_width=True)


def show_city_poi_details(poi_df: pd.DataFrame, selected_city: str):
    """
    Zeigt die POI-Details für eine Stadt in Tabellenform.
    """
    st.subheader(f"📍 POI-Details in {selected_city}")
    city_pois = poi_df[poi_df["city"] == selected_city].copy()
    city_pois["Kategorie"] = city_pois["poi_type"].apply(categorize_poi)

    grouped = city_pois.groupby("Kategorie")
    for name, group in grouped:
        st.subheader(name)
        st.dataframe(group[["name", "poi_type"]].reset_index(drop=True), use_container_width=True)

