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

We also need to create mostly empty JSON documents for each room in Redis as part of the setup before running the Node.js code.  To do this, paste the following commands into `redis-cli` or RedisInsight:

```
JSON.SET picoproject:room:212 $ '{"room": 212, "num_windows": 1, "description": "This is a double room with a view of the city.", "last_updated": 0, "climate": { "temperature": 23.2, "humidity": 52.0, "light": 15125}}'
JSON.SET picoproject:room:213 $ '{"room": 213, "num_windows": 1, "description": "This room features two queen beds and ocean views.", "last_updated": 0, "climate": { "temperature": 18.9, "humidity": 50.9, "light": 40834}}'
JSON.SET picoproject:room:214 $ '{"room": 214, "num_windows": 2, "description": "In this mini-suite, guests benefit from a king size bed and spa bath.", "last_updated": 0, "climate": { "temperature": 19.3, "humidity": 45.8, "light": 22341}}'
JSON.SET picoproject:room:215 $ '{"room": 215, "num_windows": 1, "description": "A double room overlooking the pool.", "last_updated": 0, "climate": { "temperature": 15.8, "humidity": 42.1, "light": 32999}}'
JSON.SET picoproject:room:216 $ '{"room": 216, "num_windows": 2, "description": "Mini-suite with a king bed and juliet balcony.", "last_updated": 1666022220124, "climate": { "temperature": 24.5, "humidity": 56.2, "light": 21076}}'
JSON.SET picoproject:room:217 $ '{"room": 217, "num_windows": 3, "description": "This room is a full size suite with separate television room and view of the ocean.", "last_updated": 1666012490000, "climate": { "temperature": 25.0, "humidity": 53.1, "light": 13001}}'
JSON.SET picoproject:room:218 $ '{"room": 218, "num_windows": 1, "description": "This double room has a queen bed and benefits from a view of the pool and hot tub.", "last_updated": 1666010023000, "climate": { "temperature": 22.1, "humidity": 51.7, "light": 39982}}'
JSON.SET picoproject:room:219 $ '{"room": 219, "num_windows": 1, "description": "In this double room, guests can relax in a queen bed and see the city skyline from their window.", "last_updated": 1666009941000, "climate": { "temperature": 21.7, "humidity": 50.0, "light": 41024}}'
JSON.SET picoproject:room:220 $ '{"room": 220, "num_windows": 2, "description": "A mini-suite with wide screen television, two wardrobes and a king sized bed.", "last_updated": 1666009876236, "climate": { "temperature": 18.6, "humidity": 49.9, "light": 18912}}'
JSON.SET picoproject:room:221 $ '{"room": 221, "num_windows": 1, "description": "A double room that can be accessed from room 223 for a family stay.", "last_updated": 1666009723640, "climate": { "temperature": 20.1, "humidity": 61.3, "light": 26034}}'
JSON.SET picoproject:room:222 $ '{"room": 222, "num_windows": 3, "description": "Full size suite featuring a king size bed, television lounge and a balcony with ocean views.", "last_updated": 1666019256345, "climate": { "temperature": 19.8, "humidity": 66.8, "light": 27995}}'
JSON.SET picoproject:room:223 $ '{"room": 223, "num_windows": 1, "description": "A double room that can be accessed from room 221 for a family stay.", "last_updated": 1666019712867, "climate": { "temperature": 19.9, "humidity": 42.4, "light": 12054}}'
JSON.SET picoproject:room:224 $ '{"room": 224, "num_windows": 3, "description": "A full size suite featuring a king sized bed, separate television room and chaise.", "last_updated": 1666020993743, "climate": { "temperature": 21.3, "humidity": 43.9, "light": 36232}}'
JSON.SET picoproject:room:225 $ '{"room": 225, "num_windows": 1, "description": "A double room overlooking the courtyard.", "last_updated": 1666024993799, "climate": { "temperature": 22.5, "humidity": 53.8, "light": 24721}}'
JSON.SET picoproject:room:226 $ '{"room": 226, "num_windows": 1, "description": "A double room with city views and a queen bed.", "last_updated": 1666024998434, "climate": { "temperature": 22.7, "humidity": 61.1, "light": 19000}}'
JSON.SET picoproject:room:227 $ '{"room": 227, "num_windows": 1, "description": "Double room overlooking the courtyard.", "last_updated": 1666034234678, "climate": { "temperature": 17.3, "humidity": 70.2, "light": 21436}}'
JSON.SET picoproject:room:228 $ '{"room": 228, "num_windows": 2, "description": "This mini-suite benefits from a king size bed, city views and a mini bar.", "last_updated": 1666082199112, "climate": { "temperature": 19.7, "humidity": 63.3, "light": 12888}}'
JSON.SET picoproject:room:229 $ '{"room": 229, "num_windows": 3, "description": "A full size corner suite with floor to ceiling windows, separate television room and ocean views.", "last_updated": 1666082200031, "climate": { "temperature": 23.6, "humidity": 60.2, "light": 40934}}'
```

# Creating a Search Index

We'll also want to search these documents, so let's setup a RediSearch index.  Run the following command in `redis-cli` or RedisInsight:

```
FT.CREATE idx:rooms ON JSON PREFIX 1 picoproject:room: SCHEMA $.room AS room NUMERIC SORTABLE $.num_windows AS num_windows NUMERIC SORTABLE $.description AS description TEXT $.last_updated AS last_updated NUMERIC SORTABLE $.climate.temperature AS temperature NUMERIC SORTABLE $.climate.humidity AS humidity NUMERIC SORTABLE $.climate.light AS light NUMERIC SORTABLE
```

Ensure that the index was created correctly by running a couple of sample queries using `redis-cli` or RedisInsight...

Find all rooms where the temperature is between 20 and 23 degrees returning only the room numbers and temperature, in descending order of temperature:

```
FT.SEARCH idx:rooms "@temperature:[20 23]" RETURN 2 room temperature SORTBY temperature DESC
```

Redis should return:

```
1) "6"
2) "picoproject:room:226"
3) 1) "temperature"
   2) "22.7"
   3) "room"
   4) "226"
4) "picoproject:room:225"
5) 1) "temperature"
   2) "22.5"
   3) "room"
   4) "225"
6) "picoproject:room:218"
7) 1) "temperature"
   2) "22.1"
   3) "room"
   4) "218"
8) "picoproject:room:219"
9) 1) "temperature"
   2) "21.7"
   3) "room"
   4) "219"
10) "picoproject:room:224"
11) 1) "temperature"
   2) "21.3"
   3) "room"
   4) "224"
12) "picoproject:room:221"
13) 1) "temperature"
   2) "20.1"
   3) "room"
   4) "221"
```

Find the room with the highest humidity level and return the room number, humidity and description:

```
FT.SEARCH idx:rooms "*" SORTBY humidity DESC LIMIT 0 1 RETURN 3 room humidity description
```

Redis should return:

```
1) "18"
2) "picoproject:room:227"
3) 1) "humidity"
   2) "70.2"
   3) "room"
   4) "227"
   5) "description"
   6) "Double room overlooking the courtyard."
```