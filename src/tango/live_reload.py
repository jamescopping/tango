import asyncio

from websockets.asyncio.server import serve

clients = set()


async def websocket_handler(websocket):
    clients.add(websocket)

    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)


async def websocket_main():
    async with serve(websocket_handler, "localhost", 35729):
        await asyncio.Future()  # run forever


async def reload_clients():
    if not clients:
        return

    for client in clients.copy():
        await client.send("reload")


def trigger_reload():
    asyncio.run(reload_clients())


def start_live_reload_server():
    asyncio.run(websocket_main())


LIVE_RELOAD_SCRIPT = """
<script>
const ws = new WebSocket("ws://localhost:35729");

ws.onopen = () => console.log("Connected to Tango Live Reload");
ws.onerror = (e) => console.error("Live reload error", e);
ws.onclose = () => console.log("Live reload disconnected");

ws.onmessage = (event) => {
    if (event.data === "reload") {
        console.log("Tango: Reloading...");
        location.reload();
    }
};
</script>
"""
