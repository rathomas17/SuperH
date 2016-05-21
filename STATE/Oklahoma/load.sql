DROP TABLE IF EXISTS Texas;

CREATE TABLE Texas (
Name varchar(200),
Num varchar(50),
EPAreviewStart varchar(20),
EPAreviewEnd varchar(20),
60DayPetitionStart varchar(20),
60DayPetitionEnd varchar(20),
Comment varchar(100)
);

LOAD DATA LOCAL INFILE '~/Desktop/SuperH/STATE/Texas/Texas.csv'
INTO TABLE Texas
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
