from data_sender.data_sender import DataSender, DataReading
from control_variables import API_ENDPOINTS, INTERNAL_READINGS_FILE, INTERNAL_SENDING_INTERVAL, INTERNAL_READING_INTERVAL

import sensors.dht22 as dht22

class InternalReading(DataReading):
    def __init__(self, temperature: float, humidity: float):
        super().__init__()
        self.temperature = temperature
        self.humidity = humidity

    def to_tuple(self):
        return (self.temperature, self.humidity)
    
    def to_json(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }

class InternalSender(DataSender[InternalReading]):
    def __init__(self, key: str):
        super().__init__(
            key, 
            INTERNAL_READINGS_FILE, 
            API_ENDPOINTS["LOAD_INTERNAL_READING"], 
            INTERNAL_READING_INTERVAL, 
            INTERNAL_SENDING_INTERVAL
        )
        dht22.prepare_sensor()
    
    def make_reading(self, *args):
        return InternalReading(*args)
    
    def read_data(self):
        return InternalReading(
            dht22.read_temperature(),
            dht22.read_humidity()
        )
