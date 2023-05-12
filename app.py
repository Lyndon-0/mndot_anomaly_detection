import geopandas as gpd
import leafmap.foliumap as leafmap
from shapely import wkb, wkt
import folium
import streamlit as st
from pathlib import Path
import fiona

st.set_page_config(layout="wide", page_title="Frick Unit Map", page_icon="💧",)

P = Path(r"data")
@st.cache_data
def load_files():
	gdbs = {file.stem:{layer:gpd.read_file(file,driver='FileGDB',layer=layer) for layer in fiona.listlayers(file)} for file in P.glob('**/*.gdb')}
	return gdbs

st.markdown("# Frick Unit Map")
class Map:
	def __init__(self):
		self.map = leafmap.Map(
			google_map="HYBRID",
			draw_control=False,
			# draw_control=True,
		)

M = Map()
gdbs = load_files()


layer_rules = {
	"Block Reference 9194F":{
		# 'Polygons':{"color":"red","fill_color":"red","fill_opacity":0.5,"weight":1,"opacity":0.5},
		'Polylines':{"color":"red","opacity":1,"weight":15,'label':False},
	},
	"Frick Unit Areas":{
		'Polygons':{"color":"orange","fill_opacity":0.5,"weight":8,"opacity":0.5,'label':True,'font_size':8},
	},
	"Frick Unit":{
		'Points':{"color":"purple",'label':True,'font_size':10},
		'Polylines':{"color":"pink","weight":8,'label':False},
		'Polygons':{"color":"green","fill_color":"green","weight":10,"fill":False,"opacity":0.5,'label':False},
	},
}




for gdb in gdbs:
	for layer in gdbs[gdb]:
		gdf = gdbs[gdb][layer]
		options = layer_rules[gdb][layer]
		M.map.add_gdf(
		gdf,
		layer_name=f"{gdb}: {layer}",
		info_mode='on_click',
		style=options,
		)
		if options['label'] == True:
			M.map.add_labels(
				data=gdf,
				column='Name',
				# font_color='white',
				font_color=options['color'],
				font_size=f'{options["font_size"]}pt',

			)



legend_dict = {f"{gdf}: {k}":v['color'] for gdf,layer in layer_rules.items() for k,v in layer.items()}
# st.markdown(legend_dict)

M.map.add_legend(
	# builtin_legend='NLCD',
	title='Legend',
	legend_dict=legend_dict,
	)


M.map.to_streamlit()