import os
import requests
import json

from dotenv import load_dotenv
    
def get_tariffs(body):

    load_dotenv()
    
    baseURL = os.getenv("ENERGY_SHOP_BASE_URL")
    key = os.getenv("ENERGY_SHOP_API_KEY")
    

    headers = {
        'Content-Type': 'application/json',
        'Authorization': key
    }
    
    res = requests.post(baseURL, headers=headers, data=json.dumps(body))
    return res.json()