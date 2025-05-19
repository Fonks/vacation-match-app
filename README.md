
# VacationMatch! – Deine smarte Reiseplanung für aktive Urlaube

**VacationMatch** ist eine datenbasierte Streamlit-App, die sportbegeisterten Nutzer:innen hilft, aus mehreren Städten die passende Destination für ihren aktiven Urlaub zu finden – basierend auf echten Strava-Daten und angereicherten OpenStreetMap-Informationen.

---

## Funktionsweise

Die App empfiehlt Routen je nach Nutzerpräferenz:

- **Sportart**: Laufen, Radfahren
- **Steigung**, **Streckenlänge**, **Beliebtheit**
- **Umgebung**: Park, Café, Aussichtspunkt

Kombiniert werden echte Routen aus **Strava** mit detaillierten Umgebungsdaten aus **OpenStreetMap** via Overpass API.

---

## Technologien

| Bereich        | Tools/Technologien                      |
|---------------|-----------------------------------------|
| Frontend      | `Streamlit`, `streamlit_folium`         |
| Backend       | `Python`, `Pandas`, `Requests`, `polyline` |
| Kartendarstellung | `Folium`, `Pydeck`, `geopy`            |
| Datenquellen  | `Strava API`, `OpenStreetMap Overpass API` |
| Datenverarbeitung | `GeoPandas` (optional), eigene Pre-/Post-Processor |
| Zusammenarbeit | `GitHub`, `.gitignore` für Caches etc. |

---

## Projektstruktur

| Datei | Beschreibung |
|-------|--------------|
| `strava_segments_riding.json` | Lokale Strava-Segmente für Radtouren (JSON-Format) |
| `strava_segments_running.json` | Lokale Strava-Segmente für Laufstrecken (JSON-Format) |
| `cache_manager.py` | Caching-Mechanismus für Datenabruf |
| `data_fetcher.py` | Modul zum Laden und Kombinieren von Strava/OSM-Daten |
| `osm_api.py` | Overpass API Abfragen zur OSM-Datengewinnung |
| `post_processor.py` | Nachbearbeitung der kombinierten Strava-OSM-Daten |
| `pre_processor.py` | Vorverarbeitung & Strukturierung der Rohdaten |
| `strava_api.py` | OAuth2-Authentifizierung und Segmentabruf von Strava |
| `map_layers.py` | Definition von Kartenebenen und Icons |
| `map_renderer.py` | Darstellung von Strecken und POIs auf der Streamlit-Karte |
| `constants.py` | Zentrale Kategorien und Filteroptionen |
| `osm_categories_selection.py` | UI-Komponente zur Auswahl von POIs |
| `main.py` | Streamlit App Entry Point |
| `requirements.txt` | Python-Abhängigkeiten für das Projekt |
| `.gitignore` | Ausgeschlossene Dateien und Ordner für Git |

---

## Starten der App

###  Vorbereitung

1. Repository klonen:
```bash
git clone https://github.com/dein-name/vacationmatch.git
cd vacationmatch
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv .venv
source .venv/bin/activate  # oder .venv\Scripts\activate unter Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. `.env` Datei erstellen (für Strava Token):
```env
STRAVA_CLIENT_ID=your_id
STRAVA_CLIENT_SECRET=your_secret
STRAVA_REFRESH_TOKEN=your_token
```

### ▶️ App starten

```bash
streamlit run main.py
```

---
