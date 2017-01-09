from w1thermsensor import W1ThermSensor

import pymysql.cursors
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
from datetime import timedelta

#pines para valvula
output_pin_1 = 16 #Valvula sensor 1. GPIO23
output_pin_2 = 12 #Valvula sensor 2. GPIO18
output_pin_3 = 11 #Valvula sensor 3. GPIO17
output_pin_4 = 13 #Valvula sensor 4. GPIO27
output_pin_5 = 15 #Valvula sensor 5. GPIO22
pump_pin = 40 #Bomba. GPIO21
output_pin_chiller = 11 #Rele banco de frio CHANGEME
output_pin_cold_room = 11 #Rele camara de frio CHANGEME

temp_sens_1 = 25 #FV1
temp_sens_2 = 25 #FV2
temp_sens_3 = 25 #BBT1
temp_sens_4 = 25 #BBT2
temp_sens_5 = 25 #FV3

temp_chiller = 10 #banco de frio temp CHANGEME
temp_cold_room = 10 #camara de frio temp CHANGEME

timer_on_chiller = 6 #tiempo de prendido de banco de frio en horas
timer_on_cold_room = 6  #tiempo de prendido de camara de frio en horas
timer_off_chiller = 0.5 #tiempo de apagado de banco de frio en horas
timer_off_cold_room = 0.5 #tiempo de apagado de banco de frio en horas

tolerancia = 0.3

read_interval = 5 #in seconds

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(output_pin_1, GPIO.OUT)
GPIO.setup(output_pin_2, GPIO.OUT)
GPIO.setup(output_pin_3, GPIO.OUT)
GPIO.setup(output_pin_4, GPIO.OUT)
GPIO.setup(output_pin_5, GPIO.OUT)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.setup(output_pin_chiller, GPIO.OUT)
GPIO.setup(output_pin_cold_room, GPIO.OUT)

GPIO.output(output_pin_1, True)
GPIO.output(output_pin_2, True)
GPIO.output(output_pin_3, True)
GPIO.output(output_pin_4, True)
GPIO.output(output_pin_5, True)
GPIO.output(output_pin_chiller, True)
GPIO.output(output_pin_cold_room, True)

#Para tener en cuenta: si no encuentra el sensor, rompe el script. Esto deberia
#no importar cuando se haga el refactor y detecte los sensores con listsensor
sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c24fafff")
sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2ac01ff")
sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000028104d")
sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c2a10cff")
sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff")

sensorChiller = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff") #CHANGEME
sensorColdRoom = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff") #CHANGEME

while True:
    try:
        #Init temporal variables
        sensor1_temp = 0.0
        sensor2_temp = 0.0
        sensor3_temp = 0.0
        sensor4_temp = 0.0
        sensor5_temp = 0.0
        sensorChiller_temp = 0.0
        sensorColdRoom_temp = 0.0

        output_1_val = True
        output_2_val = True
        output_3_val = True
        output_4_val = True
        output_5_val = True
        output_pump_val = True
        output_chiller_val = True
        output_cold_room_val = True

        force_chiller_off = False
        force_cold_room_off = False
        restart_chiller_date = False
        restart_cold_room_date = False

        #Read sensors
        try:
            sensor1_temp = sensor1.get_temperature()
        except:
            print("ERROR READING SENSOR 1")

        try:
            sensor2_temp = sensor2.get_temperature()
        except:
            print("ERROR READING SENSOR 2")

        try:    
            sensor3_temp = sensor3.get_temperature()
        except:
            print("ERROR READING SENSOR 3")

        try:
            sensor4_temp = sensor4.get_temperature()
        except:
            print("ERROR READING SENSOR 4")

        try:
            sensor5_temp = sensor5.get_temperature()
        except:
            print("ERROR READING SENSOR 5")

        try:
            sensorChiller_temp = sensorChiller.get_temperature()
        except:
            print("ERROR READING SENSOR CHILLER")
        
        try:
            sensorColdRoom_temp = sensorColdRoom.get_temperature()
        except:
            print("ERROR READING SENSOR COLD ROOM")

        print("Sensor 1 temp %.2f" % sensor1_temp)
        print("Sensor 2 temp %.2f" % sensor2_temp)
        print("Sensor 3 temp %.2f" % sensor3_temp)
        print("Sensor 4 temp %.2f" % sensor4_temp)
        print("Sensor 5 temp %.2f" % sensor5_temp)
        print("Sensor chiller temp %.2f" % sensorChiller_temp)
        print("Sensor cold room temp %.2f" % sensorColdRoom_temp)

        output_1_val = False if (sensor1_temp >= (temp_sens_1 + tolerancia)) else True if (sensor1_temp <= (temp_sens_1 - tolerancia)) else output_1_val
        output_2_val = False if (sensor2_temp >= (temp_sens_2 + tolerancia)) else True if (sensor2_temp <= (temp_sens_2 - tolerancia)) else output_2_val
        output_3_val = False if (sensor3_temp >= (temp_sens_3 + tolerancia)) else True if (sensor3_temp <= (temp_sens_3 - tolerancia)) else output_3_val
        output_4_val = False if (sensor4_temp >= (temp_sens_4 + tolerancia)) else True if (sensor4_temp <= (temp_sens_4 - tolerancia)) else output_4_val
        output_5_val = False if (sensor5_temp >= (temp_sens_5 + tolerancia)) else True if (sensor5_temp <= (temp_sens_5 - tolerancia)) else output_5_val

        output_pump_val = output_1_val and output_2_val and output_3_val and output_4_val and output_5_val 

        GPIO.output(output_pin_1, output_1_val)
        GPIO.output(output_pin_2, output_2_val)
        GPIO.output(output_pin_3, output_3_val)
        GPIO.output(output_pin_4, output_4_val)
        GPIO.output(output_pin_5, output_5_val)
        GPIO.output(pump_pin, output_pump_val)

        print("Output 1 on? --> ", not output_1_val)
        print("Output 2 on? --> ", not output_2_val)
        print("Output 3 on? --> ", not output_3_val)
        print("Output 4 on? --> ", not output_4_val)
        print("Output 5 on? --> ", not output_5_val)
        print("Pump on? --> ", not output_pump_val)

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='raspberry',
                                     db='Temperaturas',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                #cursor.execute("""INSERT INTO temps (temp1,temp2) VALUES (%s,%s) """,(sensor1_temp,sensor2_temp))
                cursor.execute("""UPDATE temps4 SET temp1 = %s,temp2 = %s, temp3 = %s, temp4 = %s, temp5 = %s, temp1_cfg = %s, temp2_cfg = %s, temp3_cfg = %s, temp4_cfg = %s, temp5_cfg = %s, output1 = %s, output2 = %s, output3 = %s, output4 = %s, output5 = %s WHERE 1=1 """,(sensor1_temp,sensor2_temp,sensor3_temp,sensor4_temp,sensor5_temp,
                                                   temp_sens_1,temp_sens_2,temp_sens_3,temp_sens_4,temp_sens_5,
                                                   output_1_val, output_2_val, output_3_val, output_4_val, output_5_val 
                                                   ))

            connection.commit()

        finally:
            connection.close()


        #Logica de camara y banco de frio
        #Primero chequeo la ultima hora de start de cada uno en la base:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='raspberry',
                                     db='Temperaturas',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT last_start_cold_room, last_start_chiller FROM temps_cold""")
                for (last_start_cold_room, last_start_chiller) in cursor:
                    #check timers
                    time_chiller_to_stop = last_start_chiller + timedelta(hours=timer_on_chiller)
                    time_cold_room_to_stop = last_start_cold_room + timedelta(hours=timer_on_cold_room)
                    time_chiller_to_start_again = time_chiller_to_stop + timedelta(minutes=timer_off_chiller)
                    time_cold_room_to_start_again = time_cold_room_to_stop + timedelta(minutes=timer_off_cold_room)
                    now = datetime.now()
                    if (time_chiller_to_stop <= now and time_chiller_to_start_again >= now)
                        force_chiller_off = True
                    if (time_cold_room_to_stop <= now and time_cold_room_to_start_again >= now)
                        force_cold_room_off = True
                    if (time_chiller_to_stop <= now and time_chiller_to_start_again <= now)
                        restart_chiller_date = True
                    if (time_cold_room_to_stop <= now and time_cold_room_to_start_again <= now)
                        restart_cold_room_date = True
                        
        finally:
            connection.close()


        if (force_chiller_off)
            output_chiller_val = True
        else
            output_chiller_val = False if (sensorChiller_temp >= (temp_chiller + tolerancia)) else True if (sensorChiller_temp <= (temp_chiller - tolerancia)) else output_chiller_val

        if (force_cold_room_off)
            output_cold_room_val = True
        else
            output_cold_room_val = False if (sensorColdRoom_temp >= (temp_cold_room + tolerancia)) else True if (sensorColdRoom_temp <= (temp_cold_room - tolerancia)) else output_cold_room_val

        GPIO.output(output_pin_chiller, output_chiller_val)
        GPIO.output(output_pin_cold_room, output_cold_room_val)

        print("Chiller on? --> ", not output_pin_chiller)
        print("Cold room on? --> ", not output_cold_room_val)
        print("Chiller defrost? --> ", force_chiller_off)
        print("Cold room defrost? --> ", force_cold_room_off)
        print("restart chiller date in DB? --> ", restart_chiller_date)
        print("restart cold room date in DB? --> ", restart_cold_room_date)

        #update chiller and cold room values in DB
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='raspberry',
                                     db='Temperaturas',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE temps_cold SET temp_cold_room = %s,temp_chiller = %s, temp_chiller_cfg = %s, temp_cold_room_cfg = %s, output_chiller = %s, output_cold_room = %s, timer_off_chiller = %s, timer_off_cold_room = %s WHERE 1=1 """,
                                                    (sensorColdRoom_temp,sensorChiller_temp,
                                                   temp_chiller,temp_cold_room,
                                                   output_chiller_val, output_cold_room_val,
                                                   force_chiller_off, force_cold_room_off 
                                                   ))
                if (restart_chiller_date)
                    cursor.execute("""UPDATE temps_cold SET last_start_chiller = %s""", datetime.now())
                if (restart_cold_room_date)
                    cursor.execute("""UPDATE temps_cold SET last_start_cold_room = %s""", datetime.now())

            connection.commit()

        finally:
            connection.close()

        time.sleep(read_interval)
    except:
        print("Unexpected error:", sys.exc_info()[0])
