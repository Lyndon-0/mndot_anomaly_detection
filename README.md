# MnDOT Detector Monitor — I-94 MVP

This Streamlit dashboard visualizes real-time and historical MnDOT detector data.

### Features
- Interactive map for sensor selection (via folium)
- 30-sec → 5-min time aggregation
- Basic rule checks (negative / flatline / zero-streak)
- Corridor-level heatmap and KPI summary

### Deployment
This app runs on [Streamlit Cloud](https://share.streamlit.io).  
Main entry: `mndot_app.py`

### Local Run
```bash
pip install -r requirements.txt
streamlit run mndot_app.py

## Release port (optional)
fuser -k 8501/tcp 2>/dev/null || true

## activate
streamlit run mndot_app.py --server.address 0.0.0.0 --server.port 8501
