import requests
import yaml
import sys
import os

def fetch_clash(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text

if __name__ == '__main__':
    clash_url = sys.argv[1]

    content = fetch_clash(clash_url)
    os.makedirs('output', exist_ok=True)
    with open('output/clash_base.yaml', 'w') as f:
        f.write(content)
