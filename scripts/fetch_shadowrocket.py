import sys
import requests

def fetch_shadowrocket(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open('output/shadowrocket_base.conf', 'w') as f:
        f.write(r.text)

if __name__ == '__main__':
    fetch_shadowrocket(sys.argv[1])
