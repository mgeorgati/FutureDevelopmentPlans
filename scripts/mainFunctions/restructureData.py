import geopandas as gpd
import pandas as pd, numpy as np

import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir + '/data_prep/mainFunctions/')
from format_conversions import shptoraster
from basic import  createFolder

def non_match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i not in list_b:
            non_match.append(i)
    return non_match

def restructureData(city, xlsPath, df, xlsColName, xlsCol_abbr):
    """
        xlsPath
        df
        xlsColName : Name of column in excel the sum is estimated on 
        xlsCol_abbr : Name of column in excel respective to countries name/abbreviations in dataframe   
    """
    codes = pd.read_excel(xlsPath)
    regions = codes[xlsColName].unique().tolist()
    
    ldf = df.copy()
    
    print('regions', regions)

    a = codes['{}'.format(xlsCol_abbr)].to_list()
    b = df.columns.to_list()
    
    #print(a,b)
    print(non_match_elements(a, b))
    print(non_match_elements(b, a))
    for key in regions:
        keyFrame = codes.loc[codes['{}'.format(xlsColName)] =='{}'.format(key)]
        select = keyFrame[xlsCol_abbr].tolist()
        print('selection',select)
        ldf['{}'.format(key)] = ldf[ldf.columns.intersection(select)].sum(axis=1)
        print(ldf['{}'.format(key)].sum())
        ldf['{}'.format(key)].astype(int)
        print(key, ldf['{}'.format(key)].sum())
        
    if city == 'ams':
        others = []
        if 'Unnamed: 24' in ldf.columns:
            print('Unnamed: 24', ldf['Unnamed: 24'].sum())
            others.append('Unnamed: 24')
        if 'Internationaal gebied;' in ldf.columns:
            print('Internationaal gebied;', ldf['Internationaal gebied;'].sum())
            others.append('Internationaal gebied;')
        if 'Onbekend' in ldf.columns:
            print('Onbekend', ldf['Onbekend'].sum())
            others.append('Onbekend')
        
        ldf['OTH'] = ldf[ldf.columns.intersection(others)].sum(axis=1)
        ldf['OTH'].astype(int) 
        print('Others:', others, 'Sum:', ldf['OTH'].sum())
        
        maxValues = ldf[['EU West', 'EU East', 'Other Europe etc', 'Middle East + Africa', 'Turkey + Morocco', 'Former Colonies']].idxmax(axis=1)
        for i in maxValues.index:
            ldf.at[i, '{}_new'.format(maxValues[i])] = ldf.at[i, '{}'.format(maxValues[i])] + ldf.at[i, 'OTH']
            
        ldf['EU West_new'] = ldf['EU West_new'].fillna(ldf['EU West'])
        ldf['EU East_new'] = ldf['EU East_new'].fillna(ldf['EU East'])
        ldf['Other Europe etc_new'] = ldf['Other Europe etc_new'].fillna(ldf['Other Europe etc'])
        ldf['Middle East + Africa_new'] = ldf['Middle East + Africa_new'].fillna(ldf['Middle East + Africa'])
        ldf['Turkey + Morocco_new'] = ldf['Turkey + Morocco_new'].fillna(ldf['Turkey + Morocco'])
        ldf['Former Colonies_new'] = ldf['Former Colonies_new'].fillna(ldf['Former Colonies'])
    return ldf

def calcPopulationData(year, raster_file, gdal_rasterize_path, xlsColName, basePath, pop_path, gridSize):
    # Load the files
    df90 = gpd.read_file(pop_path + "/PopData/{0}/temp_shp/{0}_dataVectorGrid.geojson".format(year))
    for col in df90.columns:
        if col.startswith('L10_'):
            country = col.split('L10_')[1]
            df90 = df90.rename(columns={col: country})

    xlsPath = basePath + "/data/UNSD — Methodology.xlsx"
    #xlsColName = "DK"
    xlsCol_abbr = "ISO-alpha3 Code"
    df_90 = restructureData(xlsPath, df90, xlsColName, xlsCol_abbr)

    selection = ['L1_SUM_POPULATION', 'MENAPA', 'DNK', 'EEU', 'OtherNonWestern', 'OtherWestern', 'WEU','Europe_nonEU', 'geometry']
    df90_roo = df_90[selection]

    createFolder(basePath + "/data/Population_{1}/{2}".format(year,xlsColName, gridSize ))
    src_file = basePath + "/data/Population_{1}/{2}/{0}_{2}.gpkg".format(year,xlsColName, gridSize )
    df90_roo.to_file(src_file, driver='GPKG',crs="EPSG:3035")

    for i in selection: 
        if i != 'geometry':
            dst_file = basePath + "/data/Population_{2}/{3}/{0}_{1}.tif".format(year, i, xlsColName, gridSize)
            shptoraster(raster_file, src_file, gdal_rasterize_path, dst_file, i, xres=100, yres=100)

def joinGrids(year, ancillary_EUROdata_folder_path, basePath, gridSize, fid, xlsColName):
    gridL = gpd.read_file(ancillary_EUROdata_folder_path + "/euroGrid/grid_{1}_{0}.gpkg".format('DK', gridSize))
    gridL = gridL[['geometry', '{}'.format(fid)]] #'GRD_ID'

    gridS = gpd.read_file(basePath + "/data/Population_{1}/{2}/{0}.gpkg".format(year,xlsColName, gridSize))

    gridS_with_gridL = gridS.sjoin(gridL, how="inner", predicate='within')
    gdf = gridS_with_gridL.copy()

    ndf = gpd.GeoDataFrame()
    for i in gridS.columns:
        if i != 'geometry':
            ndf['{}'.format(i)] = gdf.groupby(by = ['{0}'.format(fid)])['{}'.format(i)].sum()
    
    ndf = ndf.join(gridL.set_index('{0}'.format(fid)))
    ndf= gpd.GeoDataFrame(ndf, geometry='geometry')

    src_file = basePath + "/data/Population_{2}/{1}/{0}_{1}.gpkg".format(year, gridSize, xlsColName)
    ndf.to_file(src_file, driver='GPKG',crs="EPSG:3035")

