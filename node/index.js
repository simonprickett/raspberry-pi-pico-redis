import { createClient, commandOptions } from 'redis';
import * as dotenv from 'dotenv';

dotenv.config();

const REDIS_HOST = process.env.REDIS_HOST;
const REDIS_PORT = process.env.REDIS_PORT;
const REDIS_USER = process.env.REDIS_USER || 'default';
const REDIS_PASSWORD = process.env.REDIS_PASSWORD;
const LAST_ID_KEY = 'picoproject:consumer:last_id';

const client = createClient({
  url: `redis://${REDIS_USER}:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/`
});

await client.connect();

let currentId = await client.get(LAST_ID_KEY);

if (! currentId) {
  currentId = '0-0';
}

while (true) {
  try {
    let response = await client.xRead(
      commandOptions({
        isolated: true
      }), [
        // XREAD can read from multiple streams, starting at a
        // different ID for each...
        {
          key: 'picoproject:incoming',
          id: currentId
        }
      ], {
        // Read 1 entry at a time, block for 5 seconds if there are none.
        COUNT: 1,
        BLOCK: 5000
      }
    );

    if (response) {
      // Get the ID of the first (only) entry returned.
      currentId = response[0].messages[0].id;
      console.log(`Stream ID is ${currentId}.`);
      client.set(LAST_ID_KEY, currentId);

      // Get the sensor ID that sent this message...
      const sensorId = response[0].messages[0].message.id;
      console.log(`Message is from sensor ${sensorId}.`);

      const messageBody = response[0].messages[0].message;
      console.log(messageBody);

      // Figure out which room the sensor is in...
      const roomId = await client.zScore('picoproject:sensor_room', sensorId);
      console.log(`Sensor ${sensorId} is in room ${roomId}.`);

      // Update the room's JSON document with new values.
      const roomKey = `picoproject:room:${roomId}`;

      await client.json.set(roomKey, '$.climate', {
        temperature: messageBody.t,
        humidity: messageBody.h,
        light: messageBody.l
      });
    } else {
      // Response is null, we have read everything that is
      // in the stream right now...
      console.log('No new stream entries.');
    }
  } catch (err) {
    console.error(err);
  }
}