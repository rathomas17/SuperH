DROP TABLE IF EXISTS New_Mexico;

CREATE TABLE New_Mexico (
Name varchar(200),
Num varchar(50),
EPAreviewStart varchar(20),
EPAreviewEnd varchar(20),
60DayPetitionStart varchar(20),
60DayPetitionEnd varchar(20),
Comment varchar(100)
);

LOAD DATA INFILE '~/Desktop/SuperH/STATE/NewMexico/newmexico.csv'
INTO TABLE New_Mexico
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
