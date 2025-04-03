#! venv/Scripts/python.exe

import asyncio
from multiprocessing import Process

import aiohttp
import time

from utils import get_device_key
from data_sender.external_data_collection import ExternalSender
from data_sender.internal_data_collection import InternalSender
from control_variables import API_ENDPOINTS, NUMBER_OF_ATTEMPTS_FOR_OPERATIONAL


async def make_request(endpoint: str, key: str, json_data: dict[str, str]):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            endpoint, 
            json = json_data,
            headers = { "Authorization": f"Bearer {key}" }
        ) as response:
            return response


async def report_operational_status(key):
    operational_status = None
    failed_attempts = 0
    while True:
        print("Trying to connect the device with the database")

        response = await make_request(
            API_ENDPOINTS["REPORT_STATUS"], 
            key, 
            { "status": "operational" }
        )
        operational_status = response.status
        if operational_status == 200:
            break
        
        failed_attempts += 1
        if failed_attempts >= NUMBER_OF_ATTEMPTS_FOR_OPERATIONAL:
            print("The device couln't connect to the database")
            raise BaseException("The device couln't connect to the database")
        
        print("Waiting for device to be declared operational. Retrying in two seconds")
        time.sleep(2)

    print("The device is operational")


async def report_non_operational_status(key):
    await make_request(
        API_ENDPOINTS["REPORT_STATUS"], 
        key, 
        { "status": "non-operational" }
    )


async def main():
    key = get_device_key()
    await report_operational_status(key)

    external_sender = ExternalSender(key)
    internal_sender = InternalSender(key)

    first_process = Process(target = external_sender.main)
    second_process = Process(target = internal_sender.main)

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

        await report_non_operational_status(key)


if __name__ == '__main__':
    asyncio.run(main())
