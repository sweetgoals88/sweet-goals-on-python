'''
Custom module used to read data from the BH1750 sensor on the project's Raspberry Pi.
The sensor is intended to read the received light of the panel's photovoltaic
cell in order to estimate its output voltage.

Connections:
- SCL -> Physical pin 5
- SDA -> Physical pin 3
- ADD -> GND

Sampling rate: 25/3Hz (0.12s per reading)

Pre requisites:
- sudo raspi-config # enable I2C
- sudo pip install smbus
'''

import smbus

# Define some constants from the datasheet

DEVICE = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13

# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10

# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11

# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21

# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

BUS = None

def prepare_sensor():
    global BUS
    BUS = smbus.SMBus(1)  # Rev 2 Pi uses 1

def _convert_to_number(data):
    '''
    Simple function to convert 2 bytes of data
    into a decimal number
    '''
    result = (data[1] + 256 * data[0]) / 1.2
    return result

def read_light(address = DEVICE):
    '''
    Reads light from the BH1750 sensor in lux
    '''
    try:
        data = BUS.read_i2c_block_data(address, CONTINUOUS_HIGH_RES_MODE_2)
    except IOError as error:
        print("BH1750 sensor not detected")
        raise error
    return _convert_to_number(data)
