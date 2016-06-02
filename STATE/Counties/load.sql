DROP TABLE IF EXISTS mississippi_counties;

CREATE TABLE mississippi_counties (
  fips varchar(20),
  count varchar(20)



);


LOAD DATA INFILE '~/Desktop/SuperH/STATE/Counties/mississippi_counties.csv'
INTO TABLE mississippi_counties
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 0 ROWS;
