import json
import aioredis


class ChatDB:
    def __init__(self, room_name):
        self.room_name = room_name

    async def connect(self):
        self.redis = await aioredis.create_redis('redis://localhost')
        await self.redis.set('room_name', self.room_name)

    async def disconnect(self):
        await self.redis.flushall()
        self.redis.close()

    async def add_message(self, message):
        room_name = await self.redis.get('room_name')
        await self.redis.rpush(
            room_name,
            json.dumps(message)
        )

    async def get_messages(self):
        room_name = await self.redis.get('room_name')
        messages = await self.redis.lrange(room_name, 0, -1)
        return [json.loads(message) for message in messages]