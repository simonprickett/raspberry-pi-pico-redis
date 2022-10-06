# Room / Sensor Mapping Redis Commands

To map which sensors are in which rooms, this project uses a [Redis Sorted Set](https://www.youtube.com/watch?v=MUKlxdBQZ7g) whose key is `picoproject:sensor_room`.  This is covered in the [third video on YouTube](https://www.youtube.com/watch?v=0vw_vhouca8).

The members in the Sorted Set are the sensor IDs, their scores are the room IDs.  This allows each sensor to be in only one room, but each room to contain many sensors.

Paste the following commands into `redis-cli` or RedisInsight to create this key before running the Node.js code:

```
DEL picoproject:sensor_room
ZADD picoproject:sensor_room 214 1 214 2 214 3 212 5 212 6 212 8 213 9 213 11
```

Using a Sorted Set, we can ask Redis which room a given sensor ID is in like this using sensor 1 as an example:

```
ZSCORE picoproject:sensor_room 1
```

This tells us sensor 1 is in room 214.  

We can also ask which sensor IDs are in a given room like this using room 214 as an example:

```
ZRANGE picoproject:sensor_room 214 214 BYSCORE
```

This tells us that sensors 1, 2 and 3 are in room 214.

# JSON Documents for Each Room

We also need to create empty JSON documents for each room in Redis as part of the setup before running the Node.js code.  To do this, paste the following commands into `redis-cli` or RedisInsight:

```
JSON.SET picoproject:room:212 $ '{}'
JSON.SET picoproject:room:213 $ '{}'
JSON.SET picoproject:room:214 $ '{}'
```