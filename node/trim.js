import { createClient, commandOptions } from 'redis';
import * as dotenv from 'dotenv';

dotenv.config();

const REDIS_HOST = process.env.REDIS_HOST;
const REDIS_PORT = process.env.REDIS_PORT;
const REDIS_USER = process.env.REDIS_USER || 'default';
const REDIS_PASSWORD = process.env.REDIS_PASSWORD;

const KEY_PREFIX = 'picoproject';

const client = createClient({
  url: `redis://${REDIS_USER}:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/`
});

await client.connect();

// Work out the millisecond timestamp from an hour ago...
const oneHourAgo = Date.now() - (60 * 60 * 1000);

// Call XTRIM
const entriesDeleted = await client.xTrim(`${KEY_PREFIX}:incoming`, 'MINID', oneHourAgo);
console.log(`Deleted ${entriesDeleted} entries from the stream.`);

await client.quit();