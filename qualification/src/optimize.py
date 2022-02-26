import typing
from parse_input import Person, Project


def optimize(peeps: typing.List[Person], projects: typing.List[Project], skill_types: set):

    # Sort projects from shortest wd*days + wb*bbd to longest wd*days + wb*bbd
    wd=2
    wb=1
    ws=-1
    wsk_tot=0
    projects_sorted = sorted(projects, key=lambda p: wd*p.days+wb*p.bbd+ws*p.tot_skilllev)

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
                # Cannot contribute, they already are in the project
                if peep.nname in project_plan[1]:
                    continue

                # Can directly contribute to project with current skill level and levels up skill
                if peep.skill[req_skill] == req_level:
                    project_plan[1].append(peep.nname)
                    break

                # Can directly contribute to project with current skill level but does not level up
                if peep.skill[req_skill] > req_level:
                    project_plan[1].append(peep.nname)
                    break

                # Can contribute but only through mentoring
                elif peep.skill[req_skill] == req_level - 1 and any(p.skill.get(req_skill, 0) > req_level for p in project_plan[1]):
                    project_plan[1].append(peep.nname)

        if len(project_plan[1]) == project.roles:
            out.append(project_plan)

    return out
