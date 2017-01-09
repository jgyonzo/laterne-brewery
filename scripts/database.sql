create database Temperaturas;

use Temperaturas;

CREATE TABLE temps4 ( temp1 FLOAT, temp2 FLOAT, temp3 FLOAT, temp4 FLOAT, temp5 FLOAT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

insert into temps4 (temp1,temp2,temp3,temp4,temp5) values (3.5,3.5,3.5,3.5,3.5);

CREATE TABLE temps_cold ( temp_cold_room FLOAT, temp_chiller FLOAT, last_start_cold_room TIMESTAMP, last_start_chiller TIMESTAMP, temp_cold_room_cfg FLOAT, temp_chiller_cfg FLOAT, output_chiller INT, output_cold_room INT, timer_off_chiller INT, timer_off_cold_room INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );