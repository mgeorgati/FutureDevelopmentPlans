import geopandas as gpd
import random
import sys

def num_pieces(num, lenght):
    
    ot = list(range(1,lenght+1))[::-1]
    
    all_list = []
    for i in range(lenght-1):
        #print(i, ot[i])
        #n = random.randint(1, int((num-num/5) -ot[i]))
        #n = random.randint(1, (num-ot[i]))
        n = random.randint(1, int((num-num/2) -ot[i]))
        all_list.append(n)
        num -= n
        
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
        ha = int(row['max_urbanity_{0}'.format(scenario)])
        
        if ha > 0 and year_row>0:
            steps = int((year_row-2020) /5 )
            const = num_pieces(ha, steps)
            for x in range(len(const)):
                year_new = int(year_row - x*5)
                gdf.at[unique_id, '{1}_{0}_max_urbanity'.format(year_new, scenario) ] = const[x]
    
    gdf.to_file(dst_path_temp, driver='GeoJSON')
    
        

 