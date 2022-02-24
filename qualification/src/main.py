import os
import time
from glob import glob

from parse_input import parse_input_file
from optimize import optimize
from write_output import write_output_file, zip_source


def run_one_problem(path):
    print()
    t0 = time.time()

    peeps, projects, skill_types = parse_input_file(path)
    out = optimize(peeps, projects, skill_types)
    write_output_file(out, os.path.basename(path))

    print(f'Total Time: {time.time() - t0}')


if __name__ == '__main__':
    input_files = glob(r'qualification/inp/*.txt')

    for f in input_files:
        run_one_problem(f)

    zip_source('qualification')
