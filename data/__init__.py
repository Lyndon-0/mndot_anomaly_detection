import geopandas as gpd
from pathlib import Path
import pandas as pd
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")

data_path = Path(
	# "data"
	__file__
	# "G:\Arvin-Edison WSD-1215\121523003-Frick Unit Pipeline\400 GIS\Scripts\aewsd_frick_unit\data"
	).parent
logger.info(f"data_path: {data_path}")


def get_config(sheet_name):
	dfs = pd.read_excel(data_path.joinpath('config.xlsx'), sheet_name=None)
	return pd.merge(
		dfs[sheet_name].dropna(subset="id").drop(columns="Name"),
		dfs['Layers'],
		how="left",
		on='id',
	).iloc[::-1]


# filter out the following
# df['layer'] == 'Panama Unit Service Area' & df['label'] == 'Frick Unit North Service Area'
# df['layer'] == 'Frick Unit Pipeline' & df['label'] == 'Frick Unit'
# gdf = gpd.read_parquet(data_path.joinpath("gdf-2023-08-15.parquet"))

def get_gdf(sheet_name):
	# nan to none
	return gpd.read_parquet(
	sorted(
		data_path.glob(f"{sheet_name}-*.parquet"),
		reverse=True,
		key=lambda x:x.stem)[0]
	)#.pipe(lambda df: df.where(pd.notnull(df), None))

# grab newest parquet file
# simple_file = 

# full_file = sorted(
# 				data_path.glob("gdf-*.parquet"),
# 				reverse=True,
# 				key=lambda x:x.stem)[0]


# logger.log("INFO", f"loaded {gdf_file}")


# district_boundary = gdf.pipe(lambda df:df.loc[df['layer'] == "District Boundary"])
# apns = gpd.read_parquet(data_path.joinpath("apns.parquet")).to_crs("EPSG:4326")
# apn_gdf = apns[apns.intersects(district_boundary.unary_union)]

# apn_gdf = gpd.read_parquet(data_path.joinpath("apn_gdf_sa.parquet")).to_crs("EPSG:4326")
# pipes = gpd.read_parquet(data_path.joinpath("pipes.parquet"))