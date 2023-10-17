import streamlit as st
from pathlib import Path

from data import gdf,apn_gdf,pipes,config
from simple_map_utils import make_map
st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)
st.title("Frick Unit Map")


# st.dataframe(apns.drop(columns=['geometry']))
m = make_map(gdf,apn_gdf,pipes,config)
m.to_streamlit()
st.markdown("Note: Turnout locations and pipeline sizes are subject to change depending upon landowner input and field surveys.")