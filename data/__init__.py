import geopandas as gpd
from pathlib import Path
import pandas as pd

data_path = Path("data")
config = pd.read_excel(data_path.joinpath('config.xlsx'), sheet_name='layers')
gdf = gpd.read_parquet(data_path.joinpath("gdf.parquet"))
apns = gpd.read_parquet(data_path.joinpath("apns.parquet"))
pipes = gpd.read_parquet(data_path.joinpath("pipes.parquet"))