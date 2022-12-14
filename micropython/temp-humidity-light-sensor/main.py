import network
import secrets
import time
from picoredis import Redis
from dht11 import *
from machine import ADC

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(0.5)

# Should have a network connection...

# Set up the temperature/humidity sensor.
temp_humidity_sensor = DHT(18)

# Set up the light sensor.
light_sensor = ADC(1)

# Connect to Redis...
r = Redis(host = secrets.REDIS_HOST, port = secrets.REDIS_PORT)
r.auth(secrets.REDIS_PASSWORD)

while True:
    # Read the temperature and humidity data from the sensor...
    temperature, humidity = temp_humidity_sensor.readTempHumid()

    # Read the light sensor...
    light = light_sensor.read_u16()

    # Send sensor data to a Redis stream... 
    stream_id = r.xadd("picoproject:incoming", "*", "id", "1", "t", str(temperature), "h", str(humidity), "l", str(light))
    print(f"id: {stream_id}")
    print(f"t: {temperature}")
    print(f"h: {humidity}")
    print(f"l: {light}")
    time.sleep(4)
