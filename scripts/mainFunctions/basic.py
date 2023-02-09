import os
import numpy as np
#Python get unique values from list using numpy.unique

# function to get unique values
def unique(list1):
    x = np.array(list1)
    print(np.unique(x))

## ## ## ## ## ----- CREATE NEW FOLDER  ----- ## ## ## ## ##
def createFolder(path):
    if not os.path.exists(path):
        print("------------------------------ Creating Folder : {} ------------------------------".format(path))
        os.makedirs(path)
    else: 
        print("------------------------------ Folder already exists------------------------------")

#A function to compare the elements of 2 lists
def non_match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i not in list_b:
            non_match.append(i)
    return non_match

import geopandas as gpd
import json
from rasterstats import zonal_stats
# Calculate zonal statistics from tiffs
def zonalStat(src_file, dst_file, polyPath, statistics):  
    # Read Files
    districts = gpd.read_file(polyPath)
    districts = districts.to_crs("EPSG:3035")
    
    zs = zonal_stats(districts, src_file,
                stats='{}'.format(statistics), all_touched = False, percent_cover_selection=None, percent_cover_weighting=False, #0.5-->dubled the population
                percent_cover_scale=None,geojson_out=True)
    
    for row in zs:
        newDict = row['properties']
        for i in newDict.keys():
            if i == '{}'.format(statistics):
                newDict['{}_'.format(statistics)] = newDict.pop(i)
        
    result = {"type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3035" } }, "features": zs}
    #dst_file = dstPath + "{0}".format(dstFile) #
    with open(dst_file , 'w') as outfile:
        json.dump(result, outfile)
        
# Calculate zonal statistics from tiffs
def createSognMean(year, src_file, dstPath, dstFile, districtsPath, name):
    # Read Files
    districts = gpd.read_file(districtsPath)
    districts = districts.to_crs("EPSG:3035")
    
    zs = zonal_stats(districts, src_file,
                stats='mean', geojson_out=True)
    for row in zs:
        newDict = row['properties']
        for i in newDict.keys():
            if i == 'mean':
                newDict['mean_{}'.format(name)] = newDict.pop(i)
        
    result = {"type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3035" } }, "features": zs}
    dst_file = dstPath + "{0}".format(dstFile) #
    with open(dst_file , 'w') as outfile:
        json.dump(result, outfile)
        
## ## ## ## ## ----- Unzip Folder  ----- ## ## ## ## ##
import zipfile
def unzip(path_to_zip_file, directory_to_extract_to, folderName):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to + "/{}".format(folderName))

from pathlib import Path
import imageio
def createGIFs(src_path, export_path, fileName):
    """_summary_

    Args:
        src_path (_str_): Directory where png files are stored
        export_path (_type_): Directory where the exported gif is saved
        fileName (_type_): File name of gif
    """    
    
    filePaths=[]
    for file in os.listdir(src_path):
        if file.endswith('.png'):
            filePath = Path(src_path + "/" + file)
            filePaths.append(filePath)
    print(filePaths)
    images = []
    for i in filePaths:
        images.append(imageio.imread(i))
    imageio.mimsave(export_path + '/{}.gif'.format(fileName), images, fps=24, duration=1)
        
