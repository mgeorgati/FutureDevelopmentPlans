import pandas as pd 
import geopandas as gpd
import random
import subprocess
import sys
sys.path.append('C:/FUME/PopNetV2/data_prep/mainFunctions/') 

from format_conversions import shptoraster
sys.path.append('C:/FUME/PopNetV2/data_prep/config/') 
from globalVariables import gdal_rasterize_path, python_scripts_folder_path, ancillary_EUROdata_folder_path

# Function to generate a list of
# m random non-negative integers
# whose sum is n
def randomList(m, n):
 
    # Create an array of size m where
    # every element is initialized to 0
    arr = [0] * m;
     
    # To make the sum of the final list as n
    for i in range(n) :
 
        # Increment any random element
        # from the array by 1
        arr[random.randint(0, n) % m] += 1;
    
    # Print the generated list
    return arr;
        
def num_pieces(num, lenght):
    if num == 1 or lenght == 1 :
        all_list = [lenght] 
    elif num <= lenght : 
        all_list = [0] * lenght
        n = random.randint(1, lenght-1)
        all_list[n] = num
    elif num <= 3*lenght : 
        all_list = [0] * lenght
        n = random.randint(1, lenght-1)
        all_list[n] = num
    else:
        ot = list(range(1,lenght+1))[::-1]
        
        all_list = []
        for i in range(lenght-1):
            #print(i, ot[i])
            #n = random.randint(1, int((num-num/5) -ot[i]))
            #n = random.randint(1, (num-ot[i]))
            n = random.randint(1, int((num-num/2) -ot[i]))
            all_list.append(n)
            num -= n
            if num < 0 :
                print('Negative values stop the process')
                sys.exit()
            elif 5000 < num <= 30000:
                num = num/3
            elif 30000 < num <= 100000:
                num = num/8 
            elif 100000 < num <= 200000:
                num = num/15 
            elif num > 200000:
                num = num/20
            else: continue
        all_list.append(num) 
    return all_list

def random_creation(futurePlansFile, _grid, dst_path_temp, scenario): 
        
    gdf = gpd.read_file(futurePlansFile)
    for i in gdf.columns: 
        if i!='geometry': 
            gdf['{}'.format(i)] = gdf['{}'.format(i)].fillna(0)
    gdf = gdf.assign(fid_project=range(len(gdf)))
    for i, row in gdf.iterrows():
        unique_id = row['fid_project']
        name = row['uniq_id']
        year_row = row['year_{}'.format(scenario)]
        ha = int(row['max_urbanity'])
        
        if ha > 0 and year_row>0:
            steps = int((year_row-2020) /5 )
            print(ha, steps)
            const = num_pieces(ha, steps)
            for x in range(len(const)):
                year_new = int(year_row - x*5)
                gdf.at[unique_id, '{1}_{0}_max_urbanity'.format(year_new, scenario) ] = const[x]
    
    gdf.to_file(dst_path_temp, driver='GeoJSON')
    """grid = gpd.read_file(_grid, crs='EPSG:3035')
    
    _overlay = gpd.overlay(grid, gdf, how='intersection')
    _overlay.drop(['geometry'], inplace=True, axis=1)
    
    grid_join = grid.set_index('FID').join(_overlay.set_index('FID'), rsuffix='r_')
    grid_join = grid_join.dropna(subset = ['geometry'])
    grid_join.columns = grid_join.columns.astype(str)
    joined = gpd.GeoDataFrame(grid_join.reset_index(), geometry='geometry', crs= 'EPSG:3035')
    joined.drop(['fid', 'gid', '_count', '_sum', '_mean', 'gidr_',
       '_countr_', '_sumr_', '_meanr_'], inplace=True, axis=1)
    #ndf = joined[['FID', 'geometry', 'fid_project', 'housing', 'name', '{}_total'.format(year)]]
    ndf = joined.rename(columns={'FID': 'fid'})
    if 'fid' not in ndf.columns: 
        ndf = ndf.assign(fid=range(len(ndf)))"""
    """ndf = ndf[[ 'fid', 'geometry', 'NAAMPLAN', 'TOTAAL', 
       'WTYPGGBC', 'WTYPAPPC', 'WTYPONBC', 'HRKPONBC', 'rent', 'buy', 
       'Sociale_huur', 'Middeldure_huur', 'Dure_huur', 'Dure_huur_of_Koop',
       'Koop', 'Nader_te_bepalen', 'Tijdelijk_Onzelfstandig', 'year_{}'.format(scenario), 
       'fid_project', '2025_{}_TOTAAL'.format(scenario), '2030_{}_TOTAAL'.format(scenario), '2040_{}_TOTAAL'.format(scenario),
       '2035_{}_TOTAAL'.format(scenario), '2045_{}_TOTAAL'.format(scenario), '2050_{}_TOTAAL'.format(scenario), '2020_{}_TOTAAL'.format(scenario)]]
    """
    """print(' ----- Creating intermediate file with the total m2 split to different years  ----- ')
    ndf.to_file(dst_path_temp, driver='GeoJSON')"""

def randomDivisionToGridCells(year, scenario, dst_path_temp, dst_vector, raster_file, column_name, current_yearPath, 
                              previous_yearPath, temp_raster,  dst_raster_temp, dst_raster, divisionFunction = 'random'):
    df = gpd.read_file(dst_path_temp)
    df = df[['fid', 'geometry', 'fid_project', '{0}_{1}_TOTAAL'.format(year,scenario)]]
    df = df.loc[df['{0}_{1}_TOTAAL'.format(year,scenario)] > 0 ]
    #df = df.assign(fid=range(len(df)))
    for i in df.columns: 
        if i!='geometry': 
            df['{}'.format(i)] = df['{}'.format(i)].fillna(0)
    df['total_size'] = df.groupby('fid_project')['fid'].transform('size') #the number of cells with the same fid_project
    #df = df.sort_values('{0}_{1}_TOTAAL'.format(year,scenario), ascending=False).drop_duplicates('fid').sort_index()
    has = []
    projects= []
    cellsTotal=[]
    appended_data =[]
    for x in df.fid_project.unique():
        projects.append(x)
        cells = df.loc[df.fid_project==x, 'total_size'].values[0]
        cellsTotal.append(cells)
        ha = df.loc[df.fid_project==x, '{0}_{1}_TOTAAL'.format(year,scenario)].values[0]
        #has.append(ha)
        
        ndf = df.loc[df['fid_project'] == x]
        print(x, ha, cells, int(len(ndf)) )
        #if divisionFunction == 'random':
            
        #if divisionFunction == 'homo_random':
            #const = randomList(int(len(ndf)), int(ha))
        print('project#:', x, ',houses:', ha, ',cells:', cells)
        if ha <= cells:
            if ha == 1:
                const_rand = [0] * cells
                const_rand[0] = ha
            else:
                const_rand = [0] * cells
                n = random.randint(0, cells-1)
                const_rand[n] = ha
        else:
            const = num_pieces(ha, int(len(ndf)))
            const_rand = random.sample(const, len(const))
        print(x, ha, cells, const_rand)
        print('length------', len(ndf))
        ndf['{}'.format(year)] = const_rand
        appended_data.append(ndf)
    lf = pd.concat(appended_data)
    print(lf.head(5)) 
    
    ldf = gpd.GeoDataFrame(lf.reset_index(), geometry='geometry', crs= 'EPSG:3035')
    ldf.to_file(dst_vector, driver='GeoJSON')
    
    shptoraster(raster_file, dst_vector, gdal_rasterize_path, current_yearPath, column_name, xres=100, yres=100)
    
    import numpy as np, os
    import rasterio
    src = rasterio.open(current_yearPath)
    arr = src.read(1)
    print(np.max(arr))
    cmds = 'python {0}/gdal_calc.py -A "{1}"  --A_band=1  --outfile="{2}" --calc="A*100/{3}"'.format(
            python_scripts_folder_path, current_yearPath, temp_raster, round(np.max(arr),2))
    print(cmds)
    subprocess.call(cmds, shell=True)
    
    print("---- Adding the previous year's housing area ----")
    cmds = 'python {0}/gdal_calc.py -A "{1}" -B "{2}" --A_band=1 --B_band=1 --outfile="{3}" --calc="A+B"'.format(
            python_scripts_folder_path, temp_raster, previous_yearPath, dst_raster_temp)
    print(cmds)
    subprocess.call(cmds, shell=True)
    
    print("---- Adding the previous year's housing area ----")
    cmds = 'python {0}/gdal_calc.py -A "{1}" --A_band=1 --outfile="{2}" --calc="100*(A>100) + (A<=100)*A"'.format(
            python_scripts_folder_path, dst_raster_temp, dst_raster )
    print(cmds)
    subprocess.call(cmds, shell=True)
    
    os.remove(dst_raster_temp)
    os.remove(temp_raster)
        

 