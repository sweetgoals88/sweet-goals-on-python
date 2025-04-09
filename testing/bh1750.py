import smbus
import time
import datetime as dt

DEVICE = 0x23
CONTINUOUS_HIGH_RES_MODE_2 = 0x11

bus = smbus.SMBus(1)

def _convert_to_number(data):
    result = (data[1] + 256 * data[0]) / 1.2
    return result

def read_light(address = DEVICE):
    data: float = 0
    try:
        data = bus.read_i2c_block_data(address, CONTINUOUS_HIGH_RES_MODE_2)
    except IOError as error:
        print("BH1750 sensor not detected")
        raise error
    return _convert_to_number(data)

if __name__ == '__main__':
    print("Starting BH1750 sensor test...")
    while True:
        try:
            light_level = read_light()
            print(f"{str(dt.datetime.now())}. Light Level: {light_level:.2f} lx")
        except IOError as error:
            print("Error reading light level", error)
        time.sleep(1)
