from pathlib import Path
from matplotlib import pyplot as plt
import itertools
import torch
from vae import VAE, set_seed

out_path = Path("out")
checkpoint = torch.load(out_path / "vae-model.pt", map_location="cpu")
model = VAE(**checkpoint["model_kwargs"])
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

set_seed(2)
with torch.no_grad():
    z = torch.randn(9, model.latent_dim)
    x_sim = model.decode(z)

fig, axs = plt.subplots(3, 3, figsize=(9, 9))
for (n, (ix, jx)) in enumerate(itertools.product(range(3), range(3))):
    axs[ix, jx].imshow(x_sim[n].reshape(28, 28), cmap="gray_r", aspect="equal")
    axs[ix, jx].set_xticks([])
    axs[ix, jx].set_yticks([])
fig.savefig(out_path / "vae-samples.png")

with torch.no_grad():
    z = torch.randn(4, model.latent_dim)
    assert z.shape == (4,15)
    scales = torch.tensor([0.0, 2.0, 4.0], dtype=z.dtype)
    assert scales.shape == (3,)
    z_scaled = (z.unsqueeze(1) * scales.view(1, 3, 1)).reshape(-1, model.latent_dim)
    assert z_scaled.shape == (12,15)
    x_scaled = model.decode(z_scaled)
    assert x_scaled.shape == (12,28*28)

fig, axs = plt.subplots(4, 3, figsize=(9, 12))
for (n, (ix, jx)) in enumerate(itertools.product(range(4), range(3))):
    axs[ix, jx].imshow(x_scaled[n].reshape(28, 28), cmap="gray_r", aspect="equal")
    axs[ix, jx].set_xticks([])
    axs[ix, jx].set_yticks([])
    if ix == 0:
        axs[ix, jx].set_title(f"scale={int(scales[jx].item())}")
fig.savefig(out_path / "vae-scaled-samples.png")
