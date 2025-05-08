# vacation_match_app/ui/table_display.py

# Präsentiert eine Vergleichstabelle über POIs in mehreren Städten sowie eine Detailtabelle für die aktuell auf der Karte angezeigte Stadt.

import streamlit as st
import pandas as pd

def show_poi_comparison_table(poi_df: pd.DataFrame, selected_cities: list):
    """
    Zeigt eine Pivot-Tabelle, die POIs nach Stadt und Typ gruppiert.
    """
    st.subheader("📋 Vergleichstabelle: POIs in gewählten Städten")

    filtered = poi_df[poi_df["city"].isin(selected_cities)]
    summary = filtered.groupby(["city", "type"]).size().reset_index(name="count")
    pivot = summary.pivot(index="type", columns="city", values="count").fillna(0).astype(int)

    st.dataframe(pivot, use_container_width=True)


def show_city_poi_details(poi_df: pd.DataFrame, selected_city: str):
    """
    Zeigt die POI-Details für eine Stadt in Tabellenform.
    """
    st.subheader(f"📍 POI-Details in {selected_city}")
    city_pois = poi_df[poi_df["city"] == selected_city][["name", "type"]]
    st.dataframe(city_pois.reset_index(drop=True), use_container_width=True)
