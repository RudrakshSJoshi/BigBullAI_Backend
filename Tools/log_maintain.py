import json

def update_simulation_json(decision: int, tkn_val: float):
    """Updates 'simulation_res.json' with new 'amount' value and logs the change."""
    json_path = "./simulation_data.json"
    log_path = "./simulation_log.txt"
    profit = 0

    try:
        # Read the existing JSON file
        with open(json_path, "r") as file:
            data = json.load(file)

        # Fetch original values
        old_amount = data.get("amount", 0)
        held_curr = data.get("held_curr", "liq")
        old_tkn_val = data.get("tkn_val", 0)
        old_eth_equivalent = data.get("eth_equivalent", 0)

        if(held_curr == "liq" and decision == 0):
            decision = 1
        elif(held_curr == "tkn" and decision == 2):
            decision = 1

        profit = (tkn_val - old_tkn_val) * old_eth_equivalent
        if decision == 1:
            if held_curr == "liq":
                profit = 0
                data["eth_equivalent"] = old_amount / tkn_val
                print("Holding liquidity. No profit.")
                with open(log_path, "a") as log_file:
                    log_file.write(f"Liquidity Held. No profit.\n")
            else:
                data["amount"] += profit
                print("Holding tokens. Profit added.")
                with open(log_path, "a") as log_file:
                    log_file.write(f"Tokens Held. Profit: {profit}.\n")
            data["tkn_val"] = tkn_val
        elif decision == 2:
            data["held_curr"] = "tkn"
            data["tkn_val"] = tkn_val
            data["eth_equivalent"] = old_amount / tkn_val
            profit = 0
            print("Buying tokens. No profit.")
            with open(log_path, "a") as log_file:
                log_file.write(f"Tokens Bought. No profit.\n")
        else:
            data["held_curr"] = "liq"
            data["tkn_val"] = tkn_val
            data["amount"] += profit
            print("Selling tokens. Profit added.")
            with open(log_path, "a") as log_file:
                log_file.write(f"Tokens Sold. Profit: {profit}.\n")

        # Write back the updated JSON
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)

        # print("Update successful.")
    
    except Exception as e:
        print(f"Error: {e}")
