import abc
from typing import TypeVar

T = TypeVar["T"]

class DataSender():
    def __init__(self, readings_file: str):
        self.readings_file = readings_file

    @abc.abstractmethod
    def read_now(self) -> T:
        pass

    @abc.abstractmethod
    def reading_to_tuple(self, reading: T) -> tuple:
        pass

    @abc.abstractmethod
    def reading_to_json(self, reading: T) -> dict:
        pass

    @abc.abstractmethod
    def serialize_reading(self, reading: T) -> str:
        pass

    @abc.abstractmethod
    def deserialize_reading(self, string: str) -> T:
        pass
    
    
    def save_reading(self, reading: T):
        with open(self.readings_file, "a") as readings_file:
            readings_file.write(str(reading))

