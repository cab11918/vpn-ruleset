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
    
    user_rules = {}
    if '[Rule]' in user_sections:
        for line in user_sections['[Rule]']:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                parts = stripped.split(',')
                if len(parts) >= 2:
                    rule_key = f"{parts[0]},{parts[1]}"
                    user_rules[rule_key] = stripped
    
    result_lines = []
    i = 0
    processed_sections = set()
    while i < len(base_lines):
        line = base_lines[i].strip()
        result_lines.append(base_lines[i])
        i += 1
        
        if line.startswith('[') and line.endswith(']'):
            section = line
            if section in user_sections:
                processed_sections.add(section)
                while i < len(base_lines):
                    next_line = base_lines[i].strip()
                    if next_line.startswith('[') and next_line.endswith(']'):
                        break
                    if section == '[Rule]' and next_line and not next_line.startswith('#'):
                        parts = next_line.split(',')
                        if len(parts) >= 2:
                            rule_key = f"{parts[0]},{parts[1]}"
                            if rule_key in user_rules:
                                result_lines.append(user_rules[rule_key])
                                del user_rules[rule_key]
                                i += 1
                                continue
                    result_lines.append(base_lines[i])
                    i += 1
                for rule in user_rules.values():
                    result_lines.append(rule)
    
    for section, lines in user_sections.items():
        if section not in processed_sections:
            result_lines.append(section)
            result_lines.extend(lines)
    
    with open('output/shadowrocket.conf', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_shadowrocket('output/shadowrocket_base.conf')
