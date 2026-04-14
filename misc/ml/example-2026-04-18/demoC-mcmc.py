from pathlib import Path
import gzip
import pickle
import jax
import jax.numpy as jnp

# from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

import numpy as np
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, SA
import torch
from vae import VAE, set_seed

DATA_FILE = Path("data") / "mnist" / "mnist.pkl.gz"
OUT_PATH = Path("out")
CHECKPOINT_FILE = OUT_PATH / "cvae-model.pt"
MISSING_PROB = 0.5
OBSERVATION_SCALE = 0.10
NUM_WARMUP = 1000
NUM_SAMPLES = 20000
MASK_SEED = 2
MCMC_SEED = 3


# The `decode_with_torch` and `decode_black_box` functions wrap the
# decoder so that it can be used by Numpyro in posterior sampling.

def decode_with_torch(model, z, cond):
    with torch.no_grad():
        z_t = torch.tensor(np.array(z, dtype=np.float32, copy=True)).reshape(1, -1)
        cond_t = torch.tensor(np.array(cond, dtype=np.float32, copy=True)).reshape(1, -1)
        image = model.decode(z_t, cond_t)[0].cpu().numpy().astype(np.float32)
    return image


def decode_black_box(model, z, cond):
    result_shape = jax.ShapeDtypeStruct((model.input_dim,), jnp.float32)
    return jax.pure_callback(
        lambda z_, cond_: decode_with_torch(model, z_, cond_),
        result_shape,
        z,
        cond,
    )


def save_digit_plot(image, path, title):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(image.reshape(28, 28), cmap="gray_r", aspect="equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_masked_plot(image, missing_mask, path, title):
    cmap = plt.get_cmap("gray_r")
    rgb = cmap(image)[:, :3].astype(np.float32)
    rgb[missing_mask] = np.array([29 / 255, 112 / 255, 184 / 255], dtype=np.float32)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(rgb.reshape(28, 28, 3), aspect="equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def mcmc_model(model, observed_pixels, observed_index, latent_dim, cond_dim):
    theta_dim = latent_dim + cond_dim
    theta = numpyro.sample(
        "theta",
        dist.Normal(jnp.zeros(theta_dim, dtype=jnp.float32), 1.0).to_event(1),
    )

    z = theta[:latent_dim]
    cond_logits = theta[latent_dim:]
    cond = numpyro.deterministic("cond", jax.nn.softmax(cond_logits))
    image_mean = numpyro.deterministic(
        "image_mean",
        decode_black_box(model, z, cond),
    )

    predicted_observed = jnp.take(image_mean, observed_index)
    numpyro.sample(
        "obs",
        dist.Normal(predicted_observed, OBSERVATION_SCALE).to_event(1),
        obs=observed_pixels,
    )



# Step 1: load one validation image and plot the full digit.
OUT_PATH.mkdir(parents=True, exist_ok=True)
set_seed(1)

with gzip.open(DATA_FILE, "rb") as f:
    ((_, _), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")

data_image = np.asarray(x_valid[0], dtype=np.float32)
true_digit = int(y_valid[0])
save_digit_plot(
    data_image,
    OUT_PATH / "cvae-mcmc-data.png",
    f"Digit: {true_digit}",
)


# Step 2: mask pixels and highlight the missing values.
rng = np.random.default_rng(MASK_SEED)
missing_mask = rng.random(data_image.shape[0]) < MISSING_PROB
if missing_mask.all():
    missing_mask[0] = False
if (~missing_mask).all():
    missing_mask[0] = True

observed_index = np.flatnonzero(~missing_mask)


# Step 3: keep the trained PyTorch decoder as a black box inside the
# probabilistic model.
checkpoint = torch.load(CHECKPOINT_FILE, map_location="cpu")
model = VAE(**checkpoint["model_kwargs"])
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# This uses sample adaptive MCMC from Michael Zhu (2019) which is
# gradient-free because otherwise you'd need to look inside the black
# box of the decoder.
kernel = SA(
    lambda observed_pixels, observed_index: mcmc_model(
        model,
        observed_pixels,
        observed_index,
        model.latent_dim,
        model.cond_dim,
    )
)
mcmc = MCMC(kernel, num_warmup=NUM_WARMUP, num_samples=NUM_SAMPLES, num_chains=1)


# Step 4: sample the posterior over latent coordinates and class logits.
observed_pixels = jnp.asarray(data_image[observed_index], dtype=jnp.float32)
observed_index_jax = jnp.asarray(observed_index)
mcmc.run(
    jax.random.PRNGKey(MCMC_SEED),
    observed_pixels=observed_pixels,
    observed_index=observed_index_jax,
)
mcmc.print_summary()

samples = mcmc.get_samples()
theta = samples["theta"]
theta_t = torch.tensor(np.array(theta, dtype=np.float32, copy=True))
z_samples = theta_t[:, : model.latent_dim]
cond_probs = torch.softmax(theta_t[:, model.latent_dim:], dim=1)


# Step 5: decode each posterior sample in PyTorch and average the images.
with torch.no_grad():
    decoded = model.decode(z_samples, cond_probs).cpu().numpy()
posterior_mean = decoded.mean(axis=0).astype(np.float32)

imputed_image = data_image.copy()
imputed_image[missing_mask] = posterior_mean[missing_mask]

# Step 5 and a half: create a two panel plot with the masked and imputed digits
fig, ax = plt.subplots(1, 2, figsize=(8, 4))

cmap = plt.get_cmap("gray_r")
rgb = cmap(data_image)[:, :3].astype(np.float32)
rgb[missing_mask] = np.array([29 / 255, 112 / 255, 184 / 255], dtype=np.float32)
ax[0].imshow(rgb.reshape(28, 28, 3), aspect="equal")
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_title("Masked digit")
ax[1].imshow(imputed_image.reshape(28, 28), cmap="gray_r", aspect="equal")
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_title("Imputed digit")
fig.tight_layout()
fig.savefig(OUT_PATH / "cvae-mcmc-input-output.png")
plt.close(fig)


# Step 6: average the inferred class probabilities across the chain.
digit_probs = cond_probs.mean(dim=0).cpu().numpy().astype(np.float32)
colors = ["#1d70b8" if digit == true_digit else "0.6" for digit in range(model.cond_dim)]

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(np.arange(model.cond_dim), digit_probs, color=colors)
ax.set_xlabel("Digit")
ax.set_ylabel("Posterior mean conditioning weights")
ax.set_xticks(np.arange(model.cond_dim))
fig.tight_layout()
fig.savefig(OUT_PATH / "cvae-mcmc-digit-probs.png")
plt.close(fig)
