'''
Custom module used to read data from the DHT22 sensor on the project's Raspberry Pi.
The sensor is intended to read internal temperature and humidity of the prototype.

Connections:
- Data -> GPIO 17 (physical pin 11)

Sampling rate: 0.5Hz (2s per reading)

Pre requisites:
- sudo pip install adafruit-circuitpython-dht
'''

import adafruit_dht
import board

DHT_DEVICE = None

def prepare_sensor():
    global DHT_DEVICE
    DHT_DEVICE = adafruit_dht.DHT22(board.D17)

def read_temperature():
    '''
    Gets the temperature of the DHT22 sensor in Celsius
    '''
    return DHT_DEVICE.temperature

def read_humidity():
    '''
    Gets the humidity of the DHT22 sensor in percentage
    '''
    return DHT_DEVICE.humidity