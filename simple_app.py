import streamlit as st
from pathlib import Path

# from data import gdf,apn_gdf,pipes,config
# from util.simple_map_utils import make_map
st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)
st.title("Frick Unit Map")

from data import get_config, get_gdf
from util.map_utils import plot_map
# from data import get_config, get_gdf
sheet_name = "Simple"
gdf = get_gdf(sheet_name)
config = get_config(sheet_name)

# st.dataframe(apns.drop(columns=['geometry']))
m = plot_map(gdf, config)
m.to_streamlit(
	height=800,
)
st.markdown("Note: Turnout locations and pipeline sizes are subject to change depending upon landowner input and field surveys.")