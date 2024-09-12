from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
from datetime import datetime
import json

app = FastAPI()

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

manager = ConnectionManager()

@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message = {
                "from": manager.active_connections[websocket],
                "message": data_json["message"],
                "send_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "from": "System",
            "message": f"{username} disconnected.",
            "send_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
