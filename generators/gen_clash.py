def generate_clash(clash_file):
    with open(clash_file) as f:
        clash_content = f.read()
    
    try:
        with open('ruleset/clash.yaml') as f:
            user_content = f.read()
    except FileNotFoundError:
        with open('output/clash.yaml', 'w') as f:
            f.write(clash_content)
        return
    
    clash_lines = clash_content.split('\n')
    user_lines = user_content.split('\n')
    
    # 解析用户配置
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
    
    user_rules = {}
    if 'rules' in user_sections:
        for line in user_sections['rules']:
            stripped = line.strip()
            if stripped.startswith('- '):
                rule = stripped[2:]
                parts = rule.split(',')
                if len(parts) >= 2:
                    rule_key = f"{parts[0]},{parts[1]}"
                    user_rules[rule_key] = stripped
    
    # 处理机场文件
    result_lines = []
    i = 0
    while i < len(clash_lines):
        line = clash_lines[i]
        stripped = line.lstrip()
        result_lines.append(line)
        i += 1
        
        if ':' in stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            key = stripped.split(':')[0].strip()
            if key in user_sections:
                base_indent = len(line) - len(stripped)
                # 跳过机场section
                while i < len(clash_lines):
                    next_line = clash_lines[i]
                    next_stripped = next_line.lstrip()
                    if next_stripped and not next_stripped.startswith('#'):
                        next_indent = len(next_line) - len(next_stripped)
                        if next_indent <= base_indent and ':' in next_stripped and not next_stripped.startswith('-'):
                            break
                    if key == 'rules' and next_stripped.startswith('- '):
                        rule = next_stripped[2:]
                        parts = rule.split(',')
                        if len(parts) >= 2:
                            rule_key = f"{parts[0]},{parts[1]}"
                            if rule_key in user_rules:
                                result_lines.append('  ' + user_rules[rule_key])
                                del user_rules[rule_key]
                                i += 1
                                continue
                    result_lines.append(next_line)
                    i += 1
                # 追加剩余用户内容
                for rule in user_rules.values():
                    result_lines.append('  ' + rule)
    
    with open('output/clash.yaml', 'w') as f:
        f.write('\n'.join(result_lines))

if __name__ == '__main__':
    generate_clash('output/clash_base.yaml')
