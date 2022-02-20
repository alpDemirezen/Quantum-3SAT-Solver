import random


def tcnfgen(n, k, horn=1):
    cnf = []

    def unique(l, k):
        t = random.randint(1, n)
        while (t in l):
            t = random.randint(1, n)
        return t

    r = (lambda: random.randint(0, 1))

    def r_to_sign(x):
        if r() == 1:
            return x
        else:
            return -x

    for i in range(k):
        x = unique([], n)
        y = unique([x], n)
        z = unique([x, y], n)
        if horn:
            cnf.append([x, -y, -z])
        else:
            cnf.append([r_to_sign(x), r_to_sign(y), r_to_sign(z)])
    return cnf


def create_CNF(n, k):
    new_line = []
    line = tcnfgen(n, k)
    for clause in line:
        new_line.append(sorted(clause, key=abs))
    return new_line
