import os
import typing
from glob import glob

from parse_input import parse_input_file, Client
from write_output import write_output_file, zip_source


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    out = set()
    scores = []  # Some function of likes / dislikes for each ingredient
    wl, wd = 1, 1  # Weight given to likes / dislikes

    for ing, (nl, nd) in ingredients.items():
        score = (nl*wl - nd*wd)  # sum of likes, minus sum of dislikes
        if nd == 0:
            # Always add ingredients with no dislikes, and sort to back of the list
            out.add(ing)
            score *= -len(clients)
        scores.append((ing, score))

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
    ingredients_choice = list(ingredients_choice)

    total = 0
    for cl in clients:
        likes_ok = all(i in ingredients_choice for i in cl.likes)
        dislikes_ok = all(i not in ingredients_choice for i in cl.dislikes)
        total += int(likes_ok) * int(dislikes_ok)

    print(f'Ingredients ({len(ingredients_choice)}): {ingredients_choice[:10]} ...')
    print(f'Happy clients: {total} / {len(clients)}')


def run_one_problem(path):
    clients, ingredients = parse_input_file(path)
    out = optimize(clients, ingredients)
    evalutate_clients(path, out, clients)
    write_output_file(out, os.path.basename(path))


# Main entrypoint - execution starts here after definitions are made
if __name__ == '__main__':
    input_files = glob(r'practice/inp/*.txt')

    for f in input_files:
        run_one_problem(f)

    zip_source('practice')
