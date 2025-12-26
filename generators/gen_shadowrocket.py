def generate_shadowrocket(base_file):
    with open(base_file) as f:
        base_content = f.read()
    
    try:
        with open('ruleset/shadowrocket.conf') as f:
            user_content = f.read()
    except FileNotFoundError:
        with open('output/shadowrocket.conf', 'w') as f:
            f.write(base_content)
        return
    
    base_lines = base_content.split('\n')
    user_lines = user_content.split('\n')
    
    user_sections = {}
    i = 0
    while i < len(user_lines):
        line = user_lines[i].strip()
        if line.startswith('[') and line.endswith(']'):
            section = line
            section_lines = []
            i += 1
            while i < len(user_lines):
                next_line = user_lines[i].strip()
                if next_line.startswith('[') and next_line.endswith(']'):
                    break
                section_lines.append(user_lines[i])
                i += 1
            user_sections[section] = section_lines
        else:
            i += 1
    
    result_lines = []
    i = 0
    while i < len(base_lines):
        line = base_lines[i].strip()
        result_lines.append(base_lines[i])
        i += 1
        
        if line.startswith('[') and line.endswith(']'):
            section = line
            if section in user_sections:
                while i < len(base_lines):
                    next_line = base_lines[i].strip()
                    if next_line.startswith('[') and next_line.endswith(']'):
                        break
                    result_lines.append(base_lines[i])
                    i += 1
                result_lines.extend(user_sections[section])
    
    with open('output/shadowrocket.conf', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_shadowrocket('output/shadowrocket_base.conf')
