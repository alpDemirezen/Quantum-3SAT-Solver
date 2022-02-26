import pickle
from generate_instances import *

n = 3
k = 7

# You can either generate an instance randomly or try one yourself. Both methods are showcased below.

line = create_cnf(n, k)
mylist = [[-1, -2, -3], [-1, -2, 3], [-1, 2, -3], [-1, 2, 3], [1, -2, 3], [1, -2, 3], [1, -2, 3]]
with open('datafile.txt', 'wb') as fh:
    pickle.dump(mylist, fh)
