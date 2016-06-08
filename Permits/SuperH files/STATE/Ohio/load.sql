DROP TABLE IF EXISTS Ohio;

CREATE TABLE Ohio (
Facility varchar(20),
FacilityName varchar(100),
Address varchar(100),
City varchar(100),
State varchar(2),
Zipcode varchar(5),
County varchar(20),
PermitType varchar(40),
PermitDescription varbinary(3000),
InsuranceType varchar(20),
Reason varchar(20),
PermitNumber varchar(20),
IssuanceDate varchar(20),
PDFDocumentID  varchar(15)
);

LOAD DATA LOCAL INFILE '~/Desktop/SuperH/STATE/Ohio/ohio.csv'
INTO TABLE Ohio
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
