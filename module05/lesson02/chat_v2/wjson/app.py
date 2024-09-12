from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message = {
                "from": data_json["from"],
                "message": data_json["message"],
                "send_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"from": "System", "message": "A client disconnected.", "send_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
