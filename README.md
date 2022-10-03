# Experiments with Raspberry Pi Pico W and Redis

## Introduction

This repository contains [MicroPython](https://micropython.org/) and [Node.js](https://nodejs.org/en/) code to support my series of livestream videos where I build out a system that sends data from sensors into Redis for processing.  I'll add more to this README as the project progresses!

## Videos

* [Episode 1](https://www.youtube.com/watch?v=8Q3jK5CAfNQ), introducing the Pi Pico, installing MicroPython, creating a Redis Stack instance in the cloud and sending data to it with Redis Streams.  Visualizing data with RedisInsight.
* [Episode 2](https://www.youtube.com/watch?v=TQlsvxD6zRM), adding headers and a Grove shield to the Raspberry Pi Pico W, modifying the MicroPython code to read temperature and humidity values from a sensor and send them to Redis, reading those values from Redis using a Node.js application.
* Episode 3 - scheduled for Thursday October 6th 2022... we'll add another sensor, see how to store some of the data long term using RedisJSON and access it in a flexible way with RediSearch.

## Getting Started

To use this repository you will need:

* [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html).
* Your wifi credentials (SSID and password).
* [MicroPython runtime for Pico W](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) (install this on the Pico W using the drag and drop method).
* [Node.js](https://nodejs.org/en/download/).
* [A cloud Redis Stack instance](https://redis.com/try-free/) (free).  Alternatively, you'll need to be able to run Redis Stack somewhere on your local network that both your development machine and a Raspberry Pi Pico W can reach it via an IPv4 address or hostname.  It's easiest to just to this with Redis Cloud :)
* The code in this repository.
* You can use the [Thonny IDE](https://thonny.org/) to edit the code and load it on the Pi Pico W, personally I prefer [VSCode](https://code.visualstudio.com/) with [this extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to manage the Pico W.  This also allows you to use a single IDE to work with both the MicroPython and Node.js codebases.
* If you want to use the exact sensor kit and Grove shield that I am using, you'll need the [Grove Starter Kit for Raspberry Pi Pico](https://www.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico-p-4851.html) from Seeed Studio.

### MicroPython

The MicroPython code requires some secrets management... don't commit secrets (passwords etc) to source control, instead create a file `secrets.py` in this folder... it should look like this:

```python
WIFI_SSID = "wifi network name here"
WIFI_PASSWORD = "wifi password here"
REDIS_HOST = "hostname.of.your.redis.server"
REDIS_PORT = 6379 (or whatever port you have Redis running on)
REDIS_PASSWORD = "redis password here"
```

The Redis client used in this project is in the file `picoredis.py`.  It is [PicoRedis](https://github.com/SpotlightKid/picoredis) by [Christopher Arndt](https://chrisarndt.de/) and is MIT licensed.

Watch the first video to see how to get the code up and running on the device, and how to create a Redis Stack instance in the cloud.  In the second video, you'll learn how to add a temperature/humidity sensor to the device and send data from it to a Redis Stream.

### Node.js

The Node.js code also uses the same secrets, but gets their values from environment variables.  To set up and run the Node.js code, first export the environment variables, then install dependencies (this code uses the [Node-Redis](https://github.com/redis/node-redis) client) and finally start it:

```bash
export REDIS_HOST=hostname.of.your.redis.server
export REDIS_PORT=6379
export REDIS_PASSWORD=your.redis.password
cd node
npm install
npm start
```

Optionally, if you're using a user name and password to connect to Redis, you can also set:

```bash
export REDIS_USER=your.redis.user.name
```

The code connects to Redis, and reads data from the stream that the MicroPython code is writing to.  See the second video for more details.
