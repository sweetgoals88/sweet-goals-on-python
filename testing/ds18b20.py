import os
import glob
import time
import datetime as dt

device_file = "" 

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]

device_file = device_folder + '/w1_slave'

def _read_raw_temperature():
    with open(device_file, 'r') as file:
        lines = file.readlines()
        return lines

def read_temperature():
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

if __name__ == '__main__':
    while True:
        temperature = read_temperature()
        print(f"{str(dt.datetime.now())}. Temperature: {temperature:.2f} °C")
        time.sleep(1)
