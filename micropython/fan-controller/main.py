import network
import secrets
import time
import json
from picoredis import Redis, RedisTimeout
from machine import I2C, Pin, ADC
from lcd1602 import LCD1602

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(0.5)

# Should have a network connection...

# Set up the display
i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
display = LCD1602(i2c, 2, 16)

# Set up the fan.
fan = Pin(16, Pin.OUT)  

# Connect to Redis...
r = Redis(host = secrets.REDIS_HOST, port = secrets.REDIS_PORT)
r.auth(secrets.REDIS_PASSWORD)

while True:
    try:
        # Check the Redis list for this sensor
        list_item = r.rpop("picoproject:themostat:214")

        if not list_item is None:
            # Try parsing the JSON
            print(list_item)
            payload = json.loads(list_item)
            print(f"temp: {payload['t']}C")
            print(f"fan: {payload['f']}")

            # Display temperature on the screen.
            display.home()
            display.print(f"Temp: {payload['t']}C")

            # Turn the fan on for payload['f'] seconds.
            fan_duration = payload['f']
            if fan_duration > 0:
                print("Turning the fan on...")
                fan.value(1)
                time.sleep(fan_duration)
                print("Turning the fan off...")
                fan.value(0)
        else:
            print("List was empty, nothing to do.")
    except RedisTimeout:
        print("List was empty, nothing to do.")
    except ValueError:
        print("Received and ignored invalid message.")

    time.sleep(5)
