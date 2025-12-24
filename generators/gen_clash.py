import yaml

def deep_merge(base, override):
    for key, value in override.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        elif isinstance(base.get(key), list) and isinstance(value, list):
            base[key].extend(value)
        else:
            base[key] = value
    return base

def generate_clash():
    with open('output/airport.yaml') as f:
        airport = yaml.safe_load(f)
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        user_config = {}
    
    result = deep_merge(airport, user_config)
    
    with open('output/clash.yaml', 'w') as f:
        yaml.dump(result, f, allow_unicode=True, sort_keys=False)

if __name__ == '__main__':
    generate_clash()
