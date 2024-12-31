import torch
import torch.nn as nn

class RealNVPLayer(nn.Module):
    """
    A single layer of the real NVP
    """
    def __init__(self, dim_a, dim_b):
        super(RealNVPLayer, self).__init__()
        self.dim_a = dim_a
        self.dim_b = dim_b
        self.s_nn = nn.Sequential(
            nn.Linear(dim_a, 64), nn.LeakyReLU(), nn.Linear(64, dim_b), nn.LeakyReLU()
        )
        self.b_bb = nn.Sequential(
            nn.Linear(dim_a, 64), nn.LeakyReLU(), nn.Linear(64, dim_b), nn.LeakyReLU()
        )

    def forward(self, x):
        x_a = x[:, : self.dim_a]
        x_b = x[:, self.dim_a :]
        z_a = x_a
        z_b = torch.exp(-self.s_nn(z_a)) * (x_b - self.b_bb(z_a))
        z = torch.cat([z_a, z_b], dim=1)
        return z

    def ln_det_jacobian(self, x):
        x_a = x[:, : self.dim_a]
        s = self.s_nn(x_a)
        return torch.sum(-s, dim=1)

    def reverse(self, z):
        z_a = z[:, : self.dim_a]
        z_b = z[:, self.dim_a :]
        x_a = z_a
        x_b = torch.exp(self.s_nn(z_a)) * z_b + self.b_bb(z_a)
        x = torch.cat([x_a, x_b], dim=1)
        return x


class RealNVP(nn.Module):
    def __init__(self, dim_a, dim_b, num_flows):
        super(RealNVP, self).__init__()
        assert (num_flows > 0) and (
            num_flows % 2 == 0
        ), "num_flows must be a positive even integer"
        self.dim_a = dim_a
        self.dim_b = dim_b
        self.num_flows = num_flows
        self.flows = nn.ModuleList([RealNVPLayer(dim_a, dim_b) for _ in range(num_flows)])

    def forward(self, x):
        for f in self.flows:
            x = f(x)
            x = torch.cat([x[:, self.dim_a :], x[:, : self.dim_a]], dim=1)
        return x

    def ln_base_pdf(self, z):
        return -0.5 * torch.sum(z**2, dim=1)

    def ln_det_jacobian(self, x):
        ldjs = torch.zeros(x.size(0))
        for f in self.flows:
            ldjs += f.ln_det_jacobian(x)
            x = f(x)
            x = torch.cat([x[:, self.dim_a :], x[:, : self.dim_a]], dim=1)
        return ldjs

    def reverse(self, z):
        for f in reversed(self.flows):
            z = torch.cat([z[:, self.dim_a :], z[:, : self.dim_a]], dim=1)
            z = f.reverse(z)
        return z

    def reverse_with_intermediates(self, z):
        intermediates = []
        for f in reversed(self.flows):
            z = torch.cat([z[:, self.dim_a :], z[:, : self.dim_a]], dim=1)
            z = f.reverse(z)
            intermediates.append(z.detach().numpy())
        return intermediates


class NegLogLikelihoodLoss(nn.Module):
    """
    Negative log-likelihood function.
    """
    def __init__(self):
        super(NegLogLikelihoodLoss, self).__init__()

    def forward(self, x, flow):
        z = flow(x)
        ln_base_pdf = flow.ln_base_pdf(z)
        ln_det_jacobian = flow.ln_det_jacobian(x)
        return -torch.mean(ln_base_pdf + ln_det_jacobian)
