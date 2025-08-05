import os
import sys

def get_env_var(key):
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"{key} environment variable not set.")
    return value

def read_text():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        print("Error: No text (prompt or response) provided.")
        print('Usage: python main.py "prompt or response"')
    return text