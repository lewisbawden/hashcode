

def parse_input_file(path):
    with open(path, 'r') as f:
        # Get all lines, without newline character on the end
        lines = [l.rstrip('\n') for l in f.readlines()]

    clients = []  # Each clients individual likes and dislikes
    ingredients = dict()  # Each ingredients total likes and dislikes across all clients

    num_clients, lines = int(lines[0]), lines[1:]
    for idx in range(0, num_clients):
        # Get list of liked and disliked ingredients for each client
        likes = [] if lines[2 * idx] == '0' else lines[2 * idx].split()[1:]
        dislikes = [] if lines[2 * idx + 1] == '0' else lines[2 * idx + 1].split()[1:]

        # Store client in a list of clients
        c = Client(
            len(likes),
            len(dislikes),
            likes,
            dislikes
        )
        clients.append(c)

        # Store all unique ingredients, and their total likes / dislikes
        # ingredients will store a list with two elements [liked total, disliked total]
        for liked in likes:
            # if ingredient is not in dictionary, start a list with [zero likes, zero dislikes]
            # otherwise, get the list of [total likes, total, dislikes]
            n = ingredients.get(liked, [0, 0])
            # increment likes by 1 for this entry
            ingredients[liked] = [n[0] + 1, n[1]]
        for disliked in dislikes:
            n = ingredients.get(disliked, [0, 0])
            ingredients[disliked] = [n[0], n[1] + 1]

    return clients, ingredients


class Client:
    def __init__(self, n_likes, n_dislikes, likes, dislikes):
        self.n_likes = n_likes
        self.n_dislikes = n_dislikes
        self.likes = set(likes)
        self.dislikes = set(dislikes)

    def __repr__(self):
        return f'{self.__dict__}'
