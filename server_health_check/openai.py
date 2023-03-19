import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from .config import LOG_LIMIT

load_dotenv() 

# This function is called when the OpenAI API servers are down or responding with errors
def check_server_health(api_key):
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.openai.com/v1/engines/davinci", headers=headers)
        if response.status_code == 200:
            return "OpenAI API servers are healthy"
        else:
            server_unhealthy_hook() # A hook to run extra actions when the OpenAI API servers are down or responding with errors
            return f"OpenAI API servers are down or responding with errors: {response.json()}"
    except requests.exceptions.RequestException as e:
        return f"Internal Error: {e}"

# This function is called every CHECK_INTERVAL seconds
# It writes the result of the health check to a log file
# The log file is limited to LOG_LIMIT lines
def openai_health_check():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = check_server_health(os.getenv("OPENAI_API_KEY"))

    with open("health_check.log", "a") as f:
        f.write(f"{timestamp} - {result}\n")
    with open("health_check.log", "r") as f:
        contents = f.readlines()
    with open("health_check.log", "w") as f:
        f.writelines(contents[-LOG_LIMIT:])

# This function is called when the OpenAI API servers are down or responding with errors
def server_unhealthy_hook():
    ...  # define extra actions (e.g. sending notifications)