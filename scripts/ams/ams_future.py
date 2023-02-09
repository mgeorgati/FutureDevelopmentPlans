# Main Script for data preparation -------------------------------------------------------------------------------------
# imports
import os
import sys
import geopandas as gpd
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(base_dir + '/data_prep/')
from mainFunctions.basic import zonalStat
from config.globalVariables import futureDataFolder
from config.grootams_config import city, raster_file, temp_shp_path
from config.globalVariables import gdal_path, gdal_rasterize_path
print('Modules successfully loaded')

#from calc_future_infra import trainProcess
from randomAssignement import random_creation, randomDivisionToGridCells
# This script controls all the processes for the production of future layers for disaggregation: housing area, building height, construction year, proximity to train and metro stations, 
# Baseline year 2020, baseline scenario= bs, zero-migration scenario = zms
scenario = 'bs'
data_path = futureDataFolder + '/{0}/trainingdata/'.format(city)

"""
# Creating Isochones for each year for train stations and counting the accessibility of each cell  
init_trainProcess = "no" 
trainProcess00 = "no" 
trainProcess01 = "no"
trainProcess02 = "no"
trainProcess03 = "yes"
"""

# Creating random distribution of residential projects to years and grid cells
init_residentialProcess= "yes"
divideHousingAreaToYears = 'yes'
divideHousingAreaToGridCells = 'yes'

temp_shp = data_path + '/temp_shp/'
temp_tif = data_path + '/tif/'
"""
if init_trainProcess == "yes": 
    src_file = data_path + "/shp/{0}_trainst.geojson".format(city)   
    year_list = [2035, 2040, 2045, 2050]#,2025, 2030, 2035, 2040, 2045, 2050]
    transport_means = '{}_trainst'.format(scenario) 
    # Processing train and metro Station data to postgres--------------------------------------------------------------------------------------
    for year in year_list:
        yearColName = 'year_{0}'.format(scenario)
        trainProcess(trainProcess00, trainProcess01, trainProcess02, trainProcess03, src_file, city, cur,conn,
                 engine, transport_means, year, yearColName, temp_shp, temp_tif, gdal_rasterize_path, raster_file)
"""
if init_residentialProcess == "yes": 
            
    if divideHousingAreaToYears == 'yes':
        futurePlansFile = data_path + "/shp/{0}_residential.geojson".format(city)
        gridPath = temp_shp_path + "/{}_grid.geojson".format(city)
        dst_path_temp = data_path + "/shp/{0}_residential_{1}.geojson".format(city,scenario)
        random_creation(futurePlansFile, gridPath, dst_path_temp, scenario)     
    if divideHousingAreaToGridCells == 'yes':       
        for year in range(2025, 2055, 5):
            dst_path_temp = data_path + "/shp/{0}_residential_{1}.geojson".format(city, scenario)
            dst_vector = data_path + "/shp/{0}_residential_{1}A.geojson".format(city, scenario)
            column_name = '{0}'.format(year,scenario)
            current_yearPath = temp_tif + "/{2}_{1}_housingArea_Future.tif".format(city, year, scenario)
            previousYear= int(year - 5)
            
            if previousYear==2020:
                previous_yearPath = temp_tif + "/ua_{1}_urban_dense.tif".format(city, previousYear, scenario)
            else: previous_yearPath = temp_tif + "/{2}_ua_{1}_urban_dense.tif".format(city, previousYear, scenario)

            temp_raster = temp_tif + "/{2}_ua_{1}_urban_dense_temp.tif".format(city, year, scenario)
            dst_raster_temp = temp_tif + "/{2}_ua_{1}_urban_dense_temp1.tif".format(city, year, scenario)
            dst_raster = temp_tif + "/{2}_ua_{1}_urban_dense.tif".format(city, year, scenario)
            
            randomDivisionToGridCells(year, scenario, dst_path_temp, dst_vector, raster_file, column_name, current_yearPath, previous_yearPath, temp_raster,
                                       dst_raster_temp, dst_raster)  
            
            

