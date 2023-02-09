import sys
#from corine_processing import calculateCorine
#from grids_creating import creatGrids
from urban_atlas_processing import createTemplate, calculateUrbanAtlas
#from casestudyboundaries_creating import initPostgis, initPgRouting, createBoundaries, createBBox
 
from config.globalVariables import gdal_rasterize_path, python_scripts_folder_path, ancillary_EUROdata_folder_path
city = 'crc'
year = 2018

if city == 'grootams':
    from config.grootams_config import country, ancillary_data_folder_path, temp_shp_path,  temp_tif_path, raster_file, conn,cur, engine 
    nuts3_cd1 = ''
elif city == 'ams':
    from config.ams_config import country, ancillary_data_folder_path, temp_shp_path, temp_tif_path, raster_file, conn,cur, engine
elif city == 'cph':
    from config.cph_config import country, ancillary_data_folder_path, temp_shp_path,  temp_tif_path, raster_file, conn,cur, engine
elif city == 'crc':
    from config.crc_config import country, ancillary_data_folder_path, temp_shp_path, temp_tif_path, raster_file, conn,cur, engine 
elif city == 'rom':
    from config.rom_config import country, ancillary_data_folder_path, temp_shp_path,  temp_tif_path, raster_file, conn,cur, engine 

#_______________________First Files and Processes_________________________
# Import NutsFile, clip to Case Study extent
# Import Corine files, clip, use to create grid and iterate_grid 
# Import grids to DB and create BBox
"""setUpDB = 'no'
createBoundaries = 'no'
processCorine = 'no'
createGrids = 'no'
init_template = 'no' """
processUrbanAtlas = 'yes'

"""
if setUpDB == 'yes': 
    initPostgis(cur, conn)
    initPgRouting(cur, conn)
if createBoundaries == 'yes':
    createBoundaries(engine,conn, cur, ancillary_data_folder_path,ancillary_EUROdata_folder_path, nuts3_cd1, city, country, temp_shp_path)
    createBBox(engine, conn, cur, city, temp_shp_path)
if processCorine == 'yes':
    calculateCorine(city, ancillary_EUROdata_folder_path, python_scripts_folder_path, temp_shp_path, temp_tif_path, gdal_rasterize_path)
if createGrids == 'yes':  
    createGrids(city,engine, temp_tif_path, temp_shp_path,cur,country)
if init_template == "yes":
    createTemplate(city, temp_shp_path, temp_tif_path, raster_file, gdal_rasterize_path)"""
if processUrbanAtlas == 'yes':
    for year in [2006, 2012]:
        calculateUrbanAtlas(city,year,ancillary_data_folder_path, temp_shp_path, temp_tif_path, raster_file, conn,cur, engine, gdal_rasterize_path, python_scripts_folder_path)

