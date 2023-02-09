import time

def computeIsochrones(transport_means, city, cur, conn, year, yearColName, timeColumn = 'traveltime', travelcost=15 ):
    # Adding necessary columns to city cover analysis table ---------------------------------------------------------
    print("---------- Check if geometry column existis in streets, if they don't exist ----------".format(year))

    print("Checking streest - 'geometry' column".format(year))
    cur.execute("SELECT EXISTS (SELECT 1 \
                FROM information_schema.columns \
                WHERE table_schema='public' AND table_name='{}_streets' AND column_name='geometry');".format(city))
    check = cur.fetchone()
    if check[0] == False:
        print("Checking streest - 'geometry' column".format(year))
        cur.execute("SELECT EXISTS (SELECT 1 \
                    FROM information_schema.columns \
                    WHERE table_schema='public' AND table_name='{}_streets' AND column_name='geom');".format(city))
        check = cur.fetchone()
        if check[0] == False:
            print("Creating streets rename geom column to geometry column")
            # Adding water cover column to cover analysis table
            cur.execute(
                "ALTER TABLE {}_streets RENAME COLUMN geom TO geometry;".format(city))  # 11.3 sec #, \add column id SERIAL PRIMARY KEY
            conn.commit()
    else:
        print("geometry column already exists")
        
    # Adding necessary columns to city cover analysis table ---------------------------------------------------------
    print("---------- Check if geometry column existis in _cover_analysis, if they don't exist ----------".format(year))

    print("Checking streest - 'geometry' column".format(year))
    cur.execute("SELECT EXISTS (SELECT 1 \
                FROM information_schema.columns \
                WHERE table_schema='public' AND table_name='{}_cover_analysis' AND column_name='geometry');".format(city))
    check = cur.fetchone()
    if check[0] == False:
        print("Checking streest - 'geometry' column".format(year))
        cur.execute("SELECT EXISTS (SELECT 1 \
                    FROM information_schema.columns \
                    WHERE table_schema='public' AND table_name='{}_cover_analysis' AND column_name='geom');".format(city))
        check = cur.fetchone()
        if check[0] == False:
            print("Creating _cover_analysis rename geom column to geometry column")
            # Adding water cover column to cover analysis table
            cur.execute(
                "ALTER TABLE {}_cover_analysis RENAME COLUMN geom TO geometry;".format(city))  # 11.3 sec #, \add column id SERIAL PRIMARY KEY
            conn.commit()
    else:
        print("geometry column already exists")
        
    # getting id numbers for transport_means stations covering the city ---------------------------------------
    transport_means_ids = []
    closestPoint_ids=[]
    #cur.execute("alter table {0}_transport_meansst ADD COLUMN gid serial;".format(city))
    cur.execute("SELECT gid FROM {0}_{2} WHERE {0}_{2}.{3} <= {1};".format(city, year, transport_means, yearColName))
    transport_means_id = cur.fetchall()
    for id in transport_means_id:
        transport_means_ids.append(id[0])
    print(transport_means_ids)
    
    for point in transport_means_ids:
        cur.execute("SELECT {0}_streets_vertices_pgr.id as start\
                        FROM\
                        {0}_streets_vertices_pgr,\
                        {0}_{2}\
                        WHERE {0}_{2}.gid = {1}\
                        ORDER BY ST_Distance({0}_streets_vertices_pgr.the_geom, {0}_{2}.geometry) ASC\
                        LIMIT 1 ;".format(city,point, transport_means ))
        closestPoint_id = cur.fetchall()
    
        for gid in closestPoint_id:
            closestPoint_ids.append(gid[0])
        
    # Creating necessary tables ----------------------------------------------------------------------------------------
    print("---------- Creating {0}_isochrones tables, if it doesn't exist ----------".format(transport_means))
    print("Checking {0} {1}_isochrones table".format(city, year))
    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = '{0}_{2}_isochrones_{1}');".format(city, year, transport_means))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating {0} {1}_isochrones table from case study extent".format(city,transport_means))
        # table for transport_means stations in case study:
        cur.execute("create table {0}_{2}_isochrones_{1} (id int, geom geometry);".format(city,year,transport_means))
        conn.commit()
    else:
        print("{0} {1}_isochrones table already exists".format(city, transport_means))

    # saving ids to list
    for cl_id in closestPoint_ids:
        # Processing queries / running the cover analysis-----------------------------------------------------------------------------------------------
        print("-------------------- CREATING IDS FOR STARTING POINTS FOR transport_means_isochrones (transport_means STATIONS) --------------------")
        cur.execute("insert into {0}_{3}_isochrones_{1} (id) values ({2})".format(city, year, cl_id, transport_means)) # average is 15 km/h
        conn.commit()

        # Processing queries / running the cover analysis-----------------------------------------------------------------------------------------------
        print("-------------------- CREATING transport_means_isochrones FOR {0} transport_means STATION --------------------".format(cl_id))
        cur.execute("update {0}_{3}_isochrones_{2} SET \
                        geom = (Select ST_ConcaveHull(ST_Collect(geometry),0.9,false) \
                        FROM {0}_streets   \
                        JOIN (SELECT edge FROM pgr_drivingdistance('SELECT gid as id, source, target, {4} AS cost from {0}_streets', {1}, {5}, false)) \
                        AS route \
                        ON {0}_streets.gid = route.edge) \
                        where id ={1}".format(city, cl_id, year, transport_means, timeColumn, travelcost)) # average is 15 km/h and travel time is 15'
        conn.commit()

def calculateCountIsochrones(transport_means, city, conn, cur, year):
   
    print("Checking {0} cover analysis - transport_means stations column".format(city))
    cur.execute("SELECT EXISTS (SELECT 1 \
                                FROM information_schema.columns \
                                WHERE table_schema='public' AND table_name='{0}_cover_analysis' \
                                AND column_name='{1}_{2}_count');".format(city, year, transport_means))
    check = cur.fetchone()
    if check[0] == False:
        print("Creating {0} cover analysis - transport_means stations column".format(city))
        # Adding transport_means stations column to country cover analysis table
        cur.execute("""Alter table {0}_cover_analysis ADD column "{1}_{2}_count" int default 0;""".format(city, year, transport_means))
        conn.commit()
    else:
        print("""{0} cover analysis - transport_means "{1}_{2}_count" column already exists""".format(city, year, transport_means))

    # Calculating transport_means stations based on count ----------------------------------------------------------------------------------------
    print("---------- Calculating transport_means stations ----------")
    # start total query time timer
    start_query_time = time.time()
     # getting id number of chunks within the iteration grid covering the city ---------------------------------------
    ids = []
    cur.execute("SELECT gid FROM {0}_iteration_grid;".format(city))
    chunk_id = cur.fetchall()

    # saving ids to list
    for id in chunk_id:
        ids.append(id[0])

    # iterate through chunks
    for chunk in ids:
        # start single chunk query time timer
        t0 = time.time()

        # Create table containing centroids of the original small grid within the land cover of the country
        cur.execute("CREATE TABLE chunk_nr_{1} AS (SELECT id, ST_Centroid({0}_cover_analysis.geometry) AS geom \
                            FROM {0}_cover_analysis, {0}_iteration_grid \
                            WHERE {0}_iteration_grid.gid = {1} \
                            AND ST_Intersects({0}_iteration_grid.geometry, {0}_cover_analysis.geometry)\
                            AND {0}_cover_analysis.water_cover < 99.999);".format(city, chunk))  # 1.7 sec
        # check if chunk query above returns values or is empty
        result_check = cur.rowcount

        if result_check == 0:
            print("Chunk number: {0} \ {1} is empty, moving to next chunk".format(chunk, len(ids)))
            conn.rollback()
        else:
            conn.commit()
            print("Chunk number: {0} \ {1} is not empty, Processing...".format(chunk, len(ids)))

            # Index chunk
            cur.execute("CREATE INDEX chunk_nr_{0}_gix ON chunk_nr_{0} USING GIST (geom);".format(chunk))  # 175 ms
            conn.commit()

            # Counting number of transport_means stations 
            cur.execute("""with a as (select chunk_nr_{1}.id, count(*) from {0}_{3}_isochrones_{2}, chunk_nr_{1} \
            where ST_Intersects(chunk_nr_{1}.geom, {0}_{3}_isochrones_{2}.geom) \
            group by chunk_nr_{1}.id) \
            update {0}_cover_analysis set "{2}_{3}_count" = a.count from a where a.id = {0}_cover_analysis.id;""".format(city, chunk, year, transport_means))  # 4.1 sec
            conn.commit()

            # Drop chunk_nr_ table
            cur.execute("DROP TABLE chunk_nr_{0};".format(chunk))  # 22 ms
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
    print("Total road distance query time : {0} minutes".format(total_query_time)) #13min