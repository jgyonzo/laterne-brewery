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
pump_pin = 40 #Bomba. GPIO21

temp_sens_1 = 25 #FV1
temp_sens_2 = 25 #FV2
temp_sens_3 = 25 #BBT1
temp_sens_4 = 25 #BBT2
temp_sens_5 = 25 #FV3

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
GPIO.output(output_pin_1, True)
GPIO.output(output_pin_2, True)
GPIO.output(output_pin_3, True)
GPIO.output(output_pin_4, True)
GPIO.output(output_pin_5, True)
GPIO.output(pump_pin, True)

#Para tener en cuenta: si no encuentra el sensor, rompe el script. Esto deberia
#no importar cuando se haga el refactor y detecte los sensores con listsensor
sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c24fafff")
sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2ac01ff")
sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000028104d")
sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c2a10cff")
sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff")

while True:
    try:
        #Init temporal variables
        sensor1_temp = 0.0
        sensor2_temp = 0.0
        sensor3_temp = 0.0
        sensor4_temp = 0.0
        sensor5_temp = 0.0
        output_1_val = True
        output_2_val = True
        output_3_val = True
        output_4_val = True
        output_5_val = True
        output_pump_val = True

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

        print("Sensor 1 temp %.2f" % sensor1_temp)
        print("Sensor 2 temp %.2f" % sensor2_temp)
        print("Sensor 3 temp %.2f" % sensor3_temp)
        print("Sensor 4 temp %.2f" % sensor4_temp)
        print("Sensor 5 temp %.2f" % sensor5_temp)

        output_1_val = False if (sensor1_temp >= (temp_sens_1 + tolerancia)) else True if (sensor1_temp <= (temp_sens_1 - tolerancia)) else output_1_val
        output_2_val = False if (sensor2_temp >= (temp_sens_2 + tolerancia)) else True if (sensor2_temp <= (temp_sens_2 - tolerancia)) else output_2_val
        output_3_val = False if (sensor3_temp >= (temp_sens_3 + tolerancia)) else True if (sensor3_temp <= (temp_sens_3 - tolerancia)) else output_3_val
        output_4_val = False if (sensor4_temp >= (temp_sens_4 + tolerancia)) else True if (sensor4_temp <= (temp_sens_4 - tolerancia)) else output_4_val
        output_5_val = False if (sensor5_temp >= (temp_sens_5 + tolerancia)) else True if (sensor5_temp <= (temp_sens_5 - tolerancia)) else output_5_val

        output_pump_val = not output_1_val or not output_2_val or not output_3_val or not output_4_val or not output_5_val 

        GPIO.output(output_pin_1, output_1_val)
        GPIO.output(output_pin_2, output_2_val)
        GPIO.output(output_pin_3, output_3_val)
        GPIO.output(output_pin_4, output_4_val)
        GPIO.output(output_pin_5, output_5_val)
        GPIO.output(pump_pin, pump_aux_flag)

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
                cursor.execute("""UPDATE temps4 SET temp1 = %s,temp2 = %s, temp3 = %s, temp4 = %s, temp5 = %s,
                                    temp1_cfg = %s, temp2_cfg = %s, temp3_cfg = %s, temp4_cfg = %s, temp5_cfg = %s,
                                    output1 = %s, output2 = %s, output3 = %s, output4 = %s, output5 = %s, 
                                    WHERE 1=1 """,(sensor1_temp,sensor2_temp,sensor3_temp,sensor4_temp,sensor5_temp,
                                                   temp_sens_1,temp_sens_2,temp_sens_3,temp_sens_4,temp_sens_5,
                                                   output_1_val, output_2_val, output_3_val, output_4_val, output_5_val 
                                                   ))

            connection.commit()

        finally:
            connection.close()

        time.sleep(read_interval)
    except:
        print("GENERIC ERROR");
