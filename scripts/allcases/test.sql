WITH a AS (SELECT chunk_nr4536.id, max(grootams_futureprojects_bs.bs_2025_max_urbanity) as ua   
FROM chunk_nr4536, grootams_futureprojects_bs WHERE ST_intersects(chunk_nr4536.geometry, grootams_futureprojects_bs.geometry)   
GROUP BY id)      
UPDATE grootams_cover_analysis t1 SET ua_bs_2025_urban_dense_coverage =  CASE       
WHEN t1.ua_bs_2020_urban_dense_coverage = 0 THEN ROUND( (random() * ((a.ua + 10) - (a.ua-10)) + (a.ua-10) )::NUMERIC, 2)      
WHEN t1.ua_bs_2020_urban_dense_coverage > 0 AND t1.ua_bs_2020_urban_dense_coverage < a.ua THEN ROUND( (random() * (a.ua  - t1.ua_bs_2020_urban_dense_coverage) + t1.ua_bs_2020_urban_dense_coverage )::NUMERIC, 2)       
ELSE ROUND(t1.ua_bs_2020_urban_dense_coverage ::NUMERIC ,2)       
END       
FROM a   WHERE a.id = t1.id;

WITH a AS (SELECT chunk_nr4536.id FROM chunk_nr4536  WHERE chunk_nr4536.id 
not in (SELECT chunk_nr4536.id from chunk_nr4536, grootams_futureprojects_bs                       
WHERE ST_intersects(chunk_nr4536.geometry, grootams_futureprojects_bs.geometry)))   
UPDATE grootams_cover_analysis SET ua_bs_2025_urban_dense_coverage = ROUND(ua_bs_2020_urban_dense_coverage ::NUMERIC , 2)    
FROM a
WHERE a.id = grootams_cover_analysis.id;

WITH a AS (SELECT chunk_nr4536.id   FROM chunk_nr4536, grootams_futureprojects_bs WHERE ST_intersects(chunk_nr4536.geometry, grootams_futureprojects_bs.geometry)   GROUP BY id)   UPDATE grootams_cover_analysis t1 SET ua_bs_2025_infra_light_coverage = CASE        WHEN t1.ua_bs_2020_urban_dense_coverage = ROUND(t1.ua_bs_2025_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_bs_2020_infra_light_coverage ::NUMERIC,2)       WHEN t1.ua_bs_2020_urban_dense_coverage < t1.ua_bs_2025_urban_dense_coverage THEN ROUND( (random() * (((100 - t1.ua_bs_2025_urban_dense_coverage) - 0) + 0) )::NUMERIC,2)
 END      FROM a   WHERE a.id = t1.id;
WITH a AS (SELECT chunk_nr4536.id FROM chunk_nr4536               WHERE chunk_nr4536.id not in (
                        SELECT chunk_nr4536.id from chunk_nr4536, grootams_futureprojects_bs                       WHERE 
ST_intersects(chunk_nr4536.geometry, grootams_futureprojects_bs.geometry)))   UPDATE grootams_cover_analysis SET ua_bs_2025_infra_light_coverage = ROUND(ua_bs_2020_infra_light_coverage ::NUMERIC , 2)   FROM a   WHERE a.id = grootams_cover_analysis.id;
Chunk number: 4536 took 0.0020205060640970866 minutes to process
Chunk number: 4537 \ 7832 is not empty, Processing...
WITH a AS (SELECT chunk_nr4537.id, max(grootams_futureprojects_bs.bs_2025_max_urbanity) as ua   FROM chunk_nr4537, grootams_futureprojects_bs WHERE ST_intersects(chunk_nr4537.geometry, grootams_futureprojects_bs.geometry)   GROUP BY id)      
   UPDATE grootams_cover_analysis t1 SET ua_bs_2025_urban_dense_coverage =  CASE        WHEN t1.ua_bs_2020_urban_dense_coverage = 0 THEN ROUND( (random() * ((a.ua + 10) - (a.ua-10)) + (a.ua-10) )::NUMERIC, 2)       WHEN t1.ua_bs_2020_urban_dense_coverage > 0 AND t1.ua_bs_2020_urban_dense_coverage < a.ua THEN ROUND( (random() * (a.ua  - t1.ua_bs_2020_urban_dense_coverage) + t1.ua_bs_2020_urban_dense_coverage )::NUMERIC, 2)       ELSE ROUND(t1.ua_bs_2020_urban_dense_coverage ::NUMERIC , 
2)       END       FROM a   WHERE a.id = t1.id;
WITH a AS (SELECT chunk_nr4537.id FROM chunk_nr4537               WHERE chunk_nr4537.id not in (
                        SELECT chunk_nr4537.id from chunk_nr4537, grootams_futureprojects_bs                       WHERE 
ST_intersects(chunk_nr4537.geometry, grootams_futureprojects_bs.geometry)))   UPDATE grootams_cover_analysis SET ua_bs_2025_urban_dense_coverage = ROUND(ua_bs_2020_urban_dense_coverage ::NUMERIC , 2)    FROM a
WHERE a.id = grootams_cover_analysis.id;
WITH a AS (SELECT chunk_nr4537.id   FROM chunk_nr4537, grootams_futureprojects_bs WHERE ST_intersects(chunk_nr4537.geometry, grootams_futureprojects_bs.geometry)   GROUP BY id)   UPDATE grootams_cover_analysis t1 SET ua_bs_2025_infra_light_coverage = CASE        WHEN t1.ua_bs_2020_urban_dense_coverage = ROUND(t1.ua_bs_2025_urban_dense_coverage ::NUMERIC,2) THEN ROUND(t1.ua_bs_2020_infra_light_coverage ::NUMERIC,2)       WHEN t1.ua_bs_2020_urban_dense_coverage < t1.ua_bs_2025_urban_dense_coverage THEN ROUND( (random() * (((100 - t1.ua_bs_2025_urban_dense_coverage) - 0) + 0) )::NUMERIC,2)
 END      FROM a   WHERE a.id = t1.id;
WITH a AS (SELECT chunk_nr4537.id FROM chunk_nr4537               WHERE chunk_nr4537.id not in (
                        SELECT chunk_nr4537.id from chunk_nr4537, grootams_futureprojects_bs                       WHERE 
ST_intersects(chunk_nr4537.geometry, grootams_futureprojects_bs.geometry)))   UPDATE grootams_cover_analysis SET ua_bs_2025_infra_light_coverage = ROUND(ua_bs_2020_infra_light_coverage ::NUMERIC , 2)   FROM a   WHERE a.id = grootams_cover_analysis.id;


Alter table cph_residential_process3 
                ADD column prices_av_2025 double precision default 0;
				
WITH a AS (
	Select fid, avg(prices2_2025) as pr_2025 from cph_residential_process3 
	group by fid )
UPDATE cph_residential_process3 SET  prices_av_2025 = ROUND(pr_2025 ::NUMERIC , 2)  
                            FROM a 
                            WHERE a.fid = cph_residential_process3.fid;

Select fid,name, comment,geom, avg(year):: int as year, avg(year_bs):: int as year_bs,  avg(year_zms):: int as year_zms,
	avg(floors) :: int as  floors, 
	avg(housing) :: int as housing, avg("housingArea") :: int as housingArea, avg(_existinghousing) :: int as existinghousing, 
	avg(spgnprices_sogns2_2008_meanprice):: int as prices_2008, avg(spgnprices_sogns2_2018_meanprice):: int as prices_2018,
	avg(prices2_2025):: int as prices_2025, avg(prices2_2030):: int as prices_2030, avg(prices2_2035):: int as prices_2035, 
	avg(prices2_2040) :: int as prices_2040, avg(prices2_2045) :: int as prices_2045, avg(prices2_2050) :: int as prices_2050 from cph_residential_process3 
	group by fid, name, comment, geom