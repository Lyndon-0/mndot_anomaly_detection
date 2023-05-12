import geopandas as gpd
import leafmap.foliumap as leafmap
from shapely import wkb, wkt
import folium
import streamlit as st
from pathlib import Path
import fiona


P = Path(r"data")
@st.cache_data
def load_files():
	gdbs = {file.stem:{layer:gpd.read_file(file,driver='FileGDB',layer=layer) for layer in fiona.listlayers(file)} for file in P.glob('**/*.gdb')}
	return gdbs


class Map:
	def __init__(self):
		self.map = leafmap.Map(
			google_map="HYBRID",
			# draw_control=False,
			draw_control=True,
		)

	# def add_boundaries(self,boundaries):
	# 	self.map.add_gdf(boundaries,layer_name="Boundaries",info_mode='on_click',)

	# def add_markers_and_labels(self,gdf,label_col,color,icon,prefix='glyphicon',hover_cols='all',name=None):
		
	# 	for i,row in gdf.iterrows():
	# 		# st.dataframe(row['COUNTY'])
	# 		# st.write(type(row.to_frame()))
	# 		# st.markdown(type(row))
	# 		row['Point Type'] = name

	# 		frame=row.to_frame()
	# 		# make point type first column
	# 			# frame = frame.reindex(['Point Type'] + frame.columns[:-1].tolist(), axis=1)

	# 		popup = frame.to_html(
	# 			header=False,
	# 			escape=False,
	# 			render_links=True,
	# 			# col_space=10,
	# 			border=3,
	# 			)
	# 		if hover_cols == 'all':
	# 			tooltip = popup
	# 		else:
	# 			# add point type to hover_cols if not there
	# 			if 'Point Type' not in hover_cols:
	# 				hover_cols.insert(0,'Point Type')
				
				
	# 			# st.dataframe(row.to_frame())
	# 			tooltip = frame.loc[hover_cols].to_html(
	# 				header=False,
	# 				escape=False,
	# 				render_links=True,
	# 				# col_space=10,
	# 				border=3,
	# 				)

			
	# 		self.map.add_marker(
	# 			(row.geometry.y,row.geometry.x),
	# 			# popup=y['point_id'],
	# 			# popup=popup,
	# 			# tooltip=row[label_col],
	# 			# tooltip=row.to_html(),
	# 			# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
	# 			popup=popup,
	# 			tooltip=tooltip,
	# 			draggable=True,
	# 			# tooltip=f"{row.iloc[:].to_dict() }",
	# 			icon=folium.Icon(
	# 			color=color,
	# 			icon=icon,
	# 			prefix=prefix,
	# 			label=label_col,
	# 			# icon='bi bi-droplet'
	# 			),
	# 			# tooltip
	# 			)
	# 	gdf['latitude'] = gdf.geometry.y
	# 	gdf['longitude'] = gdf.geometry.x
	# 	self.map.add_labels(
	# 		data=gdf,
	# 		x='longitude',
	# 		y='latitude',
	# 		column=label_col,
	# 		font_color='white',
	# 		# font_color='black',

	# 		font_size='12pt',
	# 		layer_name='Wells',
	# 		# label_col=label_col,
	# 	)
M = Map()
gdbs = load_files()

for gdb in gdbs:
	for layer in gdbs[gdb]:
		M.map.add_gdf(gdbs[gdb][layer],layer_name=f"{gdb}: {layer}",info_mode='on_click',)
M.map.to_streamlit()