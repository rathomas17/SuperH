DROP TABLE IF EXISTS Oklahoma;

CREATE TABLE Oklahoma (
Name varchar(200),
Num varchar(50),
EPAreviewStart varchar(20),
EPAreviewEnd varchar(20),
60DayPetitionStart varchar(20),
60DayPetitionEnd varchar(20),
Comment varbinary(1000)
);

LOAD DATA LOCAL INFILE '~/Desktop/SuperH/STATE/Oklahoma/Oklahoma.csv'
INTO TABLE Oklahoma
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
