import datetime as dt
import abc
import aiohttp
from typing import TypeVar, Generic
import asyncio
from utils import dates_differ

class DataReading:
    @abc.abstractmethod
    def to_tuple(self) -> tuple:
        '''Creates a tuple with the components of the reading'''
        pass

    @abc.abstractmethod
    def to_json(self) -> dict:
        '''Creates a tuple with the components of the reading'''
        pass

    def serialize(self) -> str:
        return ",".join(map(lambda x: f"{x:.2f}",self.to_tuple())) + "\n"

T = TypeVar("T", bound=DataReading)
class DataSender(Generic[T]):
    def __init__(
            self, 
            label: str,
            key: str, 
            readings_file: str, 
            api_endpoint: str, 
            sending_interval: int, 
            reading_interval: int
        ):
        '''
        @param sending_interval The number of minutes required to send data summaries to the database
        @param readint_interval The number of seconds to use to make sensor readings
        '''
        self.key = key
        self.readings_file = readings_file
        self.api_endpoint = api_endpoint
        self.time_of_last_summary = None
        self.sending_interval = sending_interval
        self.reading_interval = reading_interval

    @abc.abstractmethod
    def read_data(self) -> T:
        '''Reads actual data from the sensors'''
        pass

    @abc.abstractmethod
    def make_reading(self, *args) -> T:
        '''Creates a reading with the given arguments; i. e., a reading object constructor'''
        pass

    @abc.abstractmethod
    def deserialize_reading(self, string: str) -> T:
        '''
        Parses a reading from a given string; it splits the string using a comma as a separator
        and converts every component to a float, then it passes the components to the
        `make_reading' method
        '''
        components = tuple(map(lambda x: float(x), string.split(",")))
        return self.make_reading(*components)
    
    def save_reading(self, reading: T):
        with open(self.readings_file, "a") as readings_file:
            readings_file.write(reading.serialize())

    def create_summary(self) -> T:
        with open(self.readings_file, "r+") as readings_file:
            readings = [ self.deserialize_reading(reading) for reading in readings_file.readlines() ]
            count = len(readings)

            components = list(zip(*[ reading.to_tuple() for reading in readings ]))
            components = [ sum(component_list) / count for component_list in components ]
            summary = self.make_reading(*components)
            readings_file.truncate(0)

            return summary
    
    def log_message(self, message: str):
        print(f"{str(dt.datetime.now())}. {self.label}: {message}")

    async def send_summary(self):
        reading = self.create_summary()
        json_payload = reading.to_json()
        json_payload["datetime"] = str(dt.datetime.now())

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_endpoint, json = json_payload, headers = { "Authorization": f"Bearer {self.key}" }) as response:
                if response.status != 200:
                    json_response = await response.json()
                    if json_response.get("error") == "Unactive device":
                        raise BaseException("The device has been deactivated")

    async def _main(self):
        while True:
            current_time = dt.datetime.now()
            if current_time.minute % self.sending_interval == 0 and dates_differ(self.time_of_last_summary, current_time):
                self.time_of_last_summary = current_time

                self.log_message("Sending summary of readings to the database")
                await self.send_summary()
                self.log_message("The summary was successfully sent")
            
            self.log_message("Reading data")
            reading = self.read_data()

            self.log_message(f"Saving data in file '{self.readings_file}'")
            self.save_reading(reading)

            self.log_message(f"Waiting for {self.reading_interval} seconds until next reading")
            await asyncio.sleep(self.reading_interval)
    
    def main(self):
        asyncio.run(self._main())
    
