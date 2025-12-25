def generate_clash(airport_file):
    with open(airport_file) as f:
        airport_content = f.read()
    
    with open('output/clash.yaml', 'w') as f:
        f.write(airport_content)

if __name__ == '__main__':
    generate_clash('output/airport.yaml')
