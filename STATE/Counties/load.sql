DROP TABLE IF EXISTS texas_counties;

CREATE TABLE texas_counties (
  fips varchar(20),
  count varchar(20)



);


LOAD DATA INFILE '~/Desktop/SuperH/STATE/Counties/texas_counties.csv'
INTO TABLE texas_counties
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 0 ROWS;
