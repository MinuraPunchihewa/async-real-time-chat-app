import asyncio
from db import ChatDB
from quart import Quart, websocket, render_template


app = Quart(__name__)


connections = set()
chat_db = ChatDB('chat_room')


@app.before_serving
async def init_db():
    await chat_db.start_db()


@app.websocket('/ws')
async def ws():
    connections.add(websocket._get_current_object())
    try:
        while True:
            message = await websocket.receive()
            await chat_db.add_message(message)

            for connection in connections:
                await connection.send(message)
    except asyncio.CancelledError:
        connections.remove(websocket._get_current_object())


@app.route('/')
async def index():
    messages = await chat_db.get_messages()
    return await render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)