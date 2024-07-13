import asyncio
from quart import Quart, websocket, render_template


app = Quart(__name__)


connections = set()


@app.websocket('/ws')
async def ws():
    connections.add(websocket._get_current_object())
    try:
        while True:
            message = await websocket.receive()
            for connection in connections:
                await connection.send(message)
    except asyncio.CancelledError:
        connections.remove(websocket._get_current_object())


@app.route('/')
async def index():
    return await render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)