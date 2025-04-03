from data_sender.data_sender import DataSender, DataReading
from control_variables import API_ENDPOINTS, EXTERNAL_READINGS_FILE, EXTERNAL_READING_INTERVAL, EXTERNAL_SENDING_INTERVAL
from random import uniform

import sensors.bh1750 as bh1750
import sensors.ds18b20 as ds18b20

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
        super().__init__(
            "ExternalReading",
            key, 
            EXTERNAL_READINGS_FILE, 
            API_ENDPOINTS["LOAD_EXTERNAL_READING"], 
            EXTERNAL_SENDING_INTERVAL, 
            EXTERNAL_READING_INTERVAL
        )

        ds18b20.prepare_sensor()
        bh1750.prepare_sensor()
    
    def make_reading(self, *args):
        return ExternalReading(*args)

    def read_data(self):
        return ExternalReading(
            ds18b20.read_temperature(),
            bh1750.read_light(),
            uniform(0, 100),
        )
