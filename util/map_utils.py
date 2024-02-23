import geopandas as gpd
from pathlib import Path
import pandas as pd
from loguru import logger
import sys
import leafmap.foliumap as leafmap
import folium

logger.remove()
logger.add(sys.stderr, level="INFO")



def plot_map(full_gdf, config):
    m = leafmap.Map(
        # tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        # attr="Esri",
        google_map="HYBRID",
        min_zoom=3,
        # zoom_control=False,
        draw_control=False,
        search_control=False,
    )
    for i, y in config.iterrows():
        try:

            gdf = full_gdf[full_gdf["layer"] == y["Name"]]
            if y["shape_type"] == "hollow_polygon":
                m.add_gdf(
                    gdf,
                    fields=["layer"],
                    highlight_function=lambda x: {
                        "fillOpacity": 0.7,
                        "weight": 6,
                        "color": "lightgreen",
                    },
                    style={
                        "color": y["color"],
                        "fillColor": "none",
                        "weight": y["size"],
                    },
                )

            if y["shape_type"] == "line":
                m.add_gdf(
                    gdf,
                    layer_name=y["Name"],
                    fields=["layer", "label"],
                    # line_weight=y['size'],
                    highlight_function=lambda x: {
                        "fillOpacity": 0.7,
                        "weight": 6,
                        "color": "lightgreen",
                    },
                    # tooltip="label",
                    style={
                        "color": y["color"],
                        "weight": y["size"],
                    },
                )
            if y["shape_type"] == "filled_polygon":
                # apns['label'] = apns['label'] + "\nService Area Type: " + apns['Service Area Type']
                # gdf['label'] = gdf['label'].str.replace(r"\n","<br>")
                # logger.info(f"filled: {y}")
                # if y["Name"] == "APNs":
                #     gdf['size'] = gdf.geometry.area

                m.add_gdf(
                    gdf,
                    layer_name=y["Name"],
                    fields=["layer","label"],
                    highlight_function=lambda x: {
                        "fillOpacity": 0.4,
                        "weight": 6,
                        "color": "lightgreen",
                    },
                    style={
                        "color": y["color"],
                        # 'color':"none",
                        "fillColor": y["color"],
                        "tooltip": "label",
                        "alpha": y["alpha"],
                        # 'weight':y['size'],
                        # "weight": gdf["size"],
                        "weight": .2,
                    },
                    # tooltip="label",
                    zoom_to_layer=True,
                )


            if y["shape_type"] == "point":

                # logger.info(f"point: {y}")
                # folium.features.CustomIcon(icon_url,icon_size=(28, 30))
                # if type(y["custom_icon"]) == str:          
                #     for row, y_gdf in gdf.iterrows():
                #         folium.R(
                #             location=[y_gdf.geometry.y, y_gdf.geometry.x],
                #             tooltip=f"<b>Layer: </b>{y['Name']}<br><b>Label: </b>{y_gdf['label']}",
                #             icon=folium.CustomIcon(
                #                     icon_image=y["custom_icon"],
                #                     icon_size=(20,20),
                #                 ) ,
                #             # icon=folium.DivIcon(
                #             #         html=f'{y["custom_icon"]}',
                #             #         icon_size=(20,20),
                #             #     ) ,
                #         ).add_to(m)

                # else:
                for row, y_gdf in gdf.iterrows():
                    # st.dataframe(y)
                    folium.Circle(
                        radius=y["size"],
                        location=[y_gdf.geometry.y, y_gdf.geometry.x],
                        color=y["color"],
                        fill=True,
                        # icon=icon,
                        # fields=["label"],
                        tooltip=f"<b>Layer: </b>{y['Name']}<br><b>Label: </b>{y_gdf['label']}",
                    ).add_to(m)

        except Exception as e:
            logger.error(y["Name"])
            logger.error(e)

    hidden_gdf_layers = [
        # "Groundwater Service Area",
    ]

    legend_dict = {
        y["Name"]: y["color"]
        for i, y in config.iterrows()
        if y["Name"] not in hidden_gdf_layers
    }
    # sort alphabetically
    legend_dict = {
        k: v for k, v in sorted(legend_dict.items(), key=lambda item: item[0])
    }

    m.add_legend(
        title="Legend",
        legend_dict=legend_dict,
    )
    m.zoom_to_gdf(
        full_gdf[full_gdf["layer"] == "Proposed Pipeline"],
    )
    return m










# import folium
# import leafmap.foliumap as leafmap
# import streamlit as st
# from logger import logger

# def plot_filled_polygon(y)	
# 	layer = y['Name']
# 	# st.markdown(layer)
# 	try:
# 		gdf = full_gdf[full_gdf['layer']==layer]
# 		color = gdf['color'].unique()[0]
# 		m.add_gdf(
# 			gdf,
# 			layer_name=layer,
# 			# alpha=y['alpha'],
# 			# highlight_function=lambda x: {"l":x['properties']['label']},
# 			fields=['layer'],
# 			highlight_function=lambda x: {"fillOpacity": 0.4, "weight": 6, "color": "lightgreen"},
# 			style={
# 				'color':color,
# 				# 'color':"none",
# 				'fillColor':color,
# 				"tooltip":"label",
# 				"alpha":y['alpha'],
# 				# 'weight':y['size'],
# 				'weight':y['size'],
# 				},
# 				# tooltip="label",
# 			zoom_to_layer=True,
# 			)

# 	except Exception as e:
# 		error_msg = f"Error with {layer}\n'{e}'"
# 		logger.error(error_msg)
# 		st.markdown(f"Error with {layer}\n'{e}'")
# 		# print(f"E

# def plot_line(y):
# 	layer = y['Name']
# 	# st.markdown(layer)
# 	try:
# 		gdf = full_gdf[full_gdf['layer']==layer]
# 		color = gdf['color'].unique()[0]
# 		m.add_gdf(
# 			gdf,
# 			layer_name=layer,
# 			fields=['layer','label'],
# 			# line_weight=y['size'],
# 			highlight_function=lambda x: {"fillOpacity": 0.7, "weight": 6, "color": "lightgreen"},
# 			# tooltip="label",
# 			style={
# 				'color': color,
# 				'weight':y['size'],
# 				},
# 			)
# 	except Exception as e:
# 		st.markdown(f"Error with {layer}\n'{e}'")

# def plot_point(y):
# 	layer = y['Name']
# 	# st.markdown(layer)
# 	try:
# 		gdf = full_gdf[full_gdf['layer']==layer]
# 		color = gdf['color'].unique()[0]
# 		for i,y in gdf.iterrows():
# 			folium.Circle(
# 				radius=y['size'],
# 				location=[y.geometry.y,y.geometry.x],
# 				color=y['color'],
# 				fill=True,
# 				# fields=["label"],
# 				tooltip=f"<b>Layer: </b>{y['layer']}<br><b>Label: </b>{y['label']}",
# 				).add_to(m)
# 		# add apns and labels
		
# 	except Exception as e:
# 		st.markdown(f"Error with {layer}\n'{e}'")


# def plot_hollow_polygon(y):
# 	layer = y['Name']
# 	# st.markdown(layer)
# 	# st.dataframe(y)
# 	try:
# 		gdf = full_gdf[full_gdf['layer']==layer]
# 		color = gdf['color'].unique()[0]
# 		m.add_gdf(
# 			gdf,
# 			# layer=layer,
# 			fields=['layer'],
# 			highlight_function=lambda x: {"fillOpacity": 0.7, "weight": 6, "color": "lightgreen"},
# 			style={
# 				'color':color,
# 				'fillColor':"none",
# 				'weight':y['size'],
# 				},
# 			)
# 	except Exception as e:
# 		error_msg = f"Error with {layer}\n'{e}'"
# 		logger.error(error_msg)
# 		st.markdown(error_msg)
# 		# print(f"Error with {layer}")

# 	for i,y in get_type(df,"hollow_polygon"):
# 		plot_hollow_polygon(y)

# 	# for layer in filled_polygons:
# 	for i,y in get_type(df,"filled_polygon"):
# 		plot_filled_polygon(y)
	


# 	apn_gdf['size'] = apn_gdf.geometry.area



# 	m.add_gdf(
# 		apn_gdf,
# 		layer_name="APNs",
# 		fields=['APN','Acreage','Landowner','Service Area Type'],
# 		style={
# 			'color':"white",
# 			"weight":0.2,
# 			"alpha":.05,
# 		},
# 	)
	
# 	# for layer in points:
# 	for i,y in get_type(df,"point"):
# 		plot_point(y)
	


# 	# for layer in lines:
# 	for i,y in get_type(df,"line"):
# 		plot_line(y)


# def make_map(full_gdf,apn_gdf,pipes,config):
# 	df = config
# 	# get_type = lambda df,shape_type: df.loc[df['shape_type'] == shape_type].iterrows()
	
# 	non_gdf_layers = [
# 		'APNs',
# 		# 'Proposed Pipeline',
# 	]
# 	hidden_gdf_layers = [
# 		# 'Frick Unit Service Area',
# 		# 'Frick Unit Service Area 2',
# 		'Groundwater Service Area',
# 		'TWCS',
# 	]
# 	get_type = lambda df,shape_type: df.loc[
# 		(df['shape_type'] == shape_type) &
# 		(~df['Name'].isin(hidden_gdf_layers + non_gdf_layers))
# 		].iterrows()

# 	clip_layers = [
# 		'Proposed Turnout',
# 		# 'Proposed Pipeline',
# 		# "Frick Unit Service Area",
# 		# "AEWSD Alignments",
# 		]
# 	service_boundary = full_gdf.pipe(lambda df:df.loc[df['label'] == "Frick Unit North Service Area"])
# 	# intersect = lambda gdf: gdf[gdf.intersects(service_boundary.unary_union)]
# 	clip = lambda gdf: gdf.clip(service_boundary)
# 	# find interescting shapes
# 	# intersecting_apns = apns[apns.intersects(service_boundary.unary_union)]

# 	m = leafmap.Map(
# 		# tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
# 		# attr="Esri",
# 		google_map="HYBRID",
# 		min_zoom=3,
		
# 		# zoom_control=False,
# 		draw_control=False,
# 		search_control=False,
# 	)


# 	legend_dict = {
# 			y['Name']:y['color'] for i,y in config.iterrows() if y['Name'] not in hidden_gdf_layers
# 		}
# 	# sort alphabetically
# 	legend_dict = {k: v for k, v in sorted(legend_dict.items(), key=lambda item: item[0])}

# 	m.add_legend(
# 		title="Legend",
# 		legend_dict=legend_dict,
# 	)
# 	m.zoom_to_gdf(
# 		full_gdf[full_gdf['layer'] == "Proposed Pipeline"],
# 	)

# 	"""
# 	"""
# 	# m.fit_bounds(bounds=ll_bounds,max_zoom=12)
# 	# m.set_max_bounds(ll_bounds)
# 	return m