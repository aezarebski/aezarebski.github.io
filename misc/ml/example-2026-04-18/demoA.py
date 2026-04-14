from pathlib import Path
import requests
from matplotlib import pyplot as plt
import numpy as np
import pickle
import gzip
import itertools
from vae import set_seed

# --------------------------------------------------------------------
# Download the data if it is not already present and then read it into
# suitable objects.
data_path = Path("data")
out_path = Path("out")
path = data_path / "mnist"

path.mkdir(parents=True, exist_ok=True)
out_path.mkdir(parents=True, exist_ok=True)
set_seed(1)

url = "https://github.com/pytorch/tutorials/raw/main/_static/"
filename = "mnist.pkl.gz"

if not (path / filename).exists():
        content = requests.get(url + filename).content
        (path / filename).open("wb").write(content)

with gzip.open((path / filename).as_posix(), "rb") as f:
        ((x_train, y_train), _, _) = pickle.load(f, encoding="latin-1")

# Select just the digits 5.
x_5s = x_train[y_train == 5,]

# Plot a handfull of the digits.
fig, axs = plt.subplots(3, 3, figsize=(9, 9))
for (n, (ix, jx)) in enumerate(itertools.product(range(3), range(3))):
    axs[ix,jx].imshow(x_5s[n].reshape((28, 28)), cmap="gray_r", aspect = "equal")
    axs[ix,jx].set_xticks([])
    axs[ix,jx].set_yticks([])
fig.savefig(fname = out_path / "raw-data-5s.png")
