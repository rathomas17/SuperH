DROP TABLE IF EXISTS Arkansas;

CREATE TABLE Arkansas (
Name varchar(200),
Num varchar(50),
EPAreviewStart varchar(20),
EPAreviewEnd varchar(20),
60DayPetitionStart varchar(20),
60DayPetitionEnd varchar(20),
Comment varbinary(200)
);

LOAD DATA LOCAL INFILE '~/Desktop/SuperH/STATE/Arkansas/Arkansas.csv'
INTO TABLE Arkansas
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
