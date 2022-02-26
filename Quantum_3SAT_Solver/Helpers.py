from collections import defaultdict
import pycosat


def get_solution_list(line):
    return [s for s in pycosat.itersolve(line)]


def back_to_initial(outcome_reversed):
    back_list = []
    for i in range(1, len(outcome_reversed)):
        if outcome_reversed[i] == "0":
            back_list.append(0 - i)
        else:
            back_list.append(i)
    return back_list


def calculate_accuracy(sol_list, tup_list):
    counter = 0
    for sol in tup_list:
        if sol[0] in sol_list:
            counter += sol[1]
    return counter


def count_sols(sol_list, tup_list):
    unique_sols = defaultdict(int)
    for sol in tup_list:
        if sol[0] in sol_list:
            unique_sols[str(sol[0])] += 1
    return unique_sols
