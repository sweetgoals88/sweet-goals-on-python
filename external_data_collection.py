from data_sender import DataSender, DataReading
from control_variables import API_ENDPOINTS, EXTERNAL_READINGS_FILE
from random import uniform
import smbus

import smbus
import time

BH1750_DEVICE     = 0x23
BH1750_CONTINUOUS_HIGH_RES_MODE_2 = 0x11

def convert_to_number(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result = (data[1] + 256 * data[0]) / 1.2
  return result



class ExternalReading(DataReading):
    def __init__(self, temperature: float, light: float, current: float):
        super().__init__()
        self.temperature = temperature
        self.light = light
        self.current = current

    def to_tuple(self):
        return ( self.temperature, self.light, self.current )
    
    def to_json(self):
        return {
            "temperature": self.temperature,
            "light": self.light,
            "current": self.current,
        }




class ExternalSender(DataSender[ExternalReading]):
    def __init__(self, key: str):
        super().__init__(key, EXTERNAL_READINGS_FILE, API_ENDPOINTS["LOAD_EXTERNAL_READING"], 10, 5)
        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
    
    def make_reading(self, *args):
        return ExternalReading(*args)

    def read_light(self):
        data = self.bus.read_i2c_block_data(BH1750_DEVICE, BH1750_CONTINUOUS_HIGH_RES_MODE_2)
        return convert_to_number(data)

    def read_data(self):
        return ExternalReading(
            uniform(0, 32),
            uniform(0, 1000),
            uniform(0, 100),
            uniform(0, 100),
            uniform(0, 1000)
        )
