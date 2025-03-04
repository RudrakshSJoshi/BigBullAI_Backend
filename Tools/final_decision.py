import json

def stop_investment():
    json_path = "./simulation_data.json"
    log_path = "./simulation_log.txt"

    with open(json_path, "r") as file:
            data = json.load(file)
    
    amount = data.get("amount", 0)
    max_profit = data.get("max_profit", 0)
    max_loss = data.get("max_loss", 0)

    if max_profit != -1:
        if amount >= max_profit:
            print("Max profit reached. Liquidating investments.")
            with open(log_path, "a") as log_file:
                log_file.write(f"Max profit reached: {amount}. Liquidating investments.\nExiting The System...\n")
            return True

    if max_loss != -1:
        if amount <= max_loss:
            print("Max loss reached. Liquidating investments.")
            with open(log_path, "a") as log_file:
                log_file.write(f"Max loss reached: {amount}. Liquidating investments.\nExiting The System...\n")
            return True
        
    return False
          