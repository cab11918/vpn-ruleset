import shutil

def generate_shadowrocket():
    try:
        shutil.copy('ruleset/shadowrocket.conf', 'output/shadowrocket.conf')
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    generate_shadowrocket()
