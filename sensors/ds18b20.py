'''
Custom module used to read data from the DS18B20 sensor on the project's Raspberry Pi.
The sensor is intended to read the surface temperature of the panel's photovoltaic
cell in order to estimate its output voltage.

Connections:
- Data -> GPIO 4 (physical pin 7)

Sampling rate: 4/3Hz (0.75s per reading)

Pre requisites:
- sudo cat "dtoverlay=w1-gpio" >> /boot/firmware/config.txt
'''

import os
import glob
import time

DEVICE_FILE = "" 

def prepare_sensor():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]

    global DEVICE_FILE
    DEVICE_FILE = device_folder + '/w1_slave'

def _read_raw_temperature():
    with open(DEVICE_FILE, 'r') as file:
        lines = file.readlines()
        return lines

def read_temperature():
    '''
    Returns the temperature measured by the DS18B20, in
    Celsius
    '''
    lines = _read_raw_temperature()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = _read_raw_temperature()
        print("Waiting for the DS18B20 to be detected")

    equals_position = lines[1].find('t=')
    if equals_position != -1:
        temperature_string = lines[1][equals_position + 2:]
        temperature = float(temperature_string) / 1000.0
        return temperature
