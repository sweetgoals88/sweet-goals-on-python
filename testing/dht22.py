import adafruit_dht
import board
import time
import datetime as dt

dht_device = adafruit_dht.DHT22(board.D17)

def read_temperature():
    return dht_device.temperature

def read_humidity():
    return dht_device.humidity

if __name__ == '__main__':
    print("Starting DHT22 sensor test...")
    while True:
        temperature = read_temperature()
        humidity = read_humidity()
        print(f"{str(dt.datetime.now())}. Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f}%")
        time.sleep(2)
