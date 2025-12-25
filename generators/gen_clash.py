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
    
    airport_lines = airport_content.split('\n')
    user_lines = user_content.split('\n')
    
    # 解析用户配置的sections
    user_sections = {}
    i = 0
    while i < len(user_lines):
        line = user_lines[i]
        stripped = line.lstrip()
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            section_lines = []
            base_indent = len(line) - len(stripped)
            i += 1
            while i < len(user_lines):
                next_line = user_lines[i]
                next_stripped = next_line.lstrip()
                if next_stripped and not next_stripped.startswith('#'):
                    next_indent = len(next_line) - len(next_stripped)
                    if next_indent <= base_indent and ':' in next_stripped and not next_stripped.startswith('-'):
                        break
                section_lines.append(next_line)
                i += 1
            user_sections[key] = section_lines
        else:
            i += 1
    
    # 处理机场文件
    result_lines = []
    i = 0
    while i < len(airport_lines):
        line = airport_lines[i]
        stripped = line.lstrip()
        result_lines.append(line)
        
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            if key in user_sections:
                base_indent = len(line) - len(stripped)
                i += 1
                while i < len(airport_lines):
                    next_line = airport_lines[i]
                    next_stripped = next_line.lstrip()
                    if next_stripped and not next_stripped.startswith('#'):
                        next_indent = len(next_line) - len(next_stripped)
                        if next_indent <= base_indent and ':' in next_stripped and not next_stripped.startswith('-'):
                            break
                    result_lines.append(next_line)
                    i += 1
                result_lines.extend(user_sections[key])
                continue
        i += 1
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
