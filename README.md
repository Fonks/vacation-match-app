
# VacationMatch! – Deine smarte Reiseplanung für aktive Urlaube

**VacationMatch** soll eine datenbasierte Streamlit-App werden, die sportbegeisterten Nutzer:innen hilft, aus mehreren Städten die passende Destination für ihren aktiven Urlaub zu finden – basierend auf echten Strava-Daten und angereicherten OpenStreetMap-Informationen.

---

## Funktionsweise

Die App empfiehlt Routen je nach Nutzerpräferenz:

- **Sportart**: Laufen, Radfahren
- **Steigung**, **Streckenlänge**, **Beliebtheit**
- **Umgebung**: Park, Café, Aussichtspunkt

Kombiniert werden echte Routen aus **Strava** mit detaillierten Umgebungsdaten aus **OpenStreetMap** via Overpass API.

---

## Technologien

| Bereich        | Tools/Technologien                        |
|---------------|-----------------------------------------   |
| Frontend      | `Streamlit`                                |
| Backend       | `Python`, `Pandas`, `Requests`, `polyline` |
| Kartendarstellung | `Pydeck`                               |
| Datenquellen  | `Strava API`, `OpenStreetMap Overpass API` |
| Datenverarbeitung | eigene Pre-/Post-Processor             |
| Zusammenarbeit | `GitHub`                                  |

---

## Projektstruktur

| Datei | Beschreibung |
|-------|--------------|
| `strava_segments_riding.json` | Cache Datei Strava-Segmente für Radtouren (JSON-Format) |
| `strava_segments_running.json` | Cache Datei Strava-Segmente für Laufstrecken (JSON-Format) |
| `cache_manager.py` | Session State für Streamlit |
| `data_fetcher.py` | Modul zum Aufruf der Strava/OSM APIs |
| `osm_api.py` | Overpass API Abfragen zur OSM-Datengewinnung |
| `strava_api.py` | OAuth2-Authentifizierung und Segmentabruf von Strava |
| `pre_processor.py` | Vorbereitung der API Calls |
| `post_processor.py` | Extraktion der notwendigen Strava Infos aus der API-Antwort |
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
git clone https://github.com/Fonks/vacation-match-app.git
cd vacation-match-app
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

4. `.env` Datei erstellen (für Strava Token, Strava Token bekommt ihr auf https://www.strava.com/settings/api):
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
