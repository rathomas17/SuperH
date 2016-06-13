DROP TABLE IF EXISTS Georgia;

CREATE TABLE Georgia (
AIRS_number varchar(10),
Facility varchar(200),
Issuance_Date varchar(20),
Final_Permit varchar(100),
Narrative varchar(100),
Permit_Type varchar(50)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/Georgia/Georgia.csv'
INTO TABLE Georgia
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
