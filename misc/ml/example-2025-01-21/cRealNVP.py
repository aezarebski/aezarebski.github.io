import torch
import torch.nn as nn

class CondACB(nn.Module):
    def __init__(self, block_dim: int, summary_dim: int):
        super(CondACB, self).__init__()
        self.block_dim = block_dim
        self.summ_dim = summary_dim
        self.s_nn = nn.Sequential(
            nn.Linear(self.block_dim + self.summ_dim, 32),
            nn.ELU(),
            nn.Linear(32, 32),
            nn.ELU(),
            nn.Linear(32, self.block_dim),
            nn.ELU(),
        )
        self.b_nn = nn.Sequential(
            nn.Linear(self.block_dim + self.summ_dim, 32),
            nn.ELU(),
            nn.Linear(32, 32),
            nn.ELU(),
            nn.Linear(32, self.block_dim),
            nn.ELU()
        )

    def forward(self, x: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        x_a = x[:, : self.block_dim]
        x_b = x[:, self.block_dim :]
        z_a = x_a
        summ_rep = summ.repeat(z_a.size(0), 1)
        x_a_prime = torch.cat([z_a, summ_rep], dim=1)
        z_b = torch.exp(-self.s_nn(x_a_prime)) * (x_b - self.b_nn(x_a_prime))
        return torch.cat([z_a, z_b], dim=1)

    def ln_det_jacobian(self, x: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        x_a = x[:, : self.block_dim]
        summ_rep = summ.repeat(x_a.size(0), 1)
        x_a_prime = torch.cat([x_a, summ_rep], dim=1)
        return torch.sum(-self.s_nn(x_a_prime), dim=1)

    def reverse(self, z: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        z_a = z[:, : self.block_dim]
        z_b = z[:, self.block_dim :]
        x_a = z_a
        summ_rep = summ.repeat(z_a.size(0), 1)
        z_a_prime = torch.cat([z_a, summ_rep], dim=1)
        x_b = torch.exp(self.s_nn(z_a_prime)) * z_b + self.b_nn(z_a_prime)
        return torch.cat([x_a, x_b], dim=1)


class CondRealNVP(nn.Module):
    def __init__(self, block_dim: int, num_flows: int, summary_dim: int):
        super(CondRealNVP, self).__init__()
        self.block_dim = block_dim
        self.num_flows = num_flows
        self.summary_dim = summary_dim
        self.flows = nn.ModuleList([CondACB(block_dim, summary_dim) for _ in range(num_flows)])

    def forward(self, x: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        for f in self.flows:
            x = f(x, summ)
            x = torch.cat([x[:, self.block_dim :], x[:, : self.block_dim]], dim=1)
        return x

    def ln_base_pdf(self, z: torch.Tensor) -> torch.Tensor:
        return -0.5 * torch.sum(z**2, dim=1)

    def ln_det_jacobian(self, x: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        ldjs = torch.zeros(x.size(0))
        for f in self.flows:
            ldjs += f.ln_det_jacobian(x, summ)
            x = f(x, summ)
            x = torch.cat([x[:, self.block_dim :], x[:, : self.block_dim]], dim=1)
        return ldjs

    def reverse(self, z: torch.Tensor, summ: torch.Tensor) -> torch.Tensor:
        # import pdb; pdb.set_trace()
        for f in reversed(self.flows):
            z = torch.cat([z[:, self.block_dim :], z[:, : self.block_dim]], dim=1)
            z = f.reverse(z, summ)
        return z


class NegLogLikelihoodLoss(nn.Module):
    """
    Negative log-likelihood function.
    """

    def __init__(self):
        super(NegLogLikelihoodLoss, self).__init__()

    def forward(
        self, x: torch.Tensor, summ: torch.Tensor, flow: CondRealNVP
    ) -> torch.Tensor:
        z = flow(x, summ)
        ln_base_pdf = flow.ln_base_pdf(z)
        ln_det_jacobian = flow.ln_det_jacobian(x, summ)
        return -torch.mean(ln_base_pdf + ln_det_jacobian)
