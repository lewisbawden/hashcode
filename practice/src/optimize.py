import typing
from parse_input import Client


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    out = list()
    scores = list()  # Some function of likes / dislikes for each ingredient
    # TODO: see if applying -1 or 0 weight to each of these improves score on the difficult examples
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
        # TODO: check the section that is removed
        #  (currently halves the section being added, then adds half the section removed if the score drops, or continues to remove half)
        if total >= prev_total:
            lower -= diff
        else:
            lower += diff
        prev_total = total

    # TODO: try same procedure on the other limit
    #  (current limits are from [0: 'lower'], but it is assumed it is always best to take the most popular ingredients - that might not always be true)

    # TODO: try one-by-one (or a smarter way) adding ingredients that where not added and/or removing ingredients that were added in the final topping choice
    #  (instead of just taking a continuous set from [0: 'lower'])

    return test


def evalutate_clients(ingredients_choice: list, clients: typing.List[Client], path='', do_print=False):
    # TODO: parallelise by splitting into 4-8 chunks

    total = 0
    for cl in clients:
        # TODO: check if using 'sets' speeds this up instead of checking for items in a list
        likes_ok = all(i in ingredients_choice for i in cl.likes)
        dislikes_ok = all(i not in ingredients_choice for i in cl.dislikes)
        total += int(likes_ok) * int(dislikes_ok)

    if do_print:
        print(f'Evaluating {path}')
        print(f'Ingredients ({len(ingredients_choice)}): {ingredients_choice[:10]} ...')
        print(f'Happy clients: {total} / {len(clients)}')

    return total
