import torch
from torch import nn


def set_seed(seed):
    torch.manual_seed(seed)


class VAE(nn.Module):
    def __init__(self, input_dim, hidden_dims, latent_dim, cond_dim=0):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dims = list(hidden_dims)
        self.latent_dim = latent_dim
        self.cond_dim = cond_dim

        encoder_layers = []
        prev_dim = self.input_dim + self.cond_dim
        for hidden_dim in self.hidden_dims:
            encoder_layers.append(nn.Linear(prev_dim, hidden_dim))
            encoder_layers.append(nn.ELU())
            prev_dim = hidden_dim
        self.encoder = nn.Sequential(*encoder_layers)

        self.fc_mu = nn.Linear(self.hidden_dims[-1], self.latent_dim)
        self.fc_logvar = nn.Linear(self.hidden_dims[-1], self.latent_dim)

        decoder_layers = []
        prev_dim = self.latent_dim + self.cond_dim
        for hidden_dim in reversed(self.hidden_dims):
            decoder_layers.append(nn.Linear(prev_dim, hidden_dim))
            decoder_layers.append(nn.ELU())
            prev_dim = hidden_dim
        decoder_layers.append(nn.Linear(prev_dim, self.input_dim))
        decoder_layers.append(nn.Sigmoid())
        self.decoder = nn.Sequential(*decoder_layers)

    def encode(self, x, cond=None):
        if self.cond_dim > 0:
            x = torch.cat([x, cond], dim=1)
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z, cond=None):
        if self.cond_dim > 0:
            z = torch.cat([z, cond], dim=1)
        return self.decoder(z)

    def forward(self, x, cond=None):
        mu, logvar = self.encode(x, cond)
        z = self.reparameterize(mu, logvar)
        x_hat = self.decode(z, cond)
        return x_hat, mu, logvar


# --------------------------------------------------------------------

def vae_loss(x, x_hat, mu, logvar):
    # Reconstruction loss. Wikipedia points to cross-entropy (or MSE)
    # for VAEs, the PyTorch documentation further recommends binary
    # cross-entropy.
    recon = nn.functional.binary_cross_entropy(x_hat, x, reduction="sum")

    # Regularization loss (using the KL-divergence) as described on
    # Wikipedia for the special case of comparing a standard normal to
    # a normal with a diagonal covariance matrix.
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return recon + kl, recon, kl
