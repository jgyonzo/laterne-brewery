create database Temperaturas;

use Temperaturas;

CREATE TABLE temps4 ( temp1 FLOAT, temp2 FLOAT, temp3 FLOAT, temp4 FLOAT, temp5 FLOAT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

insert into temps4 (temp1,temp2,temp3,temp4,temp5) values (3.5,3.5,3.5,3.5,3.5);

alter table temps4 ADD temp6 FLOAT, ADD temp7 FLOAT, ADD temp8 FLOAT, ADD temp6_cfg FLOAT, ADD temp7_cfg FLOAT, ADD temp8_cfg FLOAT, ADD output6 INTEGER, ADD output7 INTEGER, ADD output8 INTEGER;

alter table temps4 ADD temp11 FLOAT, ADD temp12 FLOAT, ADD temp11_cfg FLOAT, ADD temp12_cfg FLOAT, ADD output11 INTEGER, ADD output12 INTEGER;