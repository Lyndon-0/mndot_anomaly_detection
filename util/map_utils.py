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
                for row, y_gdf in gdf.iterrows():
                    # st.dataframe(y)
                    folium.Circle(
                        radius=y["size"],
                        location=[y_gdf.geometry.y, y_gdf.geometry.x],
                        color=y["color"],
                        fill=True,
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

