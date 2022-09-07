import network
import time
import secrets
from picoredis import Redis

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect...")
    time.sleep(0.5)

r = Redis(host="192.168.4.24", port=6379)

r.lpush('pi_pico', 'hello')
r.xadd('astream', '*', 'sender', 'pi_pico', 'data', 'todo')