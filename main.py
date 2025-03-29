#! venv/Scripts/python.exe

import requests
import asyncio
import json
import datetime as dt

API_ENDPOINT = "http://localhost:3000/api"
KEY_FILE_LOCATION = "./key.txt"
TOKEN_FILE_LOCATION = "./token.txt"

API_ENDPOINTS = {
    "DEVICE_LOGIN": f"{API_ENDPOINT}/device-login",
    "LOAD_EXTERNAL_READING": f"{API_ENDPOINT}/load-external-reading",
}

async def login():
    with open(KEY_FILE_LOCATION, "r") as key_file, open(TOKEN_FILE_LOCATION, "w") as token_file:
        key = key_file.read()
        if len(key) != 128:
            raise Exception("The device key was corrupted (wrong length)")

        response = requests.post(
            API_ENDPOINTS["DEVICE_LOGIN"],
            json = { 
                "prototype_key": key
            }
        )

        response_content = json.loads(response.content.decode())
        if not "token" in response_content:
            print(response_content)
            raise Exception("Authentication failed")

        token = response_content["token"]
        token_file.write(token)

def get_token():
    # Also, make sure to login, in case the current token
    # has already expired

    with open(TOKEN_FILE_LOCATION, "r") as token_file:
        token = token_file.read()
        return token

async def load_external_reading(
        current: float, 
        datetime: dt.datetime,
        temperature: float,
        voltage: float,
        wattage: float,
    ):
    response = requests.post(
        API_ENDPOINTS["LOAD_EXTERNAL_READING"], 
        json = {
            "current": current,
            "datetime": datetime,
            "temperature": temperature,
            "voltage": voltage,
            "wattage": wattage
        },
        headers = {
            "Authorization": f"Bearer {get_token()}"
        }
    )
    print(json.loads(response.content.decode()))

async def main():
    # await login()
    await load_external_reading(
        current=50.0, 
        datetime=str(dt.datetime.now()), 
        temperature=32.0, 
        voltage=15.0, 
        wattage=80.0
    )
    # pass

if __name__ == '__main__':
    asyncio.run(main())
