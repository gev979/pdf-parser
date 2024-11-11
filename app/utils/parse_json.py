import json
import re

def fix_invalid_json(json_string):
    # Example of simple fixes: Remove trailing commas and fix quotes
    # json_string = re.sub(r',\s*}', '}', json_string)  # Remove trailing commas before closing braces
    # json_string = re.sub(r',\s*\]', ']', json_string)  # Remove trailing commas before closing brackets
    # json_string = re.sub(r"(\w+):", r'"\1":', json_string)  # Fix unquoted keys
    json_string = re.sub(r'\\-', '-', json_string)
    return json_string

def parse_json(json_string):
    try:
        fixed_json = fix_invalid_json(json_string)
        return json.loads(fixed_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None