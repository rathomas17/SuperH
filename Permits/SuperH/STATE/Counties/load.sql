DROP TABLE IF EXISTS california_counties;

CREATE TABLE california_counties (
  fips varchar(5),
  count varchar(10),
  name varchar(20)



);


LOAD DATA INFILE '~/Desktop/SuperH/STATE/Counties/california_counties.csv'
INTO TABLE california_counties
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 0 ROWS;
