import asyncio
import math
from gpiozero import MCP3008
import datetime as dt

pot = MCP3008(0)

def convert_voltage_to_current(voltage: float) -> float:
    return voltage * 330

def read_current() -> float:
    return convert_voltage_to_current(pot.value)

async def read_total_current(
        total_computation_seconds: int,
        single_computation_seconds: int, 
        milliseconds_between_readings: int
    ) -> float:
    '''
    Gets a sample of current readings every `milliseconds_between_readings` milliseconds
    during `single_computation_seconds` seconds; then, multiplies the Irms of 
    said samples by the ratio between `total_computation_seconds` and `single_computation_seconds`
    in order to estimate the total current flow during `total_computation_seconds` seconds
    without having to spend that long reading data.

    It assumes `single_computation_between_seconds * 1000` is a multiple of `milliseconds_between readings`
    '''
    single_computation_milliseconds = single_computation_seconds * 1000
    number_of_readings = single_computation_milliseconds // milliseconds_between_readings

    summation = 0
    for i in range(number_of_readings):
        summation += read_current() ** 2
        await asyncio.sleep(milliseconds_between_readings / 1000)
    
    single_computation_current = math.sqrt(2 * summation / number_of_readings)
    total_computation_current = float(total_computation_seconds) / float(single_computation_seconds) * single_computation_current
    return total_computation_current


async def main():
    TOTAL_COMPUTATION_SECONDS = 5
    SINGLE_COMPUTATION_SECONDS = 1
    MILLISECONDS_BETWEEN_READINGS = 10

    print("Measuring current with the following parameters:")
    print(f"{TOTAL_COMPUTATION_SECONDS = }")
    print(f"{SINGLE_COMPUTATION_SECONDS = }")
    print(f"{MILLISECONDS_BETWEEN_READINGS = }")

    while True:
        current = await read_total_current(
            TOTAL_COMPUTATION_SECONDS, 
            SINGLE_COMPUTATION_SECONDS, 
            MILLISECONDS_BETWEEN_READINGS
        )
        print(f"{str(dt.datetime.now())}. Current: {current:.2f} A")
        await asyncio.sleep(TOTAL_COMPUTATION_SECONDS)

if __name__ == '__main__':
    asyncio.run(main())
