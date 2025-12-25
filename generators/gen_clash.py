import yaml

def generate_clash(airport_file):
    with open(airport_file) as f:
        airport_content = f.read()
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_content = f.read()
    except FileNotFoundError:
        with open('output/clash.yaml', 'w') as f:
            f.write(airport_content)
        return
    
    user_config = yaml.safe_load(user_content) or {}
    if not user_config:
        with open('output/clash.yaml', 'w') as f:
            f.write(airport_content)
        return
    
    user_lines = {line.split(':')[0].strip(): line for line in user_content.split('\n') if ':' in line and not line.strip().startswith('-')}
    
    lines = airport_content.split('\n')
    result_lines = []
    
    for line in lines:
        stripped = line.lstrip()
        if ':' in stripped and not stripped.startswith('-'):
            key = stripped.split(':')[0].strip()
            if key in user_lines:
                result_lines.append(user_lines[key])
                continue
        result_lines.append(line)
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
