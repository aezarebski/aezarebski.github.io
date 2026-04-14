from pathlib import Path
from matplotlib import pyplot as plt
import pickle
import gzip
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
import pdb
from vae import VAE, vae_loss, set_seed



# --------------------------------------------------------------------
# Download the data if it is not already present and then read it into
# suitable objects.
data_path = Path("data")
out_path = Path("out")
path = data_path / "mnist"
filename = "mnist.pkl.gz"
model_path = out_path / "vae-model.pt"

out_path.mkdir(parents=True, exist_ok=True)
set_seed(1)

with gzip.open(path / filename, "rb") as f:
    ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")

# Keep only the 5s.
x_train_5 = torch.tensor(x_train[y_train == 5], dtype=torch.float32)
x_valid_5 = torch.tensor(x_valid[y_valid == 5], dtype=torch.float32)
train_loader = DataLoader(
    TensorDataset(x_train_5),
    batch_size=128,
    shuffle=True,
    generator=torch.Generator().manual_seed(1),
)
valid_loader = DataLoader(TensorDataset(x_valid_5), batch_size=128, shuffle=False)


# --------------------------------------------------------------------
# Train.
model = VAE(
    input_dim=784,
    hidden_dims=[400, 200, 100],
    latent_dim=15
)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

n_epochs = 30
train_losses = []
valid_losses = []

for epoch in range(n_epochs):
    model.train()
    train_total = 0.0

    for (xb,) in train_loader:
        # pdb.set_trace()
        opt.zero_grad()
        x_hat, mu, logvar = model(xb)
        loss, recon, kl = vae_loss(xb, x_hat, mu, logvar)
        loss.backward()
        opt.step()

        train_total += loss.item()

    model.eval()
    valid_total = 0.0
    with torch.no_grad():
        for (xb,) in valid_loader:
            x_hat, mu, logvar = model(xb)
            loss, recon, kl = vae_loss(xb, x_hat, mu, logvar)
            valid_total += loss.item()

    train_mean = train_total / len(train_loader.dataset)
    valid_mean = valid_total / len(valid_loader.dataset)

    train_losses.append(train_mean)
    valid_losses.append(valid_mean)

    print(
        f"epoch={epoch+1:02d} "
        f"train_loss={train_mean:.4f} "
        f"valid_loss={valid_mean:.4f}"
    )


# --------------------------------------------------------------------
# Plot learning curves.
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(train_losses, label="train")
ax.plot(valid_losses, label="valid")
ax.set_xlabel("epoch")
ax.set_ylabel("loss per observation")
ax.legend()
fig.savefig(out_path / "vae-learning-curves.png")

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "model_kwargs": {
            "input_dim": model.input_dim,
            "hidden_dims": model.hidden_dims,
            "latent_dim": model.latent_dim,
            "cond_dim": model.cond_dim
        },
    },
    model_path,
)
