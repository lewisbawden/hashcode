import os
import time
from glob import glob

from parse_input import parse_input_file
from optimize import optimize, optimize_filtering_clients, evalutate_clients, get_full_ingredients_list
from write_output import write_output_file, zip_source


def run_one_problem(path):
    print()
    t0 = time.time()
    clients = parse_input_file(path)
    totals, i, j = optimize_filtering_clients(clients)
    ingredients = get_full_ingredients_list(clients, i, j)
    out = optimize(clients, ingredients)
    evalutate_clients(out, clients, path, True)
    write_output_file(out, os.path.basename(path))
    print(f'Total Time: {time.time() - t0}')


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = glob(r'practice/inp/*.txt')

    for f in input_files:
        run_one_problem(f)

    zip_source('practice')
