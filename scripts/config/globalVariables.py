import os
# Other Paths to necessary python scripts and functions ----------------------------------------------------------------
# path to folder containing gdal_calc.py and gdal_merge.py
python_scripts_folder_path = r'C:/Users/NM12LQ/Anaconda3/envs/pop_env/Scripts' #O:/projekter/PY000014_D/popnet_env/Scripts
#path to folder with gdal_rasterize.exe
gdal_rasterize_path = r'C:/Users/NM12LQ/Anaconda3/envs/pop_env/Library/bin' #O:/projekter/PY000014_D/popnet_env/Library/bin
gdal_path = r'C:/Users/NM12LQ/Anaconda3/envs/pop_env/Lib/site-packages/osgeo'

# DIFFERENT PATHS ------------------------------------------------------------------------------------------------------
# Get path to main script
parent_path = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/PopNetV2_backup"
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Paths for the Population Data --------------------------------------------------------------
ancillary_EUROdata_folder_path =  parent_path + "/data_prep/euroData"

futureDataFolder = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/PopNetV2_backup/data_prep/Deliverable_5.4/future_development/"
# Specify database information -----------------------------------------------------------------------------------------
# path to postgresql bin folder
pgpath = r";C:/Program Files/PostgreSQL/9.5/bin"
pghost = 'localhost'
pgport = '5432'
pguser = 'postgres'
pgpassword = 'postgres'
