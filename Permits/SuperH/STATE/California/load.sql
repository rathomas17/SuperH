DROP TABLE IF EXISTS California;

CREATE TABLE California (
ID varchar(10),
Facility varchar(50),
Location varchar(20),
County varchar(10),
Initial varchar(40),
Renewal varchar(40),
Fips varchar(10)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/California/California.csv'
INTO TABLE California
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
