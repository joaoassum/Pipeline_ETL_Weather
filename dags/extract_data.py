import requests
import json 
from pathlib import Path

import logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url:str) -> list:
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return[]
        
    if not data:
        logging.warning(f"No data found at {url}.") 
        return []
    
    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(exist_ok=True,parents=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
        
        
    return data
