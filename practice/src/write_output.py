

def write_output_file(out, name):
    with open(rf'../out/{name[0]}.txt', 'w') as f:
        f.write(f'{len(out)} {" ".join(out)}')
