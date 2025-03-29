#! venv/Scripts/python.exe

import asyncio
import datetime as dt
import random
import time
import requests
import json

API_ENDPOINT = "http://localhost:3000/api"
EXTERNAL_READINGS_LOCATION = "./readings.csv"
KEY_FILE_LOCATION = "./key.txt"
TOKEN_FILE_LOCATION = "./token.txt"

API_ENDPOINTS = {
    "LOAD_EXTERNAL_READING": f"{API_ENDPOINT}/load-external-reading",
}

class ExternalReading():
    def __init__(self, timestamp: dt.datetime, temperature: float, light: float, current: float, voltage: float, wattage: float) -> None:
        self.timestamp = timestamp
        self.temperature = temperature
        self.light = light
        self.current = current
        self.voltage = voltage
        self.wattage = wattage
    
    def __str__(self):
        return f"{str(self.timestamp)},{self.temperature:.2f},{self.light:.2f},{self.current:.2f},{self.voltage:.2f},{self.wattage:.2f}\n"

    @staticmethod
    def make_now(temperature: float, light: float, current: float, voltage: float, wattage: float) -> "ExternalReading":
        return ExternalReading(dt.datetime.now(), temperature, light, current, voltage, wattage)
    
    @staticmethod
    def deserialize(representation: str) -> "ExternalReading":
        timestamp, *everything_else = representation.split(",")
        timestamp = dt.datetime.fromisoformat(timestamp)
        everything_else = [ float(component) for component in everything_else ]
        return ExternalReading(timestamp, *everything_else)

    def to_tuple(self):
        return (
            self.timestamp,
            self.temperature,
            self.light,
            self.current,
            self.voltage,
            self.wattage
        )

    def to_json_dict(self):
        return {
            "timestamp": str(self.timestamp),
            "temperature": self.temperature,
            "light": self.light,
            "current": self.current,
            "voltage": self.voltage,
            "wattage": self.wattage
        }

def read_external_data() -> ExternalReading:
    '''This should be implemented later'''
    return ExternalReading(
        dt.datetime.now(), 
        random.uniform(0, 32),
        random.randint(0, 50),
        random.uniform(0, 100),
        random.uniform(0, 100),
        random.uniform(0, 100),
    )

def save_reading(reading: ExternalReading):
    with open(EXTERNAL_READINGS_LOCATION, "a") as readings_file:
        readings_file.write(str(reading))


TIME_OF_LAST_SUMMARY = None

def create_external_summary():
    with open(EXTERNAL_READINGS_LOCATION, "r") as readings_file:
        readings = [ ExternalReading.deserialize(reading) for reading in readings_file.readlines() ]
        count = len(readings)
        _, *usable_components = list(zip(*[ reading.to_tuple() for reading in readings ]))
        print(usable_components)
        usable_components = [ sum(component_list) / count for component_list in usable_components ]
        summary = ExternalReading.make_now(*usable_components)
        readings_file.truncate(0)
        return summary

async def send_external_summary(reading: ExternalReading):
    response = requests.post(
        API_ENDPOINTS["LOAD_EXTERNAL_READING"],
        json = reading.to_json_dict()
    )
    if not response.ok:
        json_response = json.loads(response.content.decode())
        if json_response["error"] == "Unactive device":
            raise BaseException("The device has been deactivated")
    else:
        print(f"{str(dt.datetime.now())}. The summary was successfully sent")

def main():
    while True:
        current_time = dt.datetime.now()
        if current_time.minute % 10 == 0 and TIME_OF_LAST_SUMMARY != current_time:
            summary = create_external_summary()
            global TIME_OF_LAST_SUMMARY
            TIME_OF_LAST_SUMMARY = current_time
            send_external_summary(summary)
        save_reading(read_external_data())
        time.sleep(5)

if __name__ == '__main__':
    main()
