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
    
    user_overrides = {}
    for line in user_content.split('\n'):
        stripped = line.lstrip()
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            value = ':'.join(stripped.split(':')[1:])
            user_overrides[key] = value
    
    result_lines = []
    for line in airport_content.split('\n'):
        stripped = line.lstrip()
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            if key in user_overrides:
                indent = len(line) - len(stripped)
                result_lines.append(' ' * indent + key + ':' + user_overrides[key])
                continue
        result_lines.append(line)
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
