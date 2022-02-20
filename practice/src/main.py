import os

from parse_input import *
from write_output import *


def run_one_problem(path):
    clients, ingredients = parse_input_file(path)
    

# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = os.scandir(r'../inp')
    for f in input_files:
        run_one_problem(f.path)
