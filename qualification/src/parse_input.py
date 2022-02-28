

def parse_input_file(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n') for l in f.readlines()]

    peeps = []
    projects = []

    n_peeps = int(lines[0].split()[0])
    n_projects = int(lines[0].split()[1])
    skill_types=set()

    ii = 1
    for ppeeps in range(n_peeps):
        name = lines[ii].split()[0]
        n_skills = int(lines[ii].split()[1])
        thename = Person(name, n_skills)

        for ss in range(n_skills):
            thisskill=lines[ii+ss+1].split()[0]
            skill_types.add(f'{thisskill}')
            thisskilllev = int(lines[ii + ss+1].split()[1])
            thename.skill[f'{thisskill}']=thisskilllev
            thename.tot_skilllev += thisskilllev
        peeps.append(thename)
        ii+=n_skills+1

    for pprojects in range(n_projects):
        name = lines[ii].split()[0]
        days = int(lines[ii].split()[1])
        score = int(lines[ii].split()[2])
        bbd = int(lines[ii].split()[3])
        n_roles = int(lines[ii].split()[4])
        thename = Project(name, days, score, bbd, n_roles)

        for ss in range(n_roles):
            thisskill=lines[ii+ss+1].split()[0]
            thisskilllev = int(lines[ii + ss+1].split()[1])
            thename.skill[f'{thisskill}']=thisskilllev
            thename.skill_list.append(thisskill)
            thename.tot_skilllev +=thisskilllev

        projects.append(thename)
        ii+=n_roles+1


    return peeps, projects, skill_types


class Person:
    def __init__(self, nname, n_skills):
        self.nname = nname
        self.n_skills = n_skills

        self.skill = {}
        self.freeday = 0
        self.tot_skilllev = 0

    def __repr__(self):
        return f'{self.__dict__}'


class Project:
    def __init__(self, nname, days, score, bbd, roles):
        self.nname = nname
        self.days = days
        self.score = score
        self.bbd = bbd
        self.roles = roles

        self.tot_skilllev = 0
        self.skill = {}
        self.skill_list = []
        self.staffed = False

    def __repr__(self):
        return f'{self.__dict__}'