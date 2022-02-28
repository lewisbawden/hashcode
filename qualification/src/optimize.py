import typing
from parse_input import Person, Project


def optimize(peeps: typing.List[Person], projects: typing.List[Project], skill_types: set):

    # Sort projects from shortest wd*days + wb*bbd to longest wd*days + wb*bbd
    wd=4
    wb=1
    ws=-2
    wsk_tot=1
    projects_sorted = sorted(projects, key=lambda p: wd*p.days+wb*p.bbd+ws*p.score+wsk_tot*p.tot_skilllev)

    # Create lists for each skill, fill it with each person with that skill
    skill_dict = {s: [] for s in skill_types}

    for peep in peeps:
        # Loop over skills a peep has, add them to the list if they have that skill
        for skill in peep.skill.keys():
            skill_dict[skill].append(peep)

    # Sort skill list from lowest to highest
    for s in skill_types:
        skill_dict[s] = sorted(skill_dict[s], key=lambda p: p.skill[s])

    # Also sort list of all peeps
    peeps = sorted(peeps, key=lambda p: p.tot_skilllev)

    out = []
    for i in range(4):
        # Loop over projects
        for project in projects_sorted:
            if project.staffed:
                continue
            # Loop over skills in project
            # Name of the [the name of the project, [peeps, ...]]
            project_plan = [project.nname, []]
            level_increase = []
            for req_skill, req_level in project.skill.items():
                # Take first eligible person from skill required list
                for peep in sorted(peeps, key=lambda p: p.tot_skilllev):
                    # Cannot contribute, they already are in the project
                    if peep in project_plan[1]:
                        continue

                    # Can directly contribute to project with current skill level and levels up skill
                    if project.bbd > project.days + peep.freeday:
                        if peep.skill.get(req_skill, 0) == req_level:
                            project_plan[1].append(peep)
                            level_increase.append(1)
                            break
                        if peep.skill.get(req_skill, 0) > req_level:
                            project_plan[1].append(peep)
                            level_increase.append(0)
                            break

                        # Can contribute but only through mentoring
                        if peep.skill.get(req_skill, 0) == req_level - 1 and any(p.skill.get(req_skill, 0) > req_level for p in project_plan[1]):
                            project_plan[1].append(peep)
                            level_increase.append(1)
                            break

            if len(project_plan[1]) == project.roles:
                last_peep_free = max(project_plan[1], key=lambda p: p.freeday)
                max_freeday = last_peep_free.freeday
                for i in range(project.roles):
                    level = project_plan[1][i].skill.get(project.skill_list[i], 0) + level_increase[i]
                    project_plan[1][i].skill[project.skill_list[i]] = level
                    project_plan[1][i].tot_skilllev += level_increase[i]
                    project_plan[1][i].freeday = max_freeday + project.days
                out.append([project.nname, [p.nname for p in project_plan[1]]])
                project.staffed = True


    return out
