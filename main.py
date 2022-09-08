import network
import secrets
import time
from picoredis import Redis

REDIS_HOST = "redis-11565.c275.us-east-1-4.ec2.cloud.redislabs.com"
REDIS_PORT = 11565

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Connecting to wifi...")
    time.sleep(0.5)

# Should have a network connection...

# Connect to Redis...
r = Redis(host = REDIS_HOST, port = REDIS_PORT)
r.auth(secrets.REDIS_PASSWORD)

n = 0
while True:
    # Add some value to a Redis stream... 
    stream_id = r.xadd("picoproject:incoming", "*", "device_id", "1", "data", str(n))
    print(stream_id)
    time.sleep(2)
    n = n + 1
