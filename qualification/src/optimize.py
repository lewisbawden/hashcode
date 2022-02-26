import typing
from parse_input import Person, Project


def optimize(peeps: typing.List[Person], projects: typing.List[Project], skill_types: set):

    # Sort projects from shortest wd*days + wb*bbd to longest wd*days + wb*bbd
    # todo: include score
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
        skill_dict[s] = sorted(skill_dict[s], key=lambda p: p.skill[s])
        
    out = []
    # Loop over projects
    for project in projects_sorted:
        # Loop over skills in project
        project_plan = [project.nname, []]
        for req_skill, req_level in project.skill.items():
            # Take first eligible person from skill required list
            for peep in skill_dict[req_skill]:
                if peep.skill[req_skill] >= req_level and peep.nname not in project_plan[1]:  # no learning / mentoring
                    project_plan[1].append(peep.nname)  # no handling of days remaining
                    break
        if len(project_plan[1]) == project.roles:
            out.append(project_plan)

    return out
