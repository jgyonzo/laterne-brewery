from w1thermsensor import W1ThermSensor

import pymysql.cursors
import RPi.GPIO as GPIO
import time
import sys

#pines para valvula
output_pin_1 = 16 #Valvula sensor 1. GPIO23
output_pin_2 = 12 #Valvula sensor 2. GPIO18
output_pin_3 = 11 #Valvula sensor 3. GPIO17
output_pin_4 = 13 #Valvula sensor 4. GPIO27
output_pin_5 = 15 #Valvula sensor 5. GPIO22
output_pin_6 = 29  #Valvula sensor 6. GPIO5
output_pin_7 = 31 #Valvula sensor 7. GPIO6
output_pin_8 = 33 #Valvula sensor 8. GPIO13
#output_pin_9 =  #AMBIENT. No usa
#output_pin_10 =  #

output_pin_banco_frio = 36 #Rele banco de frio. GPIO16
output_pin_camara_frio = 32 #Rele camara de frio. GPIO12

pump_pin = 40 #Bomba. GPIO21

temp_sens_1 = 21 #FV1
temp_sens_2 = 21 #FV2
temp_sens_3 = 1 #BBT1
temp_sens_4 = 5 #BBT2
temp_sens_5 = 23 #FV3
temp_sens_6 = 21 #FV4 temp8
temp_sens_7 = 21 #FV5 temp9
temp_sens_8 = 21 #FV6 temp10
#temp_sens_9 = 0 #AMBIENT temp11. No usa, solo guarda
#temp_sens_10 = 0 #disponible temp12

temp_sens_banco_frio = 1
temp_sens_camara_frio = 10

tolerancia = 0

read_interval = 30 #in seconds

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(output_pin_1, GPIO.OUT)
GPIO.setup(output_pin_2, GPIO.OUT)
GPIO.setup(output_pin_3, GPIO.OUT)
GPIO.setup(output_pin_4, GPIO.OUT)
GPIO.setup(output_pin_5, GPIO.OUT)
GPIO.setup(output_pin_6, GPIO.OUT)
GPIO.setup(output_pin_7, GPIO.OUT)
GPIO.setup(output_pin_8, GPIO.OUT)
#GPIO.setup(output_pin_9, GPIO.OUT)
#GPIO.setup(output_pin_10, GPIO.OUT)
GPIO.setup(output_pin_banco_frio, GPIO.OUT)
GPIO.setup(output_pin_camara_frio, GPIO.OUT)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.output(output_pin_1, True)
GPIO.output(output_pin_2, True)
GPIO.output(output_pin_3, True)
GPIO.output(output_pin_4, True)
GPIO.output(output_pin_5, True)
GPIO.output(output_pin_6, True)
GPIO.output(output_pin_7, True)
GPIO.output(output_pin_8, True)
#GPIO.output(output_pin_9, True)
#GPIO.output(output_pin_10, True)
GPIO.output(output_pin_banco_frio, True)
GPIO.output(output_pin_camara_frio, True)
GPIO.output(pump_pin, True)

#Para tener en cuenta: si no encuentra el sensor, rompe el script. Esto deberia
#no importar cuando se haga el refactor y detecte los sensores con listsensor
try:
    sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c24fafff")
except Exception as e:
    print("ERROR READING SENSOR 1")
try:
    sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2ac01ff")
except Exception as e:
    print("ERROR READING SENSOR 2")
try:
    sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000028104d")
except Exception as e:
    print("ERROR READING SENSOR 3")
try:
    sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c2a10cff")
except Exception as e:
    print("ERROR READING SENSOR 4")
try:
    sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0115c2a8a1ff")
except Exception as e:
    print("ERROR READING SENSOR 5")
try:
    sensor6 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "")
except Exception as e:
    print("ERROR READING SENSOR 6")
try:
    sensor7 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "")
except Exception as e:
    print("ERROR READING SENSOR 7")
try:
    sensor8 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "")
except Exception as e:
    print("ERROR READING SENSOR 8")
try:
    sensor9 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "")
except Exception as e:
    print("ERROR READING SENSOR 9")
# try:
#     sensor10 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "")
# except Exception as e:
#     print("ERROR READING SENSOR 10")
try:
    sensorBancoFrio = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c23d9eff")
except Exception as e:
    print("ERROR READING SENSOR Banco Frio")
try:
    sensorCamaraFrio = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0215c28f00ff")
except Exception as e:
    print("ERROR READING SENSOR Camara Frio")

while True:
    try:
        #Init temporal variables
        sensor1_temp = 0.0
        sensor2_temp = 0.0
        sensor3_temp = 0.0
        sensor4_temp = 0.0
        sensor5_temp = 0.0
        sensor6_temp = 0.0
        sensor7_temp = 0.0
        sensor8_temp = 0.0
        sensor9_temp = 0.0
        # sensor10_temp = 0.0
        sensorBancoFrio_temp = 0.0
        sensorCamaraFrio_temp = 0.0
        output_1_val = True
        output_2_val = True
        output_3_val = True
        output_4_val = True
        output_5_val = True
        output_6_val = True
        output_7_val = True
        output_8_val = True
#        output_9_val = True
        # output_10_val = True
        output_banco_frio_val = True
        output_camara_frio_val = True
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

        try:
            sensor6_temp = sensor6.get_temperature()
        except:
            print("ERROR READING SENSOR 6")

        try:
            sensor7_temp = sensor7.get_temperature()
        except:
            print("ERROR READING SENSOR 7")

        try:    
            sensor8_temp = sensor8.get_temperature()
        except:
            print("ERROR READING SENSOR 8")

        try:
            sensor9_temp = sensor9.get_temperature()
        except:
            print("ERROR READING SENSOR 9")

        # try:
        #     sensor10_temp = sensor10.get_temperature()
        # except:
        #     print("ERROR READING SENSOR 10")

        try:
            sensorBancoFrio_temp = sensorBancoFrio.get_temperature()
        except:
            print("ERROR READING SENSOR Banco Frio")

        try:
            sensorCamaraFrio_temp = sensorCamaraFrio.get_temperature()
        except:
            print("ERROR READING SENSOR Camara Frio")

        print("Sensor 1 temp %.2f" % sensor1_temp)
        print("Sensor 2 temp %.2f" % sensor2_temp)
        print("Sensor 3 temp %.2f" % sensor3_temp)
        print("Sensor 4 temp %.2f" % sensor4_temp)
        print("Sensor 5 temp %.2f" % sensor5_temp)
        print("Sensor 6 temp %.2f" % sensor6_temp)
        print("Sensor 7 temp %.2f" % sensor7_temp)
        print("Sensor 8 temp %.2f" % sensor8_temp)
        print("Sensor 9 temp %.2f" % sensor9_temp)
        # print("Sensor 10 temp %.2f" % sensor10_temp)
        print("Sensor Banco Frio temp %.2f" % sensorBancoFrio_temp)
        print("Sensor Camara Frio temp %.2f" % sensorCamaraFrio_temp)

        output_1_val = False if (sensor1_temp >= (temp_sens_1 + tolerancia)) else True if (sensor1_temp <= (temp_sens_1 - tolerancia)) else output_1_val
        output_2_val = False if (sensor2_temp >= (temp_sens_2 + tolerancia)) else True if (sensor2_temp <= (temp_sens_2 - tolerancia)) else output_2_val
        output_3_val = False if (sensor3_temp >= (temp_sens_3 + tolerancia)) else True if (sensor3_temp <= (temp_sens_3 - tolerancia)) else output_3_val
        output_4_val = False if (sensor4_temp >= (temp_sens_4 + tolerancia)) else True if (sensor4_temp <= (temp_sens_4 - tolerancia)) else output_4_val
        output_5_val = False if (sensor5_temp >= (temp_sens_5 + tolerancia)) else True if (sensor5_temp <= (temp_sens_5 - tolerancia)) else output_5_val
        output_6_val = False if (sensor6_temp >= (temp_sens_6 + tolerancia)) else True if (sensor6_temp <= (temp_sens_6 - tolerancia)) else output_6_val
        output_7_val = False if (sensor7_temp >= (temp_sens_7 + tolerancia)) else True if (sensor7_temp <= (temp_sens_7 - tolerancia)) else output_7_val
        output_8_val = False if (sensor8_temp >= (temp_sens_8 + tolerancia)) else True if (sensor8_temp <= (temp_sens_8 - tolerancia)) else output_8_val
#        output_9_val = False if (sensor9_temp >= (temp_sens_9 + tolerancia)) else True if (sensor9_temp <= (temp_sens_9 - tolerancia)) else output_9_val
        # output_10_val = False if (sensor10_temp >= (temp_sens_10 + tolerancia)) else True if (sensor10_temp <= (temp_sens_10 - tolerancia)) else output_10_val
        output_banco_frio_val = False if (sensorBancoFrio_temp >= (temp_sens_banco_frio + tolerancia)) else True if (sensorBancoFrio_temp <= (temp_sens_banco_frio - tolerancia)) else output_banco_frio_val
        output_camara_frio_val = False if (sensorCamaraFrio_temp >= (temp_sens_camara_frio + tolerancia)) else True if (sensorCamaraFrio_temp <= (temp_sens_camara_frio - tolerancia)) else output_camara_frio_val

        output_pump_val = output_1_val and output_2_val and output_3_val and output_4_val and output_5_val 

        GPIO.output(output_pin_1, output_1_val)
        GPIO.output(output_pin_2, output_2_val)
        GPIO.output(output_pin_3, output_3_val)
        GPIO.output(output_pin_4, output_4_val)
        GPIO.output(output_pin_5, output_5_val)
        GPIO.output(output_pin_6, output_6_val)
        GPIO.output(output_pin_7, output_7_val)
        GPIO.output(output_pin_8, output_8_val)
#        GPIO.output(output_pin_9, output_9_val)
        # GPIO.output(output_pin_10, output_10_val)
        GPIO.output(output_pin_banco_frio, output_banco_frio_val)
        GPIO.output(output_pin_camara_frio, output_camara_frio_val)
        GPIO.output(pump_pin, output_pump_val)

        print("Output 1 on? --> ", not output_1_val)
        print("Output 2 on? --> ", not output_2_val)
        print("Output 3 on? --> ", not output_3_val)
        print("Output 4 on? --> ", not output_4_val)
        print("Output 5 on? --> ", not output_5_val)
        print("Output 6 on? --> ", not output_6_val)
        print("Output 7 on? --> ", not output_7_val)
        print("Output 8 on? --> ", not output_8_val)
#        print("Output 9 on? --> ", not output_9_val)
        # print("Output 10 on? --> ", not output_10_val)
        print("Output Banco Frio on? --> ", not output_banco_frio_val)
        print("Output Camara Frio on? --> ", not output_camara_frio_val)
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
                #temp6 y temp7 son banco de frio y camara de frio. El de ambiente (temp9) no lleva cfg ni output
                cursor.execute("""UPDATE temps4 SET temp1 = %s,temp2 = %s, temp3 = %s, temp4 = %s, temp5 = %s, temp6 = %s, temp7 = %s, temp8 = %s,temp9 = %s, temp10 = %s, temp11 = %s, temp12 = %s, temp1_cfg = %s, temp2_cfg = %s, temp3_cfg = %s, temp4_cfg = %s, temp5_cfg = %s, temp6_cfg = %s, temp7_cfg = %s, temp8_cfg = %s, temp9_cfg = %s, temp10_cfg = %s, temp11_cfg = %s, temp12_cfg = %s, output1 = %s, output2 = %s, output3 = %s, output4 = %s, output5 = %s, output6 = %s, output7 = %s, output8 = %s, output9 = %s, output10 = %s, output11 = %s, output12 = %s WHERE 1=1 """,
                                                (sensor1_temp,sensor2_temp,sensor3_temp,sensor4_temp,sensor5_temp,sensorBancoFrio_temp,sensorCamaraFrio_temp,sensor6_temp,sensor7_temp,sensor8_temp,sensor9_temp,0,
                                                   temp_sens_1,temp_sens_2,temp_sens_3,temp_sens_4,temp_sens_5,temp_sens_banco_frio,temp_sens_camara_frio,temp_sens_6,temp_sens_7,temp_sens_8,0,0,
                                                   output_1_val, output_2_val, output_3_val, output_4_val, output_5_val, output_banco_frio_val, output_pin_camara_frio,output_6_val, output_7_val, output_8_val, False, False
                                                   ))

            connection.commit()

        finally:
            connection.close()

        time.sleep(read_interval)
    except:
        print("Unexpected error:", sys.exc_info()[0])
