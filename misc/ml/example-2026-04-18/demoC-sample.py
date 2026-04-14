from pathlib import Path
from matplotlib import pyplot as plt
import itertools
import torch
from torch import nn
from vae import VAE, set_seed

out_path = Path("out")
checkpoint = torch.load(out_path / "cvae-model.pt", map_location="cpu")
model = VAE(**checkpoint["model_kwargs"])
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

set_seed(1)
fig, axs = plt.subplots(3, 3, figsize=(9, 9))
for (n, (ix, jx)) in enumerate(itertools.product(range(3), range(3))):
    with torch.no_grad():
        z = torch.randn(1, model.latent_dim)
        y = torch.full((1,), n + 1, dtype=torch.long)
        cond = nn.functional.one_hot(y, num_classes=model.cond_dim).to(z.dtype)
        x_sim = model.decode(z, cond)

    axs[ix, jx].imshow(x_sim[0].reshape(28, 28), cmap="gray_r", aspect="equal")
    axs[ix, jx].set_xticks([])
    axs[ix, jx].set_yticks([])
fig.savefig(out_path / "cvae-samples.png")
