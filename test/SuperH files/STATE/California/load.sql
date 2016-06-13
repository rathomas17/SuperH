DROP TABLE IF EXISTS California;

CREATE TABLE California (
Facility varchar(200),
State varchar(50),
Location varchar(20),
Type varchar(100),
Status varchar(100),
Related_Documents varchar(200)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/California/California.csv'
INTO TABLE California
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
