import os
import glob
import time
from datetime import date

# Loading our 1-wire drivers so we can interface with the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

 # w1/devices/ is the directory for devices connected via 1-wire
base_dir = '/sys/bus/w1/devices/'

# The DS18B20 ROM folder has the name format - "28-xxxxxxxxxxxx device"
device_folder = glob.glob(base_dir + '28*')[0]  

# The DS18B20 writes temperature values to the "w1_slave" file
device_file = device_folder + '/w1_slave'

# This function reads the sensor's output file
# and returns its lines in a List
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# This function converts the raw data in the sensor's output file
# to temperature in Celcius while handling errors too.
def read_temp():
    lines = read_temp_raw()
    
    # 'YES' at the end of line 0 indicates a successful reading.
    # This while block waits until one is made.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
        
    # 't=' precedes the temperature value on line 1
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    

# This function is used to choose whether the script will indefinitely read
# and write temperature values to a file 
def run(readingsFile, sensorDelay = 1, definite = false, numOfMeasurements = 0):

    # Clearing the readings file
    readings = open(readingsFile, 'w')
    readings.close()

    with open(readingsFile, 'a') as readings:
        readings.write("Temperature Readings on " +
                       date.today().strftime("%b-%d-%Y") + "\n")
        
        # Establishing csv format
        readings.write("°C, local time\n")
        
        # If indefinite reading is selected by setting definite to false,
        # the counter is set to -1 and is never incremented so as not to
        # break the while loop. However, setting definite to false will
        # ensure temperature is only read and written numOfMeasurements times.
        if definite:
            counter = 0
        else:
            counter = -1

        while True:
            if counter >= numOfMeasurements:
                break
            readings.write("{}, {}\n"
                           .format(round(read_temp(), 4)
                                   , time.strftime("%H:%M:%S", time.localtime())))
            # flushing is being done immediately as the program may not end traditionally
            # due to the while loop
            readings.flush()
            
            if definite:
                counter += 1
                
            time.sleep(sensorDelay)
            

READINGS_FILE = "TempSensorReadings.txt"
run(READINGS_FILE)
