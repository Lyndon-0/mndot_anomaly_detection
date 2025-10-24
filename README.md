# [aewsd_frick_unit]

## Release port (optional)
fuser -k 8501/tcp 2>/dev/null || true

## activate
streamlit run mndot_app.py --server.address 0.0.0.0 --server.port 8501
