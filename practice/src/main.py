import os
import sys
import io
import typing
from glob import glob

from parse_input import parse_input_file, Client
from write_output import write_output_file, zip_source


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    out = list()
    scores = list()  # Some function of likes / dislikes for each ingredient
    wl, wd = 1, 1  # Weight given to likes / dislikes

    for ing, (nl, nd) in ingredients.items():
        score = (nl*wl - nd*wd)  # sum of likes, minus sum of dislikes
        if nd == 0:
            # Always add ingredients with no dislikes, and sort to back of the list
            out.append(ing)
            score *= -len(clients)
        scores.append((ing, score))

    # Sort ingredients by popularity score
    scores = sorted(scores, key=lambda s: s[1], reverse=True)
    sorted_ings = [i for i, s in scores]

    # Optimise toppings
    test = out
    prev_total = 0
    lower = len(scores) - len(out)
    prev_lower = lower * 2
    diff = (prev_lower - lower) / 2
    while abs(diff) > 2:
        test = out + sorted_ings[0: int(lower)]
        total = evalutate_clients(test, clients)
        diff = (prev_lower - lower) / 2
        prev_lower = lower
        # TODO: check the previous section skipped over
        if total >= prev_total:
            lower -= diff
        else:
            lower += diff
        prev_total = total

    return test


def evalutate_clients(ingredients_choice: list, clients: typing.List[Client], path='', do_print=False):
    output = sys.stdout if do_print else io.StringIO()
    print(f'Evaluating {path}', file=output)

    total = 0
    for cl in clients:
        likes_ok = all(i in ingredients_choice for i in cl.likes)
        dislikes_ok = all(i not in ingredients_choice for i in cl.dislikes)
        total += int(likes_ok) * int(dislikes_ok)

    print(f'Ingredients ({len(ingredients_choice)}): {ingredients_choice[:10]} ...', file=output)
    print(f'Happy clients: {total} / {len(clients)}', file=output)

    return total


def run_one_problem(path):
    clients, ingredients = parse_input_file(path)
    out = optimize(clients, ingredients)
    evalutate_clients(out, clients, path, True)
    write_output_file(out, os.path.basename(path))


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = glob(r'practice/inp/*.txt')

    for f in input_files:
        run_one_problem(f)

    zip_source('practice')
