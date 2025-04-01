from data_sender import DataSender, DataReading
from control_variables import API_ENDPOINTS, INTERNAL_READINGS_FILE

import platform
from random import uniform, random

import adafruit_dht
import board

class InternalReading(DataReading):
    def __init__(self, temperature: float, humidity: float):
        super().__init__()
        self.temperature = temperature
        self.humidity = humidity

    def to_tuple(self):
        return ( self.temperature, self.humidity )
    
    def to_json(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }

class InternalSender(DataSender[InternalReading]):
    def __init__(self, key: str):
        super().__init__(key, INTERNAL_READINGS_FILE, API_ENDPOINTS["LOAD_INTERNAL_READING"], 3, 3)
        self.dht_device = adafruit_dht.DHT22(board.D4)
    
    def make_reading(self, *args):
        return InternalReading(*args)
    
    def read_data(self):
        return InternalReading(
            self.dht_device.temperature, 
            self.dht_device.humidity
        )
