'''
Custom module used to read data from the SCT-013 sensor on the project's Raspberry Pi.
The sensor is intended to read current produced by the panel's prototype.

Connections:
- ADC
    - V_DD    -> VCC
    - V_REF   -> VCC
    - AGND    -> GND
    - CLK     -> GPIO 11 (physical pin 23)
    - D_OUT   -> GPIO  9 (physical pin 21)
    _ D_IN    -> GPIO 10 (physical pin 19)
    - CS/SHDN -> GPIO  8 (physical pin 24)
    - DBND    -> GND
- LM358
    - OUT1    -> CH0 (of the ADC)
    - IN1-    -> OUT1
    - GND     -> GND
    - VCC     -> VCC
- SCT-013
    - V+      -> IN1+ (of the LM358)
    - V-      -> GND

Sampling rate: 1 / SINGLE_COMPUTATION_SECONDS (1s per reading as default; variable is found at control_variables.py)

Pre requisites:
- sudo apt-get install python3-spidev # Or skip if using a full-installation RPi OS (SPI is installed by default)
- sudo raspi-config # Enable SPI
'''

import asyncio
import math
from gpiozero import MCP3008
from control_variables import EXTERNAL_READING_INTERVAL, SECONDS_TO_READ_CURRENT, MILLISECONDS_TO_READ_CURRENT

POT = None

def prepare_sensor():
    global POT
    POT = MCP3008(0)

def convert_voltage_to_current(voltage: float) -> float:
    return voltage * 330

def read_current() -> float:
    return convert_voltage_to_current(POT.value)

async def _read_total_current(
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

async def read_total_current() -> float:
    return await _read_total_current(
        EXTERNAL_READING_INTERVAL,
        SECONDS_TO_READ_CURRENT,
        MILLISECONDS_TO_READ_CURRENT
    )
