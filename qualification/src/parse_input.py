

def parse_input_file(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n') for l in f.readlines()]

    peeps = []
    projects = []

    n_peeps = int(lines[0].split()[0])
    n_projects = int(lines[0].split()[1])

    return peeps, projects


class Person:
    def __init__(self, n_skills):
        self.n_skills = n_skills
        self.skill = {}

    def __repr__(self):
        return f'{self.__dict__}'


class Project:
    def __init__(self, days, score, bbd, roles):
        self.days = days
        self.score = score
        self.bbd = bbd
        self.roles = roles

        self.skills = {}

    def __repr__(self):
        return f'{self.__dict__}'