from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from fastapi import APIRouter
import json

clients: List[WebSocket] = []

router = APIRouter()

@router.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")

async def send_order_update(order_id: int, status: str, event_type: str):
    message = {
        "order_id": order_id,
        "status": status,
        "event_type": event_type, 
    }

    for client in clients:
        await client.send_text(json.dumps(message))