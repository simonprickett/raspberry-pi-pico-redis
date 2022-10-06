import { createClient, commandOptions } from 'redis';

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
      console.log(JSON.stringify(response));

      // Get the ID of the first (only) entry returned.
      currentId = response[0].messages[0].id;
      console.log(currentId);
      client.set(LAST_ID_KEY, currentId);
    } else {
      // Response is null, we have read everything that is
      // in the stream right now...
      console.log('No new stream entries.');
    }
  } catch (err) {
    console.error(err);
  }
}