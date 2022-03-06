import pickle
from generate_instances import *

n = 3
k = 7

# You can either generate an instance randomly or try one yourself. Both methods are showcased below.

line = create_cnf(n, k)
mylist = [[-1, 5, -7], [-2, 6, -7], [-1, -5, 7], [-1, -2, 4], [1, -6, -7], [-3, 5, -6], [3, -5, -6], [-1, -2, 6], [-3, 6, -7], [4, -5, -6], [-2, -3, 7], [2, -4, -7], [-2, 5, -6], [1, -2, -6], [1, -5, -7], [3, -6, -7], [-1, -5, 7], [-3, 4, -6]]
with open('datafile7_18.txt', 'wb') as fh:
    pickle.dump(mylist, fh)
