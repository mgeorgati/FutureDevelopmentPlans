from shapely.geometry import Polygon, MultiPolygon, shape, Point
import geopandas as gp
import rasterio as rs, numpy as np
from osgeo import gdal

def readRaster(file):
    """_Read a raster file in geotiff format_

    Args:
        file (_str_): The directory of the file to be read

    Returns:
        _array_: It returns an numpy array with nan, posinf, nginf set to 0.
    """    
    src = rs.open(file)
    arr = src.read(1)
    arr = np.nan_to_num(arr, nan=0, posinf=0, neginf=0) 

    return arr

def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds

def write_geotiff(filename, arr, in_ds):
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Float32

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(filename, arr.shape[1], arr.shape[0], 1, arr_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.FlushCache()
    band.ComputeStatistics(False)
    
import rasterio  
def writeRaster(raster_file, outfile, out_array):
    with rasterio.open(raster_file) as src:
        new_dataset = rasterio.open(
            outfile,
            'w',
            driver='GTiff',
            height=src.shape[0],
            width=src.shape[1],
            count=1,
            dtype=out_array.dtype,
            crs=src.crs,
            transform= src.transform
            )
    new_dataset.write(out_array, 1)
    new_dataset.close()
    
def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo

def checkGeom(df):
    '''
    Takes a GeoDataFrame of 2D/3D Multi/Polygons and returns a GeoDataFrame of 2D Polygons
    '''
    gdf = df.copy()
    for index,i in gdf.iterrows():
        geom = i['geometry']
        if geom.geom_type != 'Polygon':
            if geom.geom_type == 'POLYGON Z':
                gdf.geometry = convert_3D_2D(gdf.geometry)
            elif geom.geom_type == 'MultiPolygon':
                gdf = gdf.explode()
    gdf = gdf.reset_index(drop=True)
    return gdf

def vectortoDB(src_file, city, cur, engine, tableName):
    gdf = gpd.read_file(src_file)
    gdf = gdf.to_crs('epsg:3035')
    if 'year' not in gdf.columns:
        gdf['year'] = 0
    
    if 'gid' in gdf.columns and gdf['gid'].isnull().values.any()==True:
        gdf = gdf.drop(columns=['gid'])
        gdf = gdf.assign(gid=range(len(gdf))) 
    if 'gid' not in gdf.columns:
        gdf = gdf.assign(gid=range(len(gdf)))
        
    print("---------- Creating {1} table for {0}, if it doesn't exist ----------".format(city, tableName))
    print("Checking {0} Case Study table".format(city))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = '{0}_{1}');".format(city, tableName))
    check = cur.fetchone()
    if check[0] == True:
        print("{0} {1} table already exists".format(city,tableName))

    else:
        print("Creating {0} {1}".format(city, tableName))
        gdf.to_postgis('{0}_{1}'.format(city, tableName),engine)
        
import subprocess
from osgeo import gdal
def shptoraster(raster_file, src_file, gdal_rasterize_path, dst_file, column_name, xres=100, yres=100):
    '''
    Takes the path of GeoDataframe and converts it to raster
        raster_file         : str
            path to base raster, from which the extent of the new raster is calculated 
        src_file            : str
            path to source file (SHP,GEOJSON, GPKG) 
        gdal_rasterize_path : str
            path to execute gdal_rasterize.exe
        dst_file            : str
            path and name of the destination file
        column_name         : str
            Field to use for rasterizing
    '''
    data = gdal.Open(raster_file)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    data = None    
    cmd = '{0}/gdal_rasterize.exe -a "{9}" -te {1} {2} {3} {4} -tr {5} "{6}" "{7}" "{8}"'\
                .format(gdal_rasterize_path, minx, miny, maxx, maxy, xres, yres, src_file, dst_file, column_name)
                
    print(cmd)
    subprocess.call(cmd, shell=True)

import geopandas as gpd    
def dbTOraster(city, gdal_rasterize_path, engine, raster_file, temp_shp_path, temp_tif_path, column_name, layerName):
    # Create SQL Query
    sql = """SELECT id, "{0}", geometry FROM {1}_cover_analysis""".format(column_name, city) #geom
    # Read the data with Geopandas
    gdf = gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='geometry' ) #geom 

    # exporting water cover from postgres
    print("Exporting {0} from postgres".format(column_name))
    src_file = temp_shp_path + "/{0}Grid.geojson".format(layerName)
    gdf.to_file(src_file,  driver="GeoJSON")   
    dst_file = temp_tif_path + "/{0}.tif".format(layerName)
    
    shptoraster(raster_file, src_file, gdal_rasterize_path, dst_file, column_name, xres=100, yres=100)
    