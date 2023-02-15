import os #, sys
#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import geopandas as gpd

from mainFunctions.format_conversions import dbTOraster, shptoraster
from mainFunctions.basic import createFolder


def calcRest(cur, conn, feature, city, chunk, xFactor, cFactor, futProjTable):
    # calculating URBAN SPARSE cover percentage - Intesects ---------------------
    cur.execute("WITH a AS (SELECT chunk_nr{1}.id \
                    FROM chunk_nr{1}, {5} WHERE ST_intersects(chunk_nr{1}.geometry, {5}.geometry) \
                    GROUP BY id) \
                    UPDATE {0}_cover_analysis t1 SET ua_{3}_{4}_coverage = CASE  \
                        WHEN t1.ua_{3}_urban_dense_coverage = ROUND(t1.ua_{2}_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_{2}_{4}_coverage ::NUMERIC,2) \
                        WHEN t1.ua_{3}_urban_dense_coverage < t1.ua_{2}_urban_dense_coverage THEN 0 \
                        END\
                        FROM a \
                    WHERE a.id = t1.id;".format(city, chunk, xFactor, cFactor, feature, futProjTable))
    conn.commit()
    # calculating URBAN SPARSE cover percentage - NOT intersecting
    cur.execute("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                            WHERE chunk_nr{1}.id not in ( \
                                                SELECT chunk_nr{1}.id from chunk_nr{1}, grootams_futureprojects_bs \
                                                    WHERE ST_intersects(chunk_nr{1}.geometry, grootams_futureprojects_bs.geometry))) \
                    UPDATE {0}_cover_analysis SET ua_{3}_{4}_coverage = ROUND(ua_{2}_{4}_coverage ::NUMERIC , 2) \
                        FROM a \
                    WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, xFactor, cFactor, feature))
    conn.commit()
                
def calcUrbanAtlasFuture(cur, conn, city, year, futureDataFolder, scenario, engine):
    #_______________________Future Projects_________________________
    print("Importing future projects to postgres")

    futtureProjectsPath = futureDataFolder + "/shp/{0}_residential_{1}.geojson".format(city,scenario)
    df = gpd.read_file(futtureProjectsPath)
    
    futProjTable = '{0}_futureprojects_{1}'.format(city, scenario)
    # Create Table for future projects
    print("---------- Creating table for country, if it doesn't exist ----------")
    print("Checking {0} Case Study table".format(futProjTable))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = '{0}');".format(futProjTable))
    check = cur.fetchone()
    if check[0] == True:
        print("{0} table already exists".format(futProjTable))

    else:
        print("Creating {0}".format(futProjTable))
        df.to_postgis('{0}'.format(futProjTable),engine)
        
    print("Set Coordinate system for GRID")
    cur.execute("SELECT UpdateGeometrySRID('{0}_grid','geometry',3035);;".format(city))  # 4.3 sec
    conn.commit()

    # Check if cover analysis table exists -------------------------------------------------------------------------------------------------------------------
    print("Checking {0} cover analysis table".format(city))
    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = '{0}_cover_analysis');".format(
            city))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating {0} cover analysis table".format(city))
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
    
    i = 'urban_dense'
    factor = 'ua_{1}_{0}'.format(i,year)
    if year == 2020 : 
        previousYear=2018
        previousfactor = 'ua_{1}_{0}'.format(i,year)
        xFactor = '2018'
    else : 
        previousYear = year-5
        previousfactor = 'ua_{2}_{1}_{0}'.format(i,previousYear,scenario )
        xFactor = '{0}_{1}'.format(scenario, year-5)
    
    if scenario == 'zms' : x_factor = 20 #the range of change in the distribution of the urban density
    elif scenario == 'bs' : x_factor = 10
    else: x_factor == 5
    
    cFactor =  '{0}_{1}'.format(scenario, year)
    for i in ['urban_dense','infra_light', 'green_spaces', 'water', 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas' ]: # 'infra_light', 'green_spaces', 'water','urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas']: # 
        factor = 'ua_{2}_{1}_{0}'.format(i,year, scenario)
        # Adding necessary columns to city cover analysis table ---------------------------------------------------------
        print("---------- Adding necessary column to {0}_cover_analysis table, if they don't exist ----------".format(city))

        print("Checking {0} cover analysis - {1} column".format(city,factor))
        cur.execute("SELECT EXISTS (SELECT 1 \
                    FROM information_schema.columns \
                    WHERE table_schema='public' AND table_name='{0}_cover_analysis' AND column_name='{1}_coverage');".format(city,factor))
        check = cur.fetchone()
        if check[0] == False:
            print("Creating {0} cover analysis - {1} column".format(city,factor))
            # Adding water cover column to cover analysis table
            cur.execute(
                "Alter table {0}_cover_analysis \
                ADD column {1}_coverage double precision default 0;".format(city,factor))  # 11.3 sec #, \add column id SERIAL PRIMARY KEY
            conn.commit()
        else:
            print("{0} cover analysis - {1} column already exists".format(city,factor))
        
        # ROUND UP PREVIOUS YEAR
        cur.execute(
                "UPDATE {0}_cover_analysis \
                SET ua_{1}_{2}_coverage = ROUND(ua_{1}_{2}_coverage ::NUMERIC, 2);".format(city, cFactor, i))  # 11.3 sec #, \add column id SERIAL PRIMARY KEY
        conn.commit()   

    #i = 'urban_dense'
    #factor = 'ua_{1}_{0}'.format(i,year)
    # Indexing necessary tables ----------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    print("Checking gist index on {0} {1} table".format(city,futProjTable))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace \
                    WHERE c.relname = '{0}_gix' AND n.nspname = 'public');".format(futProjTable))
    check = cur.fetchone()
    print(check)
    if check[0] == False:
        print("Creating gist index on {0} {1} table".format(city,futProjTable))
        # Creating index on water layer
        cur.execute("CREATE INDEX {0}_gix ON {0} USING GIST (geometry);".format(futProjTable))  # 32 msec
        conn.commit()
    else:
        print("Gist index on {0} table already exists".format(city,futProjTable))
    
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
    
    # iterating through chunks
    for chunk in ids:
        
        # check if chunk is pure ocean
        cur.execute("SELECT {0}_iteration_grid.gid \
                            FROM {0}_iteration_grid, {2} \
                            WHERE ST_Intersects({0}_iteration_grid.geometry, {2}.geometry) \
                            AND {0}_iteration_grid.gid = {1};".format(city, chunk, futProjTable))
        result_check = cur.rowcount

        if result_check == 0:
            print("Chunk number: {0} \ {1} is empty, setting {2} = 0 procent".format(chunk, len(ids), factor))
            # Setting the values of the whole chunk in city_cover_analysis - water_cover to 100 procent
            for i in ['urban_dense', 'infra_light', 'green_spaces', 'water', 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas'] : #'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas',  'green_spaces', 'water']:
                cur.execute("WITH a AS (SELECT {0}_cover_analysis.id, {0}_cover_analysis.geometry \
                            FROM {0}_cover_analysis, {0}_iteration_grid \
                            WHERE {0}_iteration_grid.gid = {1} \
                            AND ST_Intersects({0}_cover_analysis.geometry, {0}_iteration_grid.geometry)) \
                            UPDATE {0}_cover_analysis SET ua_{2}_{3}_coverage = ua_{4}_{3}_coverage \
                            FROM a WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, cFactor, i, xFactor)) # 
                conn.commit() 
            
        else:
            print("Chunk number: {0} \ {1} is not empty, Processing...".format(chunk, len(ids)))
            # start single chunk query time timer
            t0 = time.time()
            # select cells that is within each chunk and create a new table
            cur.execute("CREATE TABLE chunk_nr{1} AS (SELECT {0}_cover_analysis.id, {0}_cover_analysis.geometry \
                            FROM {0}_cover_analysis, {0}_iteration_grid \
                            WHERE {0}_iteration_grid.gid = {1} \
                            AND ST_Intersects({0}_cover_analysis.geometry, {0}_iteration_grid.geometry));".format(city, chunk))  
            conn.commit()

            # create index on chunk
            cur.execute("CREATE INDEX chunk_nr{0}_gix ON chunk_nr{0} USING GIST (geometry);".format(chunk))  
            conn.commit()
            print("WITH a AS (SELECT chunk_nr{1}.id, max({2}.{7}_{6}_max_urbanity) as ua \
                            FROM chunk_nr{1}, {2} WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis t1 SET ua_{3}_urban_dense_coverage =  CASE  \
                                WHEN t1.ua_{5}_urban_dense_coverage = 0 THEN ROUND( (random() * ((a.ua + {4}) - (a.ua-{4})) + (a.ua-{4}) )::NUMERIC, 2) \
                                WHEN t1.ua_{5}_urban_dense_coverage > 0 AND t1.ua_{5}_urban_dense_coverage < a.ua THEN ROUND( (random() * (a.ua  - t1.ua_{5}_urban_dense_coverage) + t1.ua_{5}_urban_dense_coverage )::NUMERIC, 2) \
                                ELSE ROUND(t1.ua_{5}_urban_dense_coverage ::NUMERIC , 2) \
                                END \
                                FROM a \
                            WHERE a.id = t1.id;".format(city, chunk, futProjTable, cFactor, x_factor, xFactor, year, scenario ))
            # calculating new urban cover percentage for cells in chunk that intersect  ---------------------
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id, max({2}.{7}_{6}_max_urbanity) as ua \
                            FROM chunk_nr{1}, {2} WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis t1 SET ua_{3}_urban_dense_coverage =  CASE  \
                                WHEN t1.ua_{5}_urban_dense_coverage = 0 THEN ROUND( (random() * ((a.ua + {4}) - (a.ua-{4})) + (a.ua-{4}) )::NUMERIC, 2) \
                                WHEN t1.ua_{5}_urban_dense_coverage > 0 AND t1.ua_{5}_urban_dense_coverage < a.ua THEN ROUND( (random() * (a.ua  - t1.ua_{5}_urban_dense_coverage) + t1.ua_{5}_urban_dense_coverage )::NUMERIC, 2) \
                                ELSE ROUND(t1.ua_{5}_urban_dense_coverage ::NUMERIC , 2) \
                                END \
                                FROM a \
                            WHERE a.id = t1.id;".format(city, chunk, futProjTable, cFactor, x_factor, xFactor, year, scenario ))
            ### When it is lower than the previous year
            conn.commit()
            print("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                        WHERE chunk_nr{1}.id not in ( \
                                            SELECT chunk_nr{1}.id from chunk_nr{1}, grootams_futureprojects_bs \
                                                WHERE ST_intersects(chunk_nr{1}.geometry, grootams_futureprojects_bs.geometry))) \
                            UPDATE {0}_cover_analysis SET ua_{3}_urban_dense_coverage = ROUND(ua_{5}_urban_dense_coverage ::NUMERIC , 2)  \
                            FROM a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, futProjTable, cFactor, x_factor, xFactor, year, scenario ))
            
            # calculating new urban cover percentage where in chunk but NOT intersecting 
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                        WHERE chunk_nr{1}.id not in ( \
                                            SELECT chunk_nr{1}.id from chunk_nr{1}, grootams_futureprojects_bs \
                                                WHERE ST_intersects(chunk_nr{1}.geometry, grootams_futureprojects_bs.geometry))) \
                            UPDATE {0}_cover_analysis SET ua_{3}_urban_dense_coverage = ROUND(ua_{5}_urban_dense_coverage ::NUMERIC , 2)  \
                            FROM a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, futProjTable, cFactor, x_factor, xFactor, year, scenario ))
            ### When it is lower than the previous year
            conn.commit()
            print("WITH a AS (SELECT chunk_nr{1}.id \
                            FROM chunk_nr{1}, {2} WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis t1 SET ua_{4}_infra_light_coverage = CASE  \
                                WHEN t1.ua_{3}_urban_dense_coverage = ROUND(t1.ua_{4}_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_{3}_infra_light_coverage ::NUMERIC,2) \
                                WHEN t1.ua_{3}_urban_dense_coverage < t1.ua_{4}_urban_dense_coverage THEN ROUND( (random() * (((100 - t1.ua_{4}_urban_dense_coverage) - 0) + 0) )::NUMERIC,2) \
                                END\
                                FROM a \
                            WHERE a.id = t1.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            
            # calculating LIGHT INFRA cover percentage - Intesects ---------------------
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id \
                            FROM chunk_nr{1}, {2} WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis t1 SET ua_{4}_infra_light_coverage = CASE  \
                                WHEN t1.ua_{3}_urban_dense_coverage = ROUND(t1.ua_{4}_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_{3}_infra_light_coverage ::NUMERIC,2) \
                                WHEN t1.ua_{3}_urban_dense_coverage < t1.ua_{4}_urban_dense_coverage THEN ROUND( (random() * (((100 - t1.ua_{4}_urban_dense_coverage) - 0) + 0) )::NUMERIC,2) \
                                END\
                                FROM a \
                            WHERE a.id = t1.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            conn.commit()
            print("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                        WHERE chunk_nr{1}.id not in ( \
                                            SELECT chunk_nr{1}.id from chunk_nr{1}, {2} \
                                                WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry))) \
                            UPDATE {0}_cover_analysis SET ua_{4}_infra_light_coverage = ROUND(ua_{3}_infra_light_coverage ::NUMERIC , 2) \
                            FROM a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            # calculating LIGHT INFRA cover percentage - NOT intersecting  
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                        WHERE chunk_nr{1}.id not in ( \
                                            SELECT chunk_nr{1}.id from chunk_nr{1}, {2} \
                                                WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry))) \
                            UPDATE {0}_cover_analysis SET ua_{4}_infra_light_coverage = ROUND(ua_{3}_infra_light_coverage ::NUMERIC , 2) \
                            FROM a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            conn.commit()
            
            # calculating GREEN SPACES cover percentage - Intesects ---------------------
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id \
                            FROM chunk_nr{1}, {2} WHERE ST_intersects(chunk_nr{1}.geometry, {2}.geometry) \
                            GROUP BY id) \
                            UPDATE {0}_cover_analysis t1 SET ua_{4}_green_spaces_coverage = CASE  \
                                WHEN t1.ua_{3}_urban_dense_coverage = ROUND(t1.ua_{4}_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_{3}_green_spaces_coverage ::NUMERIC,2) \
                                WHEN t1.ua_{3}_urban_dense_coverage < t1.ua_{4}_urban_dense_coverage THEN ROUND( (100 - t1.ua_{4}_urban_dense_coverage - t1.ua_{4}_infra_light_coverage )::NUMERIC,2) \
                                END\
                                FROM a \
                            WHERE a.id = t1.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            conn.commit()
            # calculating GREEN SPACES cover percentage - NOT intersecting
            cur.execute("WITH a AS (SELECT chunk_nr{1}.id FROM chunk_nr{1} \
                                        WHERE chunk_nr{1}.id not in ( \
                                            SELECT chunk_nr{1}.id from chunk_nr{1}, grootams_futureprojects_bs \
                                                WHERE ST_intersects(chunk_nr{1}.geometry, grootams_futureprojects_bs.geometry))) \
                            UPDATE {0}_cover_analysis SET ua_{4}_green_spaces_coverage = ROUND(ua_{3}_green_spaces_coverage ::NUMERIC , 2) \
                                FROM a \
                            WHERE a.id = {0}_cover_analysis.id;".format(city, chunk, futProjTable, xFactor, cFactor))
            conn.commit()
            
            ###############################################################################
            for i in [ 'water', 'urban_sparse', 'industry_commerce', 'infra_heavy', 'agriculture', 'natural_areas']: # ]
                calcRest(cur, conn, i, city, chunk, xFactor, cFactor, futProjTable)
            
            
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
    
    



