DROP TABLE IF EXISTS Louisiana;

CREATE TABLE Louisiana (
Name varchar(200),
Num varchar(50),
EPAreviewStart varchar(20),
EPAreviewEnd varchar(20),
60DayPetitionStart varchar(20),
60DayPetitionEnd varchar(20),
Comment varchar(100)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/Louisiana/Louisiana.csv'
INTO TABLE Louisiana
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
