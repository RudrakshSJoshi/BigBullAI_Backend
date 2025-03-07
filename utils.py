import json
import asyncio
from Tools.token_value import get_ethereum_price, get_electronic_gold_price
from Tools.risk_switch import risk_switcher
from Tools.final_decision import stop_investment
from Tools.log_maintain import update_simulation_json
from Agents.differentiator_agent import initiate
from Agents.web_scraper_agent import generate_questions
from Agents.web_scrape_answerer import get_answers
from Tools.query_json_handler import convert_json_to_list
from Tools.web_scrape_serp import search_internet
import threading

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
        "init_amt": amt,
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
            # tkn_val = get_electronic_gold_price()
            decision = risk_switcher(tkn_val)
            updated_info = update_simulation_json(decision, tkn_val)
            await websocket.send_json(updated_info)
            # await websocket.send_text(updated_info)
            
            stop, message = stop_investment()
            if stop:
                await websocket.send_json(message)
                await websocket.close()
                stop_event.set()
                break

            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error in investment loop: {e}")
            break  # Exit loop on error

async def handle_chat(query):
    response = initiate(query)
    category = response.get("category")

    if category == "web_scrape":
        queries_json = generate_questions(query)

        print("works till now")
        queries = convert_json_to_list(queries_json)  # Convert JSON string to list safely
        
        if not isinstance(queries, list):  # Ensure queries is a list
            raise ValueError("convert_json_to_list did not return a valid list of queries.")
        
        res = [None] * len(queries)  # Pre-allocate list to maintain order
        print("Also working my man")
        def fetch_results(idx, q):
            try:
                res[idx] = search_internet(q)  # Store results in correct index
            except Exception as e:
                res[idx] = f"Error fetching results: {str(e)}"  # Handle errors safely
        
        threads = []
        for i, q in enumerate(queries):
            thread = threading.Thread(target=fetch_results, args=(i, q))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Ensure `get_answers` returns a valid JSON-compatible value
        bot_answer = get_answers(queries, res, query)
        print("Works here too")
        if isinstance(bot_answer, dict):  
            response["bot_answer"] = bot_answer  # Store dictionary directly if valid
        else:
            response["bot_answer"] = str(bot_answer)  # Convert to string if needed
        
    return response
