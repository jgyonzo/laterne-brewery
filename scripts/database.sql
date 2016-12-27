create database Temperaturas;

use Temperaturas;

CREATE TABLE temps4 ( temp1 FLOAT, temp2 FLOAT, temp3 FLOAT, temp4 FLOAT, temp5 FLOAT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

insert into temps4 (temp1,temp2,temp3,temp4,temp5) values (3.5,3.5,3.5,3.5,3.5);