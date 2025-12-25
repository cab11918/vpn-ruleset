from ruamel.yaml import YAML

def deep_merge(base, override):
    for key, value in override.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        elif isinstance(base.get(key), list) and isinstance(value, list):
            base[key].extend(value)
        else:
            base[key] = value
    return base

def generate_clash(airport_file):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    
    with open(airport_file) as f:
        airport = yaml.load(f)
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_config = yaml.load(f)
            if user_config is None:
                user_config = {}
    except FileNotFoundError:
        user_config = {}
    
    result = deep_merge(airport, user_config)
    
    with open('output/clash.yaml', 'w') as f:
        yaml.dump(result, f)

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
