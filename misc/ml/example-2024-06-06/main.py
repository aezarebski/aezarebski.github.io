from io import StringIO
from Bio import Phylo
import h5py
import numpy as np
import pickle
import timeit

NUM_REPS = 300

def _tree_string(n):
    if n == 0:
        return "(A:0.1, A:0.1):0.1"
    else:
        tmp = _tree_string(n-1)
        return f"({tmp}, {tmp}):0.1"

def tree_string(n):
    return _tree_string(n) + ";"

newick_tree = tree_string(9)

filename_newick = "foobar.newick"
with open(filename_newick, "w+") as file:
    file.write(newick_tree)

filename_pickle = "foobar.pickle"
newick_tree_obj = Phylo.read(StringIO(newick_tree), "newick")
with open(filename_pickle, "wb+") as file:
    pickle.dump(newick_tree_obj, file)

filename_hdf5 = "foobar.hdf5"
with h5py.File(filename_hdf5, "w") as file:
    pickle_blob = np.void(pickle.dumps(newick_tree_obj))
    for i in range(NUM_REPS):
        file.create_dataset(f"tree_{i}", data=pickle_blob)



def test_a():
    tree = Phylo.read(filename_newick, "newick")
    return len(tree.get_terminals())

def test_b1():
    with open(filename_pickle, "rb") as file:
        tree = pickle.load(file)
        return len(tree.get_terminals())

def test_b2():
    for i in range(int(NUM_REPS/20)):
        with open(filename_pickle, "rb") as file:
            tree = pickle.load(file)
    return len(tree.get_terminals())

hdf5_conn = h5py.File(filename_hdf5, "r")
def test_c1():
    tree = pickle.loads(hdf5_conn[f"tree_0"][()])
    return len(tree.get_terminals())

def test_c2():
    for i in range(int(NUM_REPS/20)):
        tree = pickle.loads(hdf5_conn[f"tree_{i}"][()])
    return len(tree.get_terminals())

assert test_a() == test_b1()
assert test_a() == test_b2()
assert test_a() == test_c1()
assert test_a() == test_c2()

time_a = timeit.timeit(lambda: test_a(), number=NUM_REPS)
time_b1 = timeit.timeit(lambda: test_b1(), number=NUM_REPS)
time_b2 = timeit.timeit(lambda: test_b2(), number=20)
time_c1 = timeit.timeit(lambda: test_c1(), number=NUM_REPS)
time_c2 = timeit.timeit(lambda: test_c2(), number=20)
hdf5_conn.close()

print(f"The example tree has {test_a()} terminals")
print(f"We average times over {NUM_REPS} evaluations")
print(f"Reading with pickle (individually) is {(time_a/time_b1):.2f} times faster than reading newick")
print(f"Reading with pickle (batched) is {(time_a/time_b2):.2f} times faster than reading newick")
print(f"Reading from HDF5 (individually) is {(time_a/time_c1):.2f} times faster than reading newick")
print(f"Reading from HDF5 (batched) is {(time_a/time_c2):.2f} times faster than reading newick")
