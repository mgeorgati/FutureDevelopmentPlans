import os
import subprocess
import time
import geopandas as gpd
import glob
import numpy as np
from mainFunctions.format_conversions import dbTOraster, shptoraster
from mainFunctions.basic import createFolder

def createTemplate(city, temp_shp_path, temp_tif_path, raster_file, gdal_rasterize_path):
    src_file = temp_shp_path + "/{0}_cs.geojson".format(city)
    src = gpd.read_file(src_file)
    src['rast_id'] = 1
    src.to_file(temp_shp_path + "/{0}_cs_updated.geojson".format(city), driver='GeoJSON', crs ='EPSG:3035' )
    print(src.head(4))
    dst_file = temp_tif_path + '/{}_template.tif'.format(city)
    shptoraster(raster_file, temp_shp_path + "/{0}_cs_updated.geojson".format(city), gdal_rasterize_path, dst_file, 'rast_id', xres=100, yres=100)
    os.remove(temp_shp_path + "/{0}_cs_updated.geojson".format(city))
    
def calculateUrbanAtlas(city,year,ancillary_data_folder_path, temp_shp_path, temp_tif_path, raster_file, conn,cur, engine, gdal_rasterize_path, python_scripts_folder_path):
    print(ancillary_data_folder_path + "/urban_atlas//Shapefiles/*.gpkg")
    if year == 2006:
        src_file = glob.glob(ancillary_data_folder_path + "/urban_atlas/{0}/Shapefiles/*{0}*.shp".format(year))
        print(src_file)
        df = gpd.read_file(src_file[0])
        columnName = 'ITEM2006'
        print(df[columnName ].unique())
        
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Continuous urban fabric (S.L. : > 80%)\r\nContinuous urban fabric (S.L. : > 80%)',df[columnName] == 'Discontinuous dense urban fabric (S.L. : 50% -  80%)'), 'urban_dense', '')  
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Discontinuous medium density urban fabric (S.L. : 30% - 50%)', np.logical_or(df[columnName] == 'Discontinuous very low density urban fabric (S.L. : < 10%)', df[columnName] == 'Discontinuous low density urban fabric (S.L. : 10% - 30%)')) , 'urban_sparse', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Green urban areas', df[columnName] == 'Sports and leisure facilities') , 'green_spaces', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Industrial, commercial, public, military and private units', df[columnName] == 'Isolated structures') , 'industry_commerce', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Port areas', np.logical_or(df[columnName] == 'Airports', df[columnName] == 'Mineral extraction and dump sites')) , 'infra_heavy', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Pastures', np.logical_or(df[columnName] == 'Arable land (annual crops)', df[columnName] == 'Permanent crops (vineyards, fruit trees, olive groves)')) , 'agriculture', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Complex and mixed cultivation patterns', np.logical_or(df[columnName] == 'Forests', np.logical_or(df[columnName] == 'Herbaceous vegetation associations (natural grassland, moors...)', df[columnName] == 'Open spaces with little or no vegetation (beaches, dunes, bare rocks, glaciers)'))) , 'natural_areas', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Construction sites', np.logical_or(df[columnName] == 'Land without current use',np.logical_or(df[columnName] == 'Fast transit roads and associated land', np.logical_or(df[columnName] == 'Other roads and associated land', df[columnName] == 'Railways and associated land')))), 'infra_light', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Agricultural, semi-natural areas, wetlands',np.logical_or(df[columnName] == 'Water', df[columnName] == 'Wetlands')) , 'water', df['land_use'])
        print(df.head(5))
        print(df['land_use'].unique())
    else:
        print(ancillary_data_folder_path + "/urban_atlas/{0}/Data/*.gpkg".format(year))
        src_file = glob.glob(ancillary_data_folder_path + "/urban_atlas/{0}/Data/*.gpkg".format(year))
        print(src_file)
        df = gpd.read_file(src_file[0])
        columnName = 'class_{}'.format(year)
        print(df[columnName].unique())
        
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Continuous urban fabric (S.L. : > 80%)',df[columnName] == 'Discontinuous dense urban fabric (S.L. : 50% -  80%)'), 'urban_dense', '')  
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Discontinuous medium density urban fabric (S.L. : 30% - 50%)', np.logical_or(df[columnName] == 'Discontinuous very low density urban fabric (S.L. : < 10%)', df[columnName] == 'Discontinuous low density urban fabric (S.L. : 10% - 30%)')) , 'urban_sparse', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Green urban areas', df[columnName] == 'Sports and leisure facilities') , 'green_spaces', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Industrial, commercial, public, military and private units', df[columnName] == 'Isolated structures') , 'industry_commerce', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Port areas', np.logical_or(df[columnName] == 'Airports', df[columnName] == 'Mineral extraction and dump sites')) , 'infra_heavy', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Pastures', np.logical_or(df[columnName] == 'Arable land (annual crops)', df[columnName] == 'Permanent crops (vineyards, fruit trees, olive groves)')) , 'agriculture', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Complex and mixed cultivation patterns', np.logical_or(df[columnName] == 'Forests', np.logical_or(df[columnName] == 'Herbaceous vegetation associations (natural grassland, moors...)', df[columnName] == 'Open spaces with little or no vegetation (beaches, dunes, bare rocks, glaciers)'))) , 'natural_areas', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Construction sites', np.logical_or(df[columnName] == 'Land without current use',np.logical_or(df[columnName] == 'Fast transit roads and associated land', np.logical_or(df[columnName] == 'Other roads and associated land', df[columnName] == 'Railways and associated land')))), 'infra_light', df['land_use'])
        df['land_use'] = np.where(np.logical_or(df[columnName] == 'Water', df[columnName] == 'Wetlands') , 'water', df['land_use'])

        #'Continuous urban fabric (S.L. : > 80%)','Discontinuous dense urban fabric (S.L. : 50% -  80%)'
        # 'Discontinuous medium density urban fabric (S.L. : 30% - 50%)', 'Discontinuous very low density urban fabric (S.L. : < 10%)', 'Discontinuous low density urban fabric (S.L. : 10% - 30%)'
        #'Green urban areas', 'Sports and leisure facilities'
        #'Industrial, commercial, public, military and private units','Isolated structures',
        # 'Port areas', 'Airports' 'Mineral extraction and dump sites'
        #'Pastures', 'Arable land (annual crops)', 'Permanent crops (vineyards, fruit trees, olive groves)'
        #'Forests', 'Herbaceous vegetation associations (natural grassland, moors...)', 'Open spaces with little or no vegetation (beaches, dunes, bare rocks, glaciers)'
        #'Fast transit roads and associated land', 'Other roads and associated land', 'Railways and associated land', 'Land without current use' 
        #'Construction sites'   
        #'Water' 'Wetlands' 
    bbox = gpd.read_file(temp_shp_path + "/{}_bbox.geojson".format(city))
    print(df['land_use'].unique().tolist())
    ndf = gpd.clip(df, bbox) 
    for i in [ 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas', 'infra_light', 'green_spaces', 'water']: #['urban_dense', 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas', 'infra_light', 'green_spaces', 'water']
        bdf = ndf.loc[ndf['land_use']== i]
        #print(bdf)
        bdf.to_postgis('{0}_ua_{2}_{1}'.format(city,i,year),engine)
        factor = 'ua_{1}_{0}'.format(i,year)
        calcPercentage(cur, conn, city, factor)
        
        dbTOraster(city, gdal_rasterize_path, engine, raster_file, temp_shp_path, temp_tif_path +'/ua/', '{0}_coverage'.format(factor), '{0}'.format(factor)) #
        #createFolder(temp_tif_path +'/ua')
        #template = temp_tif_path + '/{}_template.tif'.format(city)
        
        #filePath = temp_tif_path + '/ua_{0}_{1}.tif'.format(i,year)
        #print("------------------------------ Fixing  ------------------------------")
        #cmds = 'python {0}/gdal_calc.py -A "{1}" -B "{4}" --A_band=1 --B_band=1 --outfile="{2}/ua/ua_{5}_{3}" --calc="A*B"'.format(python_scripts_folder_path, filePath, temp_tif_path, i, template,year )
        #print(cmds)
        #subprocess.call(cmds, shell=True)

def calcPercentage(cur, conn, city, factor):
    print("Set Coordinate system for GRID")
    cur.execute("SELECT UpdateGeometrySRID('{0}_grid','geometry',3035);;".format(city))  # 4.3 sec
    conn.commit()

    #-------------------------------------------------------------------------------------------------------------------
    print("Checking {0} cover analysis table".format(city))
    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = '{0}_cover_analysis');".format(
            city))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating {0} cover analysis table".format(city))
        # Watercover percentage:
        cur.execute("Create table {0}_cover_analysis as \
                            (SELECT * \
                            FROM {0}_grid);".format(city))  # 4.3 sec
        conn.commit()
    else:
        print("{0} cover analysis table already exists".format(city))
    #-------------------------------------------------------------------------------------------------------------------

    print("Set Coordinate system for cover analysis")
    cur.execute("SELECT UpdateGeometrySRID('{0}_cover_analysis','geometry',3035);;".format(city))  # 4.3 sec
    conn.commit()

    # Adding necessary columns to city cover analysis table ---------------------------------------------------------
    print("---------- Adding necessary column to {0}_cover_analysis table, if they don't exist ----------".format(city))

    print("Checking {0} cover analysis - {1} column".format(city,factor))
    cur.execute("SELECT EXISTS (SELECT 1 \
                FROM information_schema.columns \
                WHERE table_schema='public' AND table_name='{0}_cover_analysis' AND column_name='{1}_coverage');".format(city,factor))
    check = cur.fetchone()
    print(check[0])
    if check[0] == False:
        print("Creating {0} cover analysis - {1} column".format(city,factor))
        # Adding water cover column to cover analysis table
        cur.execute(
            "Alter table {0}_cover_analysis \
            ADD column {1}_coverage double precision default 0;".format(city,factor))  # 11.3 sec #, \add column id SERIAL PRIMARY KEY
        conn.commit()
    else:
        print("{0} cover analysis - {1} column already exists".format(city,factor))

    # Indexing necessary tables ----------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    print("Checking gist index on {0} {1} table".format(city,factor))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace \
                    WHERE c.relname = '{0}_{1}_gix' AND n.nspname = 'public');".format(city,factor))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating gist index on {0} {1} table".format(city,factor))
        # Creating index on water layer
        cur.execute("CREATE INDEX {0}_{1}_gix ON {0}_{1} USING GIST (geometry);".format(city,factor))  # 32 msec
        conn.commit()
    else:
        print("Gist index on {0} {1} table already exists".format(city,factor))
    #-------------------------------------------------------------------------------------------------------------------
    print("Checking id index on {0} cover analysis table".format(city))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace \
                        WHERE c.relname = '{0}_cover_analysis_id_index' AND n.nspname = 'public');".format(city))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating id index on {0} cover analysis table".format(city))
        # Create index on city water cover id
        cur.execute("CREATE INDEX {0}_cover_analysis_id_index ON {0}_cover_analysis (id);".format(city))  # 4.8 sec
        conn.commit()
    else:
        print("Id index on {0} cover analysis table already exists".format(city))
    #-------------------------------------------------------------------------------------------------------------------
    print("Checking gist index on {0} cover analysis table".format(city))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace \
                            WHERE c.relname = '{0}_cover_analysis_gix' AND n.nspname = 'public');".format(city))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating gist index on {0} cover analysis table".format(city))
        # Creating index on water layer
        cur.execute("CREATE INDEX {0}_cover_analysis_gix ON {0}_cover_analysis USING GIST (geometry);".format(city))
        conn.commit()
    else:
        print("Gist index on {0} cover analysis table already exists".format(city))

    #-------------------------------------------------------------------------------------------------------------------
    print("Set Coordinate system for ITERATION GRID")
    cur.execute("SELECT UpdateGeometrySRID('{0}_iteration_grid','geometry',3035);;".format(city))  # 4.3 sec
    conn.commit()

    # getting id number of chunks within the iteration grid covering the city ---------------------------------------
    ids = []
    cur.execute("SELECT gid FROM {0}_iteration_grid;".format(city))
    chunk_id = cur.fetchall()

    # saving ids to list
    for id in chunk_id:
        ids.append(id[0])
    # Processing queries / running the cover analysis-----------------------------------------------------------------------------------------------
    print("-------------------- PROCESSING COVERAGE ANALYSIS: {0} consists of {1} big chunks --------------------".format(city, len(ids)))

    # Calculating water cover percentage -------------------------------------------------------------------------------

    print("---------- Calculating {0} cover percentage ----------".format(factor))
    # start total query time timer
    start_query_time = time.time()

    # preparing water table by subdividing city water table
    print("Creating subdivided {} table".format(factor))
    cur.execute(
        "CREATE TABLE subdivided_{0}_{1} AS (SELECT ST_Subdivide({0}_{1}.geometry, 40) AS geometry FROM {0}_{1})".format(
            city,factor))

    # create index on water
    cur.execute("CREATE INDEX subdivided_{0}_{1}_gix ON subdivided_{0}_{1} USING GIST (geometry);".format(city,factor))

    # iterating through chunks
    for chunk in ids:
       
        # check if chunk is pure ocean
        cur.execute("SELECT {0}_iteration_grid.gid \
                            FROM {0}_iteration_grid, {0}_cs \
                            WHERE ST_Intersects({0}_iteration_grid.geometry, {0}_cs.geometry) \
                            AND {0}_iteration_grid.gid = {1};".format(city, chunk))
        result_check = cur.rowcount

        if result_check == 0:
            print("Chunk number: {0} \ {1} is empty, setting {2} = 0 procent".format(chunk, len(ids), factor))
            # Setting the values of the whole chunk in city_cover_analysis - water_cover to 100 procent
            cur.execute("WITH a AS (SELECT {0}_cover_analysis.id, {0}_cover_analysis.geometry \
                        FROM {0}_cover_analysis, {0}_iteration_grid \
                        WHERE {0}_iteration_grid.gid = {1} \
                        AND ST_Intersects({0}_cover_analysis.geometry, {0}_iteration_grid.geometry)) \
                        UPDATE {0}_cover_analysis SET {2}_coverage = 0 FROM a WHERE a.id = {0}_cover_analysis.id;".format(
                city, chunk, factor))
        else:
            print("Chunk number: {0} \ {1} is not empty, Processing...".format(chunk, len(ids)))
            # start single chunk query time timer
            t0 = time.time()
            # select cells that is within each chunk and create a new table
            cur.execute("CREATE TABLE chunk_nr{1} AS (SELECT {0}_cover_analysis.id, {0}_cover_analysis.geometry \
                            FROM {0}_cover_analysis, {0}_iteration_grid \
                            WHERE {0}_iteration_grid.gid = {1} \
                            AND ST_Intersects({0}_cover_analysis.geometry, {0}_iteration_grid.geometry));".format(city,
                                                                                                        chunk))  # 1.6 sec
            conn.commit()

            # create index on chunk
            cur.execute("CREATE INDEX chunk_nr{0}_gix ON chunk_nr{0} USING GIST (geometry);".format(chunk))  # 464 msec
            conn.commit()

            # calculating water cover percentage
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id, sum(ST_AREA(ST_INTERSECTION(chunk_nr{1}.geometry, {0}_{2}.geometry))/10000*100) as {2} \
                            FROM chunk_nr{1}, {0}_{2} WHERE ST_intersects(chunk_nr{1}.geometry, {0}_{2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis SET {2}_coverage = {2} from a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, factor))

            # drop chunk_nr table
            cur.execute("DROP TABLE chunk_nr{0};".format(chunk))  # 22 ms
            conn.commit()

            # stop single chunk query time timer
            t1 = time.time()

            # calculate single chunk query time in minutes
            total = (t1 - t0) / 60
            print("Chunk number: {0} took {1} minutes to process".format(chunk, total))

    # stop total query time timer
    stop_query_time = time.time()

    # calculate total query time in minutes
    total_query_time = (stop_query_time - start_query_time) / 60
    print("Total {1} cover query time : {0} minutes".format(total_query_time,factor))
    
    # drop subdivided water table
    cur.execute("DROP TABLE subdivided_{0}_{1};".format(city,factor))  # 22 ms
    conn.commit()




    