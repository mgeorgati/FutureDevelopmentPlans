import os,sys
import psycopg2
from sqlalchemy import create_engine

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(base_dir)
sys.path.append(base_dir + '/data_prep/')
from config.globalVariables import pguser, pghost, pgpassword, pgport

city ='cph'
country='DK'

# DIFFERENT PATHS ------------------------------------------------------------------------------------------------------
# Get path to main script
parent_path = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/PopNetV2_backup"
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Paths for the Population Data --------------------------------------------------------------
#path to ancillary data folder
ancillary_data_folder_path = parent_path + "/data_prep/{}_Projectdata/AncillaryData".format(city)
ancillary_POPdata_folder_path = base_dir + "/data_prep/{}_Projectdata/PopData".format(city)

# Paths for the data / folders in the Project_data folder --------------------------------------------------------------
#path to ancillary data folder
temp_shp_path = parent_path + "/data_prep/{}_ProjectData/temp_shp".format(city)
temp_tif_path = parent_path + "/data_prep/{}_ProjectData/temp_tif".format(city)


spdAncillary = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/SpatialDisaggregation/AncillaryData"
raster_file = spdAncillary + "/{0}/corine/waterComb_{0}_CLC_2012_2018.tif".format(city)

# Specify database information -----------------------------------------------------------------------------------------
# path to postgresql bin folder
pgdatabase = '{}_data'.format(city)
engine = create_engine(f'postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}?gssencmode=disable')
conn = psycopg2.connect(database=pgdatabase, user=pguser, host=pghost, password=pgpassword,sslmode="disable",gssencmode="disable")
cur = conn.cursor()