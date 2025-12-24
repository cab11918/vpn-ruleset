import yaml
import requests
import sys

def deep_merge(base, override):
    for key, value in override.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        elif isinstance(base.get(key), list) and isinstance(value, list):
            base[key].extend(value)
        else:
            base[key] = value
    return base

def generate_clash(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    airport = yaml.safe_load(resp.text)
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        user_config = {}
    
    result = deep_merge(airport, user_config)
    
    with open('output/clash.yaml', 'w') as f:
        yaml.dump(result, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

if __name__ == '__main__':
    generate_clash(sys.argv[1])
