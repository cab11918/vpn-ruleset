import requests
import yaml
import sys
import os

def fetch_airport(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return yaml.safe_load(resp.text)

if __name__ == '__main__':
    clash_url = sys.argv[1]

    config = fetch_airport(clash_url)
    os.makedirs('output', exist_ok=True)
    with open('output/airport.yaml', 'w') as f:
        yaml.dump(config, f, allow_unicode=True)
