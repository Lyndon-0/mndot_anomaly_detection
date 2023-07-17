import folium
import leafmap.foliumap as leafmap
import streamlit as st
def make_map(full_gdf,apns):
	lines = ['Proposed Pipeline', 'AEWSD North Canal', 'FFPPP Discharge Pipeline',"AEWSD Alignments"]
	filled_polygons = ['Frick Unit Service Area']
	hollow_polygons = ['District Boundary']
	points = ['Proposed Turnout']

	clip_layers = [
		'Proposed Turnout',
		# 'Proposed Pipeline',
		"Frick Unit Service Area",
		# "AEWSD Alignments",
		]
	service_boundary = full_gdf.pipe(lambda df:df.loc[df['label'] == "Frick Unit North Service Area"])
	intersect = lambda gdf: gdf[gdf.intersects(service_boundary.unary_union)]
	clip = lambda gdf: gdf.clip(service_boundary)
	apns = apns.to_crs("EPSG:4326")
	# find interescting shapes
	# intersecting_apns = apns[apns.intersects(service_boundary.unary_union)]



	m = leafmap.Map(
		# tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
		# attr="Esri",
		google_map="HYBRID",
		min_zoom=3,
		# max_zoom=12,

		# min_lat=bounds[2],
		# max_lat=bounds[3],
		# min_lon=bounds[0],
		# max_lon=bounds[1],
		# max_bounds=True,
		
		# zoom_control=False,
		draw_control=False,
		search_control=False,

	)

	for layer in hollow_polygons:
		try:
			gdf = full_gdf[full_gdf['layer']==layer]
			if layer in clip_layers:
				gdf = clip(gdf)
				# gdf = intersect(gdf)
			color = gdf['color'].unique()[0]
			m.add_gdf(
				gdf,
				layer_name=layer,
							# style_function=lambda x: {"color": "red", "fillOpacity": 0},
				fields=['layer'],
				highlight_function=lambda x: {"fillOpacity": 0.7, "weight": 6, "color": "lightgreen"},
				style={
					'color':color,
					'fillColor':"none",
					},
				# highlight_function=lambda x: x['properties'],
				# highlight_function=lambda x: {"l":x['properties']['label']},
				# highlight_function=lambda x: {"l":x['properties']['label']},
				)
		except:
			pass
			# st.markdown(f"Error with {layer}")
			# print(f"Error with {layer}")

	for layer in filled_polygons:
		try:
				
			gdf = full_gdf[full_gdf['layer']==layer]
			if layer in clip_layers:
				gdf = clip(gdf)
				# gdf = intersect(gdf)
			color = gdf['color'].unique()[0]
			m.add_gdf(
				gdf,
				layer_name=layer,
				# highlight_function=lambda x: {"l":x['properties']['label']},
				fields=['layer'],
				highlight_function=lambda x: {"fillOpacity": 0.4, "weight": 6, "color": "lightgreen"},
				style={
					# 'color':color,
					'color':"none",
					'fillColor':color,
					"tooltip":"label",
					},
					# tooltip="label",
				zoom_to_layer=True,
				)

		except:
			st.markdown(f"Error with {layer}")
			# print(f"Error with {layer}")
	
	intersecting_apns = apns[apns.intersects(service_boundary.unary_union)]
	# st.dataframe(intersecting_apns.drop(columns=['geometry']))
	apn_gdf = intersecting_apns#)


	apn_gdf['size'] = apn_gdf.geometry.area  
	# apn_gdf = apns
	# st.dataframe(apn_gdf.drop(columns=['geometry']))
	m.add_gdf(
		apn_gdf,
		# layer_name="APNs",
		# style_function=lambda x: {"color": "red", "fillOpacity": 0},
		fields=['APN','Acreage','Landowner'],
		# highlight_function=lambda x: {"fillOpacity": 0.7, "weight": 6, "color": "lightgreen"},
		
		style={
			'color':"white",
			"weight":0.5,
		},
	)
	for layer in points:
		try:
			gdf = full_gdf[full_gdf['layer']==layer]
			if layer in clip_layers:
				gdf = clip(gdf)
				# intersect(gdf)
			color = gdf['color'].unique()[0]
			for i,y in gdf.iterrows():
				folium.Circle(
					radius=30,
					location=[y.geometry.y,y.geometry.x],
					color=y['color'],
					fill=True,
					# tooltip=[y["label"]],
					tooltip="Proposed Turnout",
					).add_to(m)
			# add apns and labels
			
		except:
			st.markdown(f"Error with {layer}")


	for layer in lines:
		try:
			gdf = full_gdf[full_gdf['layer']==layer]
			# st.markdown(layer)
			# st.markdown(gdf.crs)
			if layer in clip_layers:
				gdf = clip(gdf)
				# intersect(gdf)
			color = gdf['color'].unique()[0]
			m.add_gdf(
				gdf,
				layer_name=layer,
				fields=['layer','label'],
				highlight_function=lambda x: {"fillOpacity": 0.7, "weight": 6, "color": "lightgreen"},
				# tooltip="label",
				style={'color': color},
				)

		except:
			st.markdown(f"Error with {layer}")
	# apns.crs = "EPSG:4326"
	# st.markdown(apns.crs)
	# apn_gdf = clip(apns.to_crs("EPSG:4326"))
	# apn_gdf = clip(apns)
	# apn_gdf = apns.to_crs("EPSG:4326")


	m.add_legend(
		title="Legend",
		legend_dict={
			"Proposed Pipeline": "orange",
			# "AEWSD Alignments": "orange",
			"AEWSD North Canal": "#0000ff",
			"FFPPP Discharge Pipeline": "red",
			"Frick Unit Service Area": "salmon",
			"District Boundary": "#000000",
			"Proposed Turnout": "#ffff00",
			"APN": "white",
		}
	)
	m.zoom_to_gdf(apn_gdf)
	# m.fit_bounds(bounds=ll_bounds,max_zoom=12)
	# m.set_max_bounds(ll_bounds)
	return m