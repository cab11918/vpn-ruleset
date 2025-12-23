import yaml
import glob

POLICY_MAP = {'proxy': 'PROXY', 'direct': 'DIRECT', 'reject': 'REJECT'}

def load_rules():
    rules = []
    for f in sorted(glob.glob('ruleset/*.yaml')):
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
    rules = [convert_rule(r) for r in load_rules()]
    rules = [r for r in rules if r]
    
    with open('output/shadowrocket.conf', 'w') as f:
        f.write('[Rule]\n')
        for rule in rules:
            f.write(rule + '\n')

if __name__ == '__main__':
    generate_shadowrocket()
