import json
import asyncio
from Tools.token_value import get_ethereum_price
from Tools.risk_switch import risk_switcher
from Tools.final_decision import stop_investment
from Tools.log_maintain import update_simulation_json

# Investment logic that continuously updates based on the market
async def investment_logic(amt, profit, loss, stop_event, websocket):
    json_path = "simulation_data.json"
    log_path = "simulation_log.txt"

    # Ensure the JSON and log files exist and empty them
    with open(json_path, "w") as json_file:
        json.dump({}, json_file)
    with open(log_path, "w") as log_file:
        log_file.write("Simulation log initialized.\n")

    data = {
        "amount": amt,
        "held_curr": "liq",
        "tkn_val": 0,
        "eth_equivalent": 0,
        "max_profit": profit,
        "max_loss": loss
    }

    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    with open(log_path, "a") as log_file:
        log_file.write("Simulation started.\n")

    while not stop_event.is_set():
        try:
            tkn_val = get_ethereum_price()
            decision = risk_switcher(tkn_val)
            updated_info = update_simulation_json(decision, tkn_val)

            await websocket.send_text(updated_info)
            
            stop, message = stop_investment()
            if stop:
                await websocket.send_text(message)
                await websocket.close()
                stop_event.set()
                break

            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error in investment loop: {e}")
            break  # Exit loop on error