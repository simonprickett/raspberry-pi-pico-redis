import network
import secrets
import time
from picoredis import Redis

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(0.5)

# Should have a network connection...

# Connect to Redis...
r = Redis(host = secrets.REDIS_HOST, port = secrets.REDIS_PORT)
r.auth(secrets.REDIS_PASSWORD)

n = 0
while True:
    # Add some value to a Redis stream... 
    stream_id = r.xadd("picoproject:incoming", "*", "device_id", "1", "data", str(n))
    print(stream_id)
    time.sleep(2)
    n = n + 1
