import os

from parse_input import *
from write_output import *


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = os.scandir(r'../inp')
    for f in input_files:
        parse_input_file(f.path)