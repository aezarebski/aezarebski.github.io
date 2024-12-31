import numpy as np
import matplotlib.pyplot as plt
import pickle



with open("training-results.pkl", "rb") as f:
    data = pickle.load(f)
    training_data = data["training_data"]
    intermediates = data["intermediates"]

plt.style.use("ggplot")

fig, axs = plt.subplots(8 + 1, 1, figsize=(4, 36))
for ix, x in enumerate(intermediates):
    axs[ix].scatter(x[:, 0], x[:, 1], color="#4daf4a", alpha=0.5)
    axs[ix].set_xlim(-6, 6)
    axs[ix].set_ylim(-6, 6)
axs[-1].scatter(training_data[:, 0], training_data[:, 1], color="#984ea3", alpha=0.5)
axs[-1].set_xlim(-6, 6)
axs[-1].set_ylim(-6, 6)
fig.tight_layout()
plt.savefig("results-figure.png")
