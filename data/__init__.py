import geopandas as gpd
from pathlib import Path
import pandas as pd

data_path = Path("data")
config = pd.read_excel(data_path.joinpath('config.xlsx'), sheet_name='layers')

# filter out the following
# df['layer'] == 'Panama Unit Service Area' & df['label'] == 'Frick Unit North Service Area'
# df['layer'] == 'Frick Unit Pipeline' & df['label'] == 'Frick Unit'
gdf = gpd.read_parquet(data_path.joinpath("gdf-2023-08-15.parquet"))
# .pipe(
# 	lambda df: df.loc[
# 		(df['layer'] == 'Panama Unit Service Area') &
# 		(df['label'] != 'Frick Unit North Service Area')
# 	]
# ).pipe(
# 	lambda df: df.loc[
# 		(df['layer'] == 'Frick Unit Pipeline')&
# 		(df['label'] != 'Frick Unit')
# 	]
# )
district_boundary = gdf.pipe(lambda df:df.loc[df['layer'] == "District Boundary"])
# apns = gpd.read_parquet(data_path.joinpath("apns.parquet")).to_crs("EPSG:4326")
# apn_gdf = apns[apns.intersects(district_boundary.unary_union)]

apn_gdf = gpd.read_parquet(data_path.joinpath("apn_gdf_sa.parquet")).to_crs("EPSG:4326")
pipes = gpd.read_parquet(data_path.joinpath("pipes.parquet"))