import streamlit as st
from pathlib import Path

from data import gdf,apns,pipes,config
from map_utils import make_map
st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)
st.title("Frick Unit Map")


# st.dataframe(apns.drop(columns=['geometry']))
m = make_map(gdf,apns,pipes,config)
m.to_streamlit()
st.markdown("Note: Turnout locations and pipeline sizes are subject to change depending upon input received from landowners")