import os
import typing

from parse_input import *
from write_output import *


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    out = set()
    scores = []  # Some function of likes / dislikes for each ingredient
    wl, wd = 1, 1  # Weight given to likes / dislikes

    for ing, (nl, nd) in ingredients.items():
        scores.append((ing, (nl*wl - nd*wd)))
        # Always add ingredients with no dislikes
        if nd == 0:
            out.add(ing)

    # Sort ingredients by popularity score
    scores = sorted(scores, key=lambda s: s[1], reverse=True)

    prev_score = scores[0][1]
    out.add(scores[0][0])
    for ing, score in scores[1:]:
        if score != prev_score:
            break
        out.add(ing)
        prev_score = score

    return out


def evalutate_clients(path, ingredients_choice, clients: typing.List[Client]):
    print(f'Evaluating {path}')

    total = 0
    for cl in clients:
        likes_ok = all(i in ingredients_choice for i in cl.likes)
        dislikes_ok = all(i not in ingredients_choice for i in cl.dislikes)
        total += int(likes_ok) * int(dislikes_ok)
    print(f'Ingredients: {list(ingredients_choice)[:10]} ...')
    print(f'Happy clients: {total} / {len(clients)}')


def run_one_problem(path):
    clients, ingredients = parse_input_file(path)
    out = optimize(clients, ingredients)
    evalutate_clients(path, out, clients)
    write_output_file(out, os.path.basename(path))


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = os.scandir(r'practice/inp')

    for f in input_files:
        run_one_problem(f.path)

    zip_source('practice')
