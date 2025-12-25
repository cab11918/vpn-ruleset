def generate_clash(airport_file):
    with open(airport_file) as f:
        airport_lines = f.read().split('\n')
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_lines = f.read().split('\n')
    except FileNotFoundError:
        with open('output/clash.yaml', 'w') as f:
            f.write('\n'.join(airport_lines))
        return
    
    # 找出用户配置中需要追加的section（如proxy-groups, rules）
    append_sections = {}
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
            append_sections[key] = section_lines
        else:
            i += 1
    
    # 处理机场文件，在对应section后追加用户内容
    result_lines = []
    i = 0
    while i < len(airport_lines):
        line = airport_lines[i]
        stripped = line.lstrip()
        result_lines.append(line)
        
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            if key in append_sections:
                base_indent = len(line) - len(stripped)
                i += 1
                # 跳过机场文件中该section的内容
                while i < len(airport_lines):
                    next_line = airport_lines[i]
                    next_stripped = next_line.lstrip()
                    if next_stripped and not next_stripped.startswith('#'):
                        next_indent = len(next_line) - len(next_stripped)
                        if next_indent <= base_indent and ':' in next_stripped and not next_stripped.startswith('-'):
                            break
                    result_lines.append(next_line)
                    i += 1
                # 追加用户的内容
                result_lines.extend(append_sections[key])
                continue
        i += 1
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
