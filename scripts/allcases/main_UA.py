import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from corine_processing import calculateCorine
#from grids_creating import creatGrids

#from casestudyboundaries_creating import initPostgis, initPgRouting, createBoundaries, createBBox
from urban_atlas_processing import createTemplate, calculateUrbanAtlas
from urban_atlas_future import calcUrbanAtlasFuture
from config.globalVariables import gdal_rasterize_path, python_scripts_folder_path
from randomAssignement import random_creation
from mainFunctions.format_conversions import dbTOraster
city = 'grootams'
year = 2020
scenario = 'zms'

if city == 'grootams':
    from config.grootams_config import country, ancillary_data_folder_path, temp_shp_path,  temp_tif_path, raster_file, conn,cur, engine, futureDataFolder
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

# This is a process for creating land uses density layers by migration scenarion for the future
# You need the 2018 Urban atlas layers for each of the cities as baseline 
# You also need a vector layer of the polygons to be developed in the future for each city, called city_residential. 
# It shouls include a field 'year_scenario' indicating the completion year of the project and a field 'max_urbanity_scenario' which indicates the maximum level of continuous urban fabric.

# The 1st process is to include the baseline urban atlas layers in the database  
processUrbanAtlas = 'no'
#The 2nd step is to split the level of urbanity to the different examined years in 5-year intervals  
divideHousingAreaToYears = 'no'
# The 3rd step is to calculate the next year urban fabric layer and update the rest as well
processUrbanAtlasFuture = 'yes'
# The 4rth step is to rasterize the corresponding layers for each scenario, year and land use
rasterizeUrbanAtlasFuture = 'no'
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
    calculateUrbanAtlas(city,year,ancillary_data_folder_path, temp_shp_path, temp_tif_path, raster_file, conn,cur, engine, gdal_rasterize_path, python_scripts_folder_path)
    
if divideHousingAreaToYears == 'yes':
    futurePlansFile = futureDataFolder + "/shp/{0}_residential.geojson".format(city)
    gridPath = os.path.dirname(futureDataFolder) + "/temp_shp/{}_grid.geojson".format(city)
    dst_path_temp = futureDataFolder + "/shp/{0}_residential_{1}.geojson".format(city,scenario)
    random_creation(futurePlansFile, gridPath, dst_path_temp, scenario)     

if processUrbanAtlasFuture == 'yes':
    for scenario in ['bs','zms']: #'bs', 
        for year in [2020, 2025, 2030, 2035, 2040, 2045, 2050]:
            calcUrbanAtlasFuture(cur, conn, city, year, futureDataFolder, scenario, engine)

if rasterizeUrbanAtlasFuture == 'yes':
    for scenario in ['bs']: #, 'zms'
        for year in [2020, 2025, 2030, 2035, 2040, 2045, 2050]:
            for i in ['urban_dense', 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas', 'infra_light', 'green_spaces', 'water']:
                dbTOraster(city, gdal_rasterize_path, engine, raster_file, temp_shp_path, temp_tif_path +'/ua/', 'ua_{1}_{0}_{2}_coverage'.format(year, scenario, i), 'ua_{1}_{0}_{2}'.format(year, scenario, i)) 

