import geopandas as gpd
from pathlib import Path
data_path = Path("data")
gdf = gpd.read_parquet(data_path.joinpath("gdf.parquet"))
apns = gpd.read_parquet(data_path.joinpath("apns.parquet"))