import typing
from parse_input import Person, Project


def optimize(peeps: typing.List[Person], projects: typing.List[Project], skill_types: set):

    # Sort projects from shortest wd*days + wb*bbd to longest wd*days + wb*bbd
    wd=2
    wb=1
    projects_sorted = sorted(projects, key=lambda p: wd*p.days+wb*p.bbd)

    # Create lists for each skill, fill it with each person with that skill
    skill_dict = {s: [] for s in skill_types}

    for peep in peeps:
        # Loop over skills a peep has, add them to the list if they have that skill
        for skill in peep.skill.keys():
            skill_dict[skill].append(peep)

    # Sort skill list from lowest to highest
    for s in skill_types:
        skill_dict[s] = sorted(skill_dict[s], lambda p: p.skill[s])
        
    out = []
    # Loop over projects
    # Take first eligible person from skill required list

    return out
