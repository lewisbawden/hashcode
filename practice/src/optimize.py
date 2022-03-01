import os.path
import random
import time
import typing
from parse_input import Client


def optimize_filtering_clients(clients):
    totals = []
    max_total = 0
    max_i, max_j = 0, 0
    for i in range(0, 10):
        totals.append([])
        for j in range(0, 10):
            ingredients = get_full_ingredients_list(clients, i, j)
            best_ingredients = optimize(clients, ingredients, '', False)
            total = evalutate_clients(best_ingredients, clients)
            totals[i].append(total)
            if total > max_total:
                max_total = total
                max_i, max_j = i, j

    return totals, max_i, max_j


def optimize(clients, ingredients, path, do_genetic=False):
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
            score *= -2*len(clients)
        scores.append((ing, score))

    # Sort ingredients by popularity score
    scores = sorted(scores, key=lambda s: s[1], reverse=True)
    sorted_ingredients = [i for i, s in scores]

    # Optimise toppings: Binary search for best cut off of ingredients to take
    # Start by taking all ingredients, then half - if it improves, subtract a quarter more ingredients, if not, add a quarter
    # Initialise the default or first values
    test = best_ingredients
    n_tries = 4
    if len(sorted_ingredients) < n_tries * 3:
        return test
    else:
        minarg = 1
        maxarg = len(scores) - len(best_ingredients) - 1
        diff = int((maxarg - minarg - 1) / (n_tries - 1))
        maxloc = maxarg
        while diff > 1.5:
            tries = [i for i in range(int(minarg), int(maxarg), diff)]
            totals = [evalutate_clients(best_ingredients + sorted_ingredients[0: ti], clients) for ti in tries]
            maxtotal = max(totals)
            for i, ti in enumerate(reversed(totals)):
                if maxtotal == ti and i == 0:
                    maxloc = tries[n_tries - 1 - i]
                    minarg = tries[n_tries - 1 - i - 2]
                    maxarg = tries[n_tries - 1 - i]
                    break
                elif maxtotal == ti:
                    maxloc = tries[n_tries - 1 - i]
                    minarg = tries[n_tries - 1 - i - 1]
                    maxarg = tries[n_tries - 1 - i + 1]
                    break
            diff = int((maxarg - minarg - 1) / (n_tries - 1))

        test = best_ingredients + sorted_ingredients[0: maxloc]
        if do_genetic:
            test = mutate(best_ingredients, sorted_ingredients[0: len(sorted_ingredients) - len(best_ingredients)], maxloc, clients, os.path.basename(path)[0])

    return test


def mutate(not_disliked, out, maxloc, clients, problem):
    n_mutations = 7
    converged = False
    count = 0
    threshold = 100
    max_count = 10000
    best_score = evalutate_clients(out[0:maxloc] + not_disliked, clients)
    a, b = 2, 2
    best_choice = [threshold * 0.75 * ((1 - (1 / a)) + (i / (maxloc * a))) for i in range(maxloc)] + [threshold * 1.25 * (1 + (i / b * (len(out) - maxloc))) for i in range(len(out) - maxloc)]
    fluct = 50
    fp = rf'practice/out/data_{problem}.csv'
    t0 = time.time()
    with open(fp, 'w') as f:
        f.write('count,time,best_now,best_ever\n')

    while not converged:
        choices = [[best_choice[i] + random.randint(int(-fluct + (count / max_count) * fluct), int(fluct - (count / max_count) * fluct)) for i in range(len(out))] for j in range(n_mutations)]
        tests = [[out[j] for j in range(len(out)) if choices[i][j] < threshold] + not_disliked for i in range(n_mutations)]
        totals = [evalutate_clients(tests[i], clients) for i in range(n_mutations)]
        maxtot = max(totals)
        for i in range(n_mutations):
            if totals[i] == maxtot:
                if maxtot > best_score:
                    best_choice = choices[i]
                    best_score = maxtot
                break
        line = f'{count},{time.time()-t0},{maxtot},{best_score}\n'
        with open(fp, 'a+') as f:
            f.write(line)
        if count == max_count:
            converged = True
            out = tests[i]
        count += 1
    return out


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


def get_full_ingredients_list(clients: typing.List[Client], fussiness_likes=1e9, fussiness_dislikes=1e9):
    ingredients = dict()  # Each ingredients total likes and dislikes across all clients

    # Store all unique ingredients, and their total likes / dislikes
    # ingredients will store a list with two elements [liked total, disliked total]

    # Don't try and cater to fussy eaters
    for c in clients:
        if c.n_likes < fussiness_likes:
            for liked in c.likes:
                # if ingredient is not in dictionary, start a list with [zero likes, zero dislikes]
                # otherwise, get the list of [total likes, total, dislikes]
                n = ingredients.get(liked, [0, 0])
                # increment likes by 1 for this entry
                ingredients[liked] = [n[0] + 1, n[1]]

        if c.n_dislikes < fussiness_dislikes:
            for disliked in c.dislikes:
                n = ingredients.get(disliked, [0, 0])
                ingredients[disliked] = [n[0], n[1] + 1]

    return ingredients