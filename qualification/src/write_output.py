import zipfile
from glob import glob



def write_output_file(out, name):
    with open(rf'qualification/out/{name[0]}.txt', 'w') as f:
        f.write(f'{len(out)}\n')
        for pprojects in out:
            f.write(f'{pprojects[0]}\n')
            f.write(f'{" ".join(pprojects[1])}\n')


def zip_source(root):
    files = glob(rf'{root}/**/*.py', recursive=True)
    with zipfile.ZipFile(rf'{root}/out/source.zip', 'w') as z:
        for f in files:
            z.write(f)
