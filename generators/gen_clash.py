import yaml

def generate_clash(airport_file):
    with open(airport_file) as f:
        airport_content = f.read()
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        user_config = {}
    
    if not user_config:
        with open('output/clash.yaml', 'w') as f:
            f.write(airport_content)
        return
    
    lines = airport_content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        
        if ':' in stripped and not stripped.startswith('-'):
            key = stripped.split(':')[0].strip()
            if key in user_config:
                indent = len(line) - len(stripped)
                value = user_config[key]
                if isinstance(value, str):
                    result_lines.append(' ' * indent + f"{key}: {yaml.dump(value, default_style=\"'\").strip()}")
                else:
                    result_lines.append(' ' * indent + f"{key}: {value}")
                i += 1
                continue
        
        result_lines.append(line)
        i += 1
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
