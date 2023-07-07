import streamlit as st
from pathlib import Path

from data import gdf,apns
st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)
st.title("Frick Unit Map")
from map_utils import make_map
m = make_map(gdf,apns)
m.to_streamlit()
st.markdown("Note: Turnout locations and pipeline sizes are subject to change depending upon input received from landowners")

