import typing
from parse_input import Client


def optimize(clients, ingredients):
    """ Return list of ingredients to go on pizza. """

    best_ingredients = list()
    scores = list()  # Some function of likes / dislikes for each ingredient
    # TODO: see if applying -1 or 0 weight to each of these improves score on the difficult examples
    wl, wd = 1, 1  # Weight given to likes / dislikes

    for ing, (nl, nd) in ingredients.items():
        score = (nl*wl - nd*wd)  # sum of likes, minus sum of dislikes
        if nd == 0:
            # Always add ingredients with no dislikes, and sort to back of the list
            best_ingredients.append(ing)
            score *= -len(clients)
        scores.append((ing, score))

    # Sort ingredients by popularity score
    scores = sorted(scores, key=lambda s: s[1], reverse=True)
    sorted_ingredients = [i for i, s in scores]

    # Optimise toppings: Binary search for best cut off of ingredients to take
    # Start by taking all ingredients, then half - if it improves, subtract a quarter more ingredients, if not, add a quarter
    # Initialise the default or first values
    test = best_ingredients
    prev_total = 0
    cutoff_lower = len(scores) - len(best_ingredients)
    prev_cutoff_lower = cutoff_lower * 2
    diff = 1e99
    while abs(diff) > 2:
        test = best_ingredients + sorted_ingredients[0: int(cutoff_lower)]
        total = evalutate_clients(test, clients)
        diff = (prev_cutoff_lower - cutoff_lower) / 2
        prev_cutoff_lower = cutoff_lower
        if total >= prev_total:
            cutoff_lower -= diff
        else:
            cutoff_lower += diff * 2  # TODO: Check if this '* 2' does make sure all values skipped over are covered
        prev_total = total

    # TODO: try one-by-one (or a smarter way) adding ingredients that where not added and/or removing ingredients that were added in the final topping choice
    #  (instead of just taking a continuous set from [0: 'lower'])

    return test


def evalutate_clients(ingredients_choice: list, clients: typing.List[Client], path='', do_print=False):
    ing_set = set(ingredients_choice)

    total = 0
    for cl in clients:
        likes_ok = len(cl.likes - ing_set) == 0
        dislikes_ok = len(ing_set.intersection(cl.dislikes)) == 0
        total += int(likes_ok) * int(dislikes_ok)

    if do_print:
        print(f'Evaluating {path}')
        print(f'Ingredients ({len(ingredients_choice)}): {ingredients_choice[:10]} ...')
        print(f'Happy clients: {total} / {len(clients)}')

    return total
