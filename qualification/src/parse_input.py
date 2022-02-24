

def parse_input_file(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n') for l in f.readlines()]

    objects = []

    num_objects, lines = int(lines[0]), lines[1:]
    for idx in range(0, num_objects):
        objects.append(Object(lines[idx]))

    return objects


class Object:
    def __init__(self, lines):
        self.parse(lines)

    def __repr__(self):
        return f'{self.__dict__}'

    def parse(self, lines):
        pass
