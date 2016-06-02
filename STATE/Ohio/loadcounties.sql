DROP TABLE IF EXISTS ohio_counties;

CREATE TABLE ohio_counties (
fips varchar(20),
count varchar(20)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/Ohio/ohio_counties.csv'
INTO TABLE ohio_counties
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 0 ROWS;
