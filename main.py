#! venv/Scripts/python.exe

from data_sender import DataSender, DataReading
from random import uniform, random
from multiprocessing import Process

from control_variables import API_ENDPOINTS, INTERNAL_READINGS_FILE, EXTERNAL_READINGS_FILE
from utils import get_device_key
from external_data_collection import ExternalSender



if __name__ == '__main__':
    try:
        key = get_device_key()
    except Exception as e:
        print("The device key was corrupted")

    external_sender = ExternalSender(key)
    internal_sender = InternalSender(key)

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
