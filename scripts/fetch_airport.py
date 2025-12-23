import requests
import yaml
import sys
import os

def fetch_airport(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return yaml.safe_load(resp.text)

def fetch_shadowrocket(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text

if __name__ == '__main__':
    clash_url = sys.argv[1]
    shadowrocket_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    config = fetch_airport(clash_url)
    os.makedirs('output', exist_ok=True)
    with open('output/airport.yaml', 'w') as f:
        yaml.dump(config, f, allow_unicode=True)
    
    if shadowrocket_url:
        conf = fetch_shadowrocket(shadowrocket_url)
        with open('output/airport_shadowrocket.conf', 'w') as f:
            f.write(conf)
