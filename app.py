from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

# Assume these functions are imported from your modules
from Tools.token_value import get_ethereum_price
from Tools.risk_switch import risk_switcher
from Tools.final_decision import stop_investment
from Tools.log_maintain import update_simulation_json

from utils import investment_logic
# Initialize the FastAPI app
app = FastAPI()

# Allow all origins using CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# WebSocket Endpoint: /inv
@app.websocket("/inv")
async def inv(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Receive the initial investment details from the frontend
        init_message = await websocket.receive_text()
        init_data = json.loads(init_message)  # Parse JSON

        amt = init_data.get("amount", 1000)
        profit = init_data.get("profit", amt * 1.0005)
        loss = init_data.get("loss", amt * 0.9995)

        print(amt, profit, loss)
        stop_event = asyncio.Event()
        investment_task = asyncio.create_task(investment_logic(amt, profit, loss, stop_event, websocket))

        while not stop_event.is_set():
            message = await websocket.receive_text()
            if message == "stop":
                print("Received stop command from client.")
                await websocket.send_text("Stopping Token Investment. Liquidating Assets.")
                stop_event.set()
                break

    except WebSocketDisconnect:
        print("Client disconnected from /inv WebSocket")
        stop_event.set()  # Ensure investment logic stops

    finally:
        investment_task.cancel()  # Cancel the running task safely
