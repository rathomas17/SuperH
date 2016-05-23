DROP TABLE IF EXISTS Arizona;

CREATE TABLE Arizona (
  Facility varchar(200),
  State varchar(50),
  Location varchar(20),
  Type varchar(100),
  Status varchar(100),
  Related_Documents varchar(200)
  );

LOAD DATA INFILE '~/Desktop/SuperH/STATE/Arizona/Arizona.csv'
INTO TABLE Arizona
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
