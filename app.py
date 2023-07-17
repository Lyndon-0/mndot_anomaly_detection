import streamlit as st
from pathlib import Path

from data import gdf,apns,pipes
st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)
st.title("Frick Unit Map")
from map_utils import make_map


# st.dataframe(apns.drop(columns=['geometry']))
m = make_map(gdf,apns,pipes)
m.to_streamlit()
st.markdown("Note: Turnout locations and pipeline sizes are subject to change depending upon input received from landowners")