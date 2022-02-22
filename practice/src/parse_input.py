

def parse_input_file(path):
    with open(path, 'r') as f:
        # Get all lines, without newline character on the end
        lines = [l.rstrip('\n') for l in f.readlines()]

    clients = []  # Each clients individual likes and dislikes

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

    return clients


class Client:
    def __init__(self, n_likes, n_dislikes, likes, dislikes):
        self.n_likes = n_likes
        self.n_dislikes = n_dislikes
        self.likes = set(likes)
        self.dislikes = set(dislikes)

    def __repr__(self):
        return f'{self.__dict__}'
