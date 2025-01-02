import numpy as np
import matplotlib.pyplot as plt
import pickle


with open("training-results.pkl", "rb") as f:
    data = pickle.load(f)
    training_data = data["training_data"]
    intermediates = data["intermediates"]

plt.style.use("./aez20250101.mplstyle")
alpha_val = 0.3


def style_axes(ax, title):
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks([-4, -2, 0, 2, 4])
    ax.set_title(title)


tick_vals = [-4, -2, 0, 2, 4]
fig, axs = plt.subplots(3, 3, figsize=(12, 12))
for ix, x in enumerate(intermediates):
    ax_ix, ax_ij = ix // 3, ix % 3
    axs[ax_ix, ax_ij].scatter(
        x[:, 0], x[:, 1], color="#4daf4a", zorder=5, alpha=alpha_val
    )
    style_axes(axs[ax_ix, ax_ij], f"Layer {ix+1}")
axs[-1, -1].scatter(
    training_data[:, 0], training_data[:, 1], color="#984ea3", zorder=5, alpha=alpha_val
)
style_axes(axs[-1, -1], "Training Data")

fig.tight_layout()
plt.savefig("results-figure.png")
