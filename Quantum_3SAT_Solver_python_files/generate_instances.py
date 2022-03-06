import random


def create_cnf(n, k):
    new_line = []
    line = cnf_gen(n, k)
    for clause in line:
        new_line.append(sorted(clause, key=abs))
    return new_line


def cnf_gen(n, k, horn=1):
    cnf = []

    def unique(list_of_tries):
        unique_random = random.randint(1, n)
        while unique_random in list_of_tries:
            unique_random = random.randint(1, n)
        return unique_random

    random_value = random.randint(0, 1)

    def r_to_sign(returning_value):
        if random_value == 1:
            return returning_value
        else:
            return -returning_value

    for i in range(k):
        first = unique([])
        second = unique([first])
        third = unique([first, second])
        if horn:
            cnf.append([first, -second, -third])
        else:
            cnf.append([r_to_sign(first), r_to_sign(second), r_to_sign(third)])
    return cnf
