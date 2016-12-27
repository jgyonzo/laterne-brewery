from w1thermsensor import W1ThermSensor

import pymysql.cursors
import RPi.GPIO as GPIO
import time

#pines para valvula
output_pin_1 = 16 #Valvula sensor 1. GPIO23
output_pin_2 = 12 #Valvula sensor 2. GPIO18
output_pin_3 = 11 #Valvula sensor 3. GPIO17
output_pin_4 = 13 #Valvula sensor 4. GPIO27
output_pin_5 = 15 #Valvula sensor 5. GPIO22
pump_pin = 7 #Bomba. GPIO4

temp_sens_1 = 22 #FV1
temp_sens_2 = 22 #FV2
temp_sens_3 = 22 #BBT1
temp_sens_4 = 22 #BBT2
temp_sens_5 = 22 #FV3

tolerancia = 0.3

read_interval = 5 #in seconds

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(output_pin_1, GPIO.OUT)
GPIO.setup(output_pin_2, GPIO.OUT)
GPIO.setup(output_pin_3, GPIO.OUT)
GPIO.setup(output_pin_4, GPIO.OUT)
GPIO.setup(output_pin_5, GPIO.OUT)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.output(output_pin_1, False)
GPIO.output(output_pin_2, False)
GPIO.output(output_pin_3, False)
GPIO.output(output_pin_4, False)
GPIO.output(output_pin_5, False)
GPIO.output(pump_pin, False)


sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c24fafff")
sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2ac01ff")
sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000028104d")
sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c2a10cff")
sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff")


sensor1_temp = 0.0
sensor2_temp = 0.0
sensor3_temp = 0.0
sensor4_temp = 0.0
sensor5_temp = 0.0

while True:
    try:
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

        print("Sensor 1 temp %.2f" % sensor1_temp)
        print("Sensor 2 temp %.2f" % sensor2_temp)
        print("Sensor 3 temp %.2f" % sensor3_temp)
        print("Sensor 4 temp %.2f" % sensor4_temp)
        print("Sensor 5 temp %.2f" % sensor5_temp)
        
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
                cursor.execute("""UPDATE temps4 SET temp1 = %s,temp2 = %s, temp3 = %s, temp4 = %s, temp5 = %s WHERE 1=1 """,(sensor1_temp,sensor2_temp,sensor3_temp,sensor4_temp,sensor5_temp))

            connection.commit()

        finally:
            connection.close()

        pump_aux_flag = False
        
        if sensor1_temp >= (temp_sens_1 + tolerancia):
            GPIO.output(output_pin_1, True)
            pump_aux_flag = True
            print("ON output 1")
        elif sensor1_temp <= (temp_sens_1 - tolerancia):
            GPIO.output(output_pin_1, False)
            print("OFF output 1")

        if sensor2_temp >= (temp_sens_2 + tolerancia):
            GPIO.output(output_pin_2, True)
            pump_aux_flag = True
            print("ON output 2")
        elif sensor2_temp <= (temp_sens_2 - tolerancia):
            GPIO.output(output_pin_2, False)
            print("OFF output 2")

        if sensor3_temp >= (temp_sens_3 + tolerancia):
            GPIO.output(output_pin_3, True)
            pump_aux_flag = True
            print("ON output 3")
        elif sensor3_temp <= (temp_sens_3 - tolerancia):
            GPIO.output(output_pin_3, False)
            print("OFF output 3")

        if sensor4_temp >= (temp_sens_4 + tolerancia):
            GPIO.output(output_pin_4, True)
            pump_aux_flag = True
            print("ON output 4")
        elif sensor4_temp <= (temp_sens_4 - tolerancia):
            GPIO.output(output_pin_4, False)
            print("OFF output 4")

        if sensor5_temp >= (temp_sens_5 + tolerancia):
            GPIO.output(output_pin_5, True)
            pump_aux_flag = True
            print("ON output 5")
        elif sensor5_temp <= (temp_sens_5 - tolerancia):
            GPIO.output(output_pin_5, False)
            print("OFF output 5")

        GPIO.output(pump_pin, pump_aux_flag)

        time.sleep(read_interval)
    except:
        print("GENERIC ERROR");
