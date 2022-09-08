# Experiments with Raspberry Pi Pico W and Redis

## Introduction

This repository contains [MicroPython](https://micropython.org/) code to support my series of livestream videos where I build out a system that sends data from sensors into Redis for processing.  I'll add more to this README as the project progresses!

## Videos

* [Episode 1](https://www.youtube.com/watch?v=8Q3jK5CAfNQ), introducing the Pi Pico, installing MicroPython, creating a Redis Stack instance in the cloud and sending data to it with Redis Streams.  Visualizing data with RedisInsight.
* Epidode 2, this is due to be streamed on September 22nd 2022 (here) and we'll cover attaching real sensors.

## Getting Started

To use this repository you will need:

* [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html).
* Your wifi credentials (SSID and password).
* [MicroPython runtime for Pico W](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) (install this on the Pico W using the drag and drop method).
* [A cloud Redis Stack instance](https://redis.com/try-free/) (free).
* The code in this repository.
* You can use the [Thonny IDE](https://thonny.org/) to edit the code and load it on the Pi Pico W, personally I prefer [VSCode](https://code.visualstudio.com/) with [this extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to manage the Pico W.

The code requires some secrets management... don't commit secrets (passwords etc) to source control, instead create a file `secrets.py` in this folder... it should look like this:

```python
WIFI_SSID = "wifi network name here"
WIFI_PASSWORD = "wifi password here"
REDIS_HOST = "hostname.of.your.redis.server"
REDIS_PORT = 6379 (or whatever port you have Redis running on)
REDIS_PASSWORD = "redis password here"
```

Watch the first video to see how to get the code up and running on the device, and how to create a Redis Stack instance in the cloud.