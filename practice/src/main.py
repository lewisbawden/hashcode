import os

from parse_input import *
from write_output import *


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    scores = []  # Some function of likes / dislikes for each ingredient
    wl, wd = 1, 1  # Weight given to likes / dislikes

    for ing, (nl, nd) in ingredients.items():
        scores.append(nl*wl - nd*wd)

    # Sort ingredients by popularity score
    scores = sorted(ingredients.keys(), key=lambda s: s[1], reverse=True)

    out = [scores[0]]
    return out


def run_one_problem(path):
    clients, ingredients = parse_input_file(path)
    out = optimize(clients, ingredients)
    write_output_file(out, os.path.basename(path))


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = os.scandir(r'practice/inp')

    for f in input_files:
        run_one_problem(f.path)

    zip_source('practice')
