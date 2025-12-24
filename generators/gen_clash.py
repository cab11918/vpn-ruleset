import yaml
import glob

POLICY_MAP = {'proxy': 'Proxy', 'direct': 'DIRECT', 'reject': 'REJECT'}

def load_rules():
    rules = []
    for f in sorted(glob.glob('ruleset/clash.yaml')):
        with open(f) as file:
            data = yaml.safe_load(file)
            if data and 'rules' in data:
                rules.extend(data['rules'])
    return rules

def convert_rule(rule):
    t = rule['type'].upper().replace('-', '-')
    v = rule['value']
    p = POLICY_MAP.get(rule['policy'], rule['policy'])
    
    if t == 'DOMAIN':
        return f'DOMAIN,{v},{p}'
    elif t == 'DOMAIN-SUFFIX':
        return f'DOMAIN-SUFFIX,{v},{p}'
    elif t == 'IP-CIDR':
        return f'IP-CIDR,{v},{p}'
    elif t == 'GEOIP':
        return f'GEOIP,{v},{p}'
    return None

def generate_clash():
    with open('output/airport.yaml') as f:
        airport = yaml.safe_load(f)
    
    user_rules = [convert_rule(r) for r in load_rules()]
    user_rules = [r for r in user_rules if r]
    
    airport_rules = airport.get('rules', [])
    airport['rules'] = user_rules + airport_rules
    
    with open('output/clash.yaml', 'w') as f:
        yaml.dump(airport, f, allow_unicode=True, sort_keys=False)

if __name__ == '__main__':
    generate_clash()
