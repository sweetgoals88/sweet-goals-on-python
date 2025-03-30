#! venv/Scripts/python.exe

from data_sender import DataSender, DataReading
from random import uniform, random
import asyncio
from multiprocessing import Process

API_ENDPOINT = "http://localhost:3000/api"
EXTERNAL_READINGS_FILE = "./external-readings.csv"
INTERNAL_READINGS_FILE = "./internal-readings.csv"
KEY_FILE_LOCATION = "./key.txt"
TOKEN_FILE_LOCATION = "./token.txt"

API_ENDPOINTS = {
    "LOAD_EXTERNAL_READING": f"{API_ENDPOINT}/load-external-reading",
    "LOAD_INTERNAL_READING": f"{API_ENDPOINT}/load-internal-reading",
}

class ExternalReading(DataReading):
    def __init__(self, temperature: float, light: float, current: float, voltage: float, wattage: float):
        super().__init__()
        self.temperature = temperature
        self.light = light
        self.current = current
        self.voltage = voltage
        self.wattage = wattage

    def to_tuple(self):
        return ( self.temperature, self.light, self.current, self.voltage, self.wattage )
    
    def to_json(self):
        return {
            "temperature": self.temperature,
            "light": self.light,
            "current": self.current,
            "voltage": self.voltage,
            "wattage": self.wattage,
        }

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

class ExternalSender(DataSender[ExternalReading]):
    def __init__(self):
        super().__init__(EXTERNAL_READINGS_FILE, API_ENDPOINTS["LOAD_EXTERNAL_READING"], 10, 5)
    
    def make_reading(self, *args):
        return ExternalReading(*args)

    def read_data(self):
        return ExternalReading(
            uniform(0, 32),
            uniform(0, 1000),
            uniform(0, 100),
            uniform(0, 100),
            uniform(0, 1000)
        )

class InternalSender(DataSender[InternalReading]):
    def __init__(self):
        super().__init__(INTERNAL_READINGS_FILE, API_ENDPOINTS["LOAD_INTERNAL_READING"], 5, 3)
    
    def make_reading(self, *args):
        return InternalReading(*args)
    
    def read_data(self):
        return InternalReading(uniform(0, 32), random())

if __name__ == '__main__':
    external_sender = ExternalSender()
    internal_sender = InternalSender()

    first_process = Process(target = external_sender._main)
    second_process = Process(target = internal_sender._main)
    
    try:
        first_process.start()
        second_process.start()
        first_process.join()
        second_process.join()

    except Exception:
        print("Shutting down processes")

    finally:
        first_process.terminate()
        second_process.terminate()
