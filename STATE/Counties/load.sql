DROP TABLE IF EXISTS Counties;

CREATE TABLE Counties (
  Type varchar(10),
  fips varchar(5),
  name varchar(40)



);


LOAD DATA INFILE '~/Desktop/SuperH/STATE/Counties/Counties.csv'
INTO TABLE Counties
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
