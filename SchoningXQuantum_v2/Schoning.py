import itertools
import random
from collections import defaultdict

from Helpers import *


def create_assignment(n):
    return [random.choice([-i - 1, i + 1]) for i in range(n)]


def create_not_to_have_clauses(assignment):
    not_to_have_clauses = [i * (-1) for i in assignment]
    return convert(itertools.combinations(not_to_have_clauses, 3))


def convert(possible_clauses):
    new_possible_clauses = []
    for comb in possible_clauses:
        new_clause = []
        for element in comb:
            new_clause.append(element)
        new_possible_clauses.append(new_clause)
    return new_possible_clauses


def schoning_run(step, n, line, total_it):
    soln_list = get_solution_list(line)

    count_list = defaultdict(int)
    for i in range(total_it):
        assignment = schoning(step, n, line)
        if assignment in soln_list:
            count_list[str(assignment)] += 1

    return sum(count_list.values()) / total_it


def schoning(step, n, line):
    assignment = create_assignment(n)
    for deneme in range(step):
        r = random.randint(0, len(line) - 1)
        converted = create_not_to_have_clauses(assignment)

        # print("converted", converted)
        if line[r] in converted:
            value_negated = random.choice(line[r])
            for a in range(len(assignment)):
                if abs(assignment[a]) == abs(value_negated):
                    assignment[a] = assignment[a] * (-1)
    return assignment