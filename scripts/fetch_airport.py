import requests
import yaml
import sys

def fetch_airport(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return yaml.safe_load(resp.text)

if __name__ == '__main__':
    url = sys.argv[1]
    config = fetch_airport(url)
    with open('output/airport.yaml', 'w') as f:
        yaml.dump(config, f, allow_unicode=True)
