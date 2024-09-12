from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, NamedTuple, Optional
from datetime import datetime
import json

app = FastAPI()

class ChatMessage(NamedTuple):
    from_user: str
    message: str
    send_time: str
    special_effect: Optional[str] = None  # Optional field for special effects

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        del self.active_connections[websocket]

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def handle_command(self, command: str):
        if command == "!happy":
            # Sending a special message with a visual effect
            special_message = ChatMessage(
                from_user="System",
                message="🎉 Happy Programmers' Day! 🎉",
                send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                special_effect="happy"  # Applying a special effect
            )
            await self.broadcast(special_message._asdict())

manager = ConnectionManager()

@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message_text = data_json["message"]

            # Check if it's a command
            if message_text.startswith("!"):
                await manager.handle_command(message_text)
            else:
                message = ChatMessage(
                    from_user=manager.active_connections[websocket],
                    message=message_text,
                    send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                await manager.broadcast(message._asdict())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "from": "System",
            "message": f"{username} disconnected.",
            "send_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
