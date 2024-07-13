import json
from redis import asyncio as aioredis


class ChatDB:
    def __init__(self, room_name):
        self.room_name = room_name
        self.pool = aioredis.ConnectionPool.from_url("redis://localhost")
        self.client = None

    async def connect(self):
        self.client = aioredis.Redis(connection_pool=self.pool)
        await self.client.set('room_name', self.room_name)

    async def disconnect(self):
        await self.client.flushall()
        self.client.close()

    async def add_message(self, message):
        room_name = await self.client.get('room_name')
        await self.client.rpush(
            room_name,
            json.dumps(message)
        )

    async def get_messages(self):
        room_name = await self.client.get('room_name')
        messages = await self.client.lrange(room_name, 0, -1)
        return [eval(json.loads(message)) for message in messages]