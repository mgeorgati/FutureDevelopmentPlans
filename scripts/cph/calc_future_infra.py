import sys,os
sys.path.append('C:/FUME/PopNetV2/data_prep/mainFunctions/') 
from format_conversions import vectortoDB, dbTOraster
from calc_Isochrones import computeIsochrones, calculateCountIsochrones


def trainProcess(trainProcess00, trainProcess01, trainProcess02, trainProcess03, src_file, city, cur,conn,
                 engine, transport_means, year, yearColName, temp_shp_path, temp_tif_path, gdal_rasterize_path, raster_file ):
    if trainProcess00 == "yes":
        vectortoDB(src_file, city, cur, engine, transport_means) 
    if trainProcess01 == "yes":
        print("------------------------------ COMPUTING COUNT OF ISOCHRONES FOR CELL IN GRID FOR TRAIN STATIONS {0} ------------------------------")
        computeIsochrones(transport_means, city, cur, conn, year, yearColName, timeColumn = 'traveltime', travelcost=15 )
    if trainProcess02 == "yes":
        print("------------------------------ COMPUTING ISOCHRONES FOR TRAIN STATIONS BIKING 15' with 15km/h------------------------------")
        calculateCountIsochrones(transport_means, city, conn, cur, year)
    if trainProcess03 == "yes":
        column_name = '{0}_{1}_count'.format(year, transport_means)
        layerName = '{0}_{1}'.format(year,transport_means)
        dbTOraster(city, gdal_rasterize_path, engine, raster_file, temp_shp_path, temp_tif_path, column_name, layerName)