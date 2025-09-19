# The Rise and Fall of Somali Pirates — Interactive Dashboard

Analyze global piracy incidents (1994–2020) with an interactive Streamlit dashboard featuring a year slider, geospatial map, and regional distribution pie chart. The app fetches data from a public maritime piracy dataset and includes a ransom-trend view and contextual “rise/fall” summaries.

## Quick start

```bash
# 1) Install dependencies
pip install -r requirements.txt

# 2) Launch the app
streamlit run streamlit_app_new.py
```

### Requirements
- streamlit
- pandas
- altair
- plotly

## What’s inside

- **Streamlit app UI** with dark Altair theme, custom CSS, and wide layout.  
- **Animated year slider (1994–2020)** driving both the regional **pie chart** and the **Mapbox** scatter of attacks by type.  
- **Custom regional mapping**: countries remapped into analysis regions (e.g., *East Africa/Somalia*, *Malacca Strait*, *South China Sea*, etc.) with yearly counts and percentages.  
- **Line chart** of incidents per region across years.  
- **Ransom trends** (2005–2012) as grouped bars plus an average line.  
- **Context panels** summarizing reasons for the *rise* and *fall* of Somali piracy.  

## Data sources

The app pulls CSVs directly from a public GitHub dataset at runtime (pirate attacks + country codes).

## Project structure

```
.
├── Instructions_to_run.txt       # simple install/run steps
├── requirements.txt              # dependencies
└── streamlit_app_new.py          # full Streamlit app
```

## How to use

1. Use the **Year slider** to animate changes in regional composition and geospatial distribution.  
2. Toggle **attack types** via the legend to focus the map.  
3. Inspect the **line chart** for long-term regional trends.  
4. Review **ransom trends** for 2005–2012.  
5. Read the **context sections** for historical drivers behind rise/fall.  

## Notes & customization

- The app reads data **live from GitHub**; for offline runs, swap URLs for local CSV paths in `load_pirate_data()`.  
- Region buckets are defined in a **custom mapping** dictionary; adjust to your analysis needs.  
- Add new panels (e.g., per-vessel analysis, seasonal decomposition) where marked sections build figures.  

## Credits & license

Dashboard developed by **Ravi Teja Rajavarapu**, **Achu Jeeju**, and **Sai Charan Reddy Kotha** (credit appears in the app footer).  
License: MIT (or your choice).  
