import yaml
import glob

POLICY_MAP = {'proxy': 'PROXY', 'direct': 'DIRECT', 'reject': 'REJECT'}

def load_rules():
    rules = []
    for f in sorted(glob.glob('ruleset/shadowrocket.yaml')):
        with open(f) as file:
            data = yaml.safe_load(file)
            if data and 'rules' in data:
                rules.extend(data['rules'])
    return rules

def convert_rule(rule):
    t = rule['type'].upper()
    v = rule['value']
    p = POLICY_MAP[rule['policy']]
    
    if t == 'DOMAIN':
        return f'DOMAIN,{v},{p}'
    elif t == 'DOMAIN-SUFFIX':
        return f'DOMAIN-SUFFIX,{v},{p}'
    elif t == 'IP-CIDR':
        return f'IP-CIDR,{v},{p}'
    elif t == 'GEOIP':
        return f'GEOIP,{v},{p}'
    return None

def generate_shadowrocket():
    with open('output/airport_shadowrocket.conf') as f:
        base_conf = f.read()
    
    user_rules = [convert_rule(r) for r in load_rules()]
    user_rules = [r for r in user_rules if r]
    
    lines = base_conf.split('\n')
    rule_idx = next((i for i, l in enumerate(lines) if l.strip() == '[Rule]'), -1)
    
    if rule_idx >= 0:
        lines = lines[:rule_idx+1] + user_rules + lines[rule_idx+1:]
    
    with open('output/shadowrocket.conf', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    generate_shadowrocket()
