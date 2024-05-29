import os
import requests
import json

from dotenv import load_dotenv, dotenv_values
    
def get_tariffs(body):
    load_dotenv()
    
    baseURL = os.getenv("ENERGY_SHOP_BASE_URL")
    key = os.getenv("ENERGY_SHOP_API_KEY")
    
    print(baseURL)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': key
    }
    
    req = requests.post(baseURL, headers=headers, data=json.dumps(body))
    return req.json()