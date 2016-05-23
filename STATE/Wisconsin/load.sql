DROP TABLE IF EXISTS Wisconsin;

CREATE TABLE Wisconsin (
FID varchar(15),
Facility varbinary(200),
Address varchar(100),
City varchar(100),
County varchar(100)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/Wisconsin/Wisconsin.csv'
INTO TABLE Wisconsin
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
