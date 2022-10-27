# Experiments with Raspberry Pi Pico W and Redis

## Introduction

This repository contains [MicroPython](https://micropython.org/) and [Node.js](https://nodejs.org/en/) code to support my series of livestream videos where I build out a system that sends data from sensors into Redis for processing.  I'll add more to this README as the project progresses!

## Videos

* [Episode 1](https://www.youtube.com/watch?v=8Q3jK5CAfNQ), introducing the Pi Pico, installing MicroPython, creating a Redis Stack instance in the cloud and sending data to it with Redis Streams.  Visualizing data with RedisInsight.
* [Episode 2](https://www.youtube.com/watch?v=TQlsvxD6zRM), adding headers and a Grove shield to the Raspberry Pi Pico W, modifying the MicroPython code to read temperature and humidity values from a sensor and send them to Redis, reading those values from Redis using a Node.js application.
* [Episode 3](https://www.youtube.com/watch?v=0vw_vhouca8), added a light sensor, looked at how to modify the Node stream reading code so that it remembers where it was in the Stream when restarted and demonstrated how to use a Sorted Set to model 1:many relationships.  We ended by storing sensor data per room in JSON documents in Redis.
* [Episode 4](https://www.youtube.com/watch?v=MuaJzyUHmx0), dealt with the issue of trimming the incoming data Stream, added last modified timestamps and sorted out some data type mismatches then added a RediSearch index and demonstrated some queries over the data stored in JSON documents.
* [Episode 5](https://www.youtube.com/watch?v=ypQ4bjiKeRo): the final episode for this project.  Added a second Raspberry Pi Pico W with a fan and display attached, used a Redis List to sent it commands to use the fan to lower the room temperature after the temperature has exceeded a threshold for a certain time.

## Getting Started

To use this repository you will need:

* [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html).  This project uses two of these.
* [Headers](https://shop.pimoroni.com/products/pico-header-pack?variant=32374935715923) for each Raspberry Pi Pico W - you'll need to solder these onto the devices in order to be able to attach the Grove shield.
* Your wifi credentials (SSID and password).
* [MicroPython runtime for Pico W](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) (install this on the Pico W using the drag and drop method).
* [Node.js](https://nodejs.org/en/download/).
* [A cloud Redis Stack instance](https://redis.com/try-free/) (free).  Alternatively, you'll need to be able to run Redis Stack somewhere on your local network that both your development machine and a Raspberry Pi Pico W can reach it via an IPv4 address or hostname.  It's easiest to just to this with Redis Cloud :)
* The code in this repository.
* You can use the [Thonny IDE](https://thonny.org/) to edit the code and load it on the Pi Pico W, personally I prefer [VSCode](https://code.visualstudio.com/) with [this extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to manage the Pico W.  This also allows you to use a single IDE to work with both the MicroPython and Node.js codebases.
* If you want to use the exact sensor kit and Grove shield that I am using, you'll need the [Grove Starter Kit for Raspberry Pi Pico](https://www.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico-p-4851.html) from Seeed Studio.  This project uses two Grove shields, one for each Raspberry Pi Pico W device.

### Create the Initial Data Fixtures

This project relies on some data setup tasks that need to be completed before running the Node.js code.  Follow the instructions in [create_initial_data_fixtures.md](create_initial_data_fixtures.md) before starting the code.

### MicroPython

The MicroPython code requires some secrets management... don't commit secrets (passwords etc) to source control, instead create a file `secrets.py` in the `micropython/temp-humidity-light-sensor` and `micropython/fan-controller` folders... it should look like this:

```python
WIFI_SSID = "wifi network name here"
WIFI_PASSWORD = "wifi password here"
REDIS_HOST = "hostname.of.your.redis.server"
REDIS_PORT = 6379 (or whatever port you have Redis running on)
REDIS_PASSWORD = "redis password here"
```

The Redis client used in this project is in the file `picoredis.py`.  It is [PicoRedis](https://github.com/SpotlightKid/picoredis) by [Christopher Arndt](https://chrisarndt.de/) and is MIT licensed.

Watch the first video to see how to get the code for the temperature / humidity / light sensor up and running on the device, and how to create a Redis Stack instance in the cloud.  In the second video, you'll learn how to add a temperature/humidity sensor to the device and send data from it to a Redis Stream.  Setup and code for the fan controller component is covered in the 5th video.

I'm using Seed Studio's [examples from their wiki](https://wiki.seeedstudio.com/Grove_Shield_for_Pi_Pico_V1.0/) for the code that talks to the various Grove sensors in their kit.

### Node.js

The Node.js code also uses the same secrets, but gets their values from a `.env` file  Create a file that looks like this and save it in the `node` folder as `.env`:

```
REDIS_HOST = "hostname.of.your.redis.server"
REDIS_PORT = 6379 (or whatever port you have Redis running on)
REDIS_PASSWORD = "redis password here"
```

Optionally, if you're using a user name and password to connect to Redis, you can also set:

```
REDIS_USER = "your.redis.user.name"
```

To set up and run the Node.js Stream consumer code you'll first need to install the dependencies (this code uses the [Node-Redis](https://github.com/redis/node-redis) client and [dotenv](https://www.npmjs.com/package/dotenv) package) and finally start it:

```bash
cd node
npm install
npm run consumer
```

The code connects to Redis, and reads data from the stream that the MicroPython code is writing to.  See the [second](https://www.youtube.com/watch?v=TQlsvxD6zRM) and [third](https://www.youtube.com/watch?v=0vw_vhouca8) videos for more details.  It also instructs the fan component to turn on the fan when a room is above a certain temperature for a while.  This is covered in the [fifth video](https://www.youtube.com/watch?v=ypQ4bjiKeRo) and uses a Redis List.

To trim the Stream periodically, deleting entries that are more than an hour old, run the trimmer component like this:

```bash
cd node
npm install
npm run trimmer
```

The code connects to Redis, and uses the `XTRIM` command to remove stream entries that are over an hour old.  Note that to do this is uses the `MINID` trimming strategy which became available in Redis 6.2. See the [fourth](https://www.youtube.com/watch?v=MuaJzyUHmx0) video for more details.