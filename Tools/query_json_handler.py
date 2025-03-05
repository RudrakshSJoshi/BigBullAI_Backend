import json

def convert_json_to_list(json_data):
    # Convert the JSON string to a Python dictionary (if it's a string representation)
    data = json.loads(json_data)
    
    # Extract the list under the key "queries"
    return data['queries']