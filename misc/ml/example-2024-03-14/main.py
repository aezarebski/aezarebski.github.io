# [[file:../post-2024-03-14.org::*Overview][Overview:1]]
import time
import sys
import os
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import normal, uniform, beta
import pandas as pd
import plotnine as p9
from plotnine import *

current_directory = Path(os.getcwd())
sys.path.append(str(current_directory.parent))
import niceneuron.plot as nn_plot

torch.manual_seed(0)
# Overview:1 ends here

# [[file:../post-2024-03-14.org::*Model and loss function][Model and loss function:1]]
class LocationNB(nn.Module):
    def __init__(self, m):
        super(LocationNB, self).__init__()
        self._m = m  # dataset size: {z_1,...,z_m}
        self._num_S = 3  # number of summary statistics
        self._q = 10  # latent dimension
        self._p = 1  # output dimension

        self._phi = nn.Sequential(
            nn.Linear(self._num_S + 1, self._q),
            nn.Sigmoid(),
            nn.Linear(self._q, self._q),
            nn.Sigmoid(),
            nn.Linear(self._q, self._p),
        )

    def signed_sqrt(self, x):
        return torch.sign(x) * torch.sqrt(torch.abs(x))

    def forward(self, x, tau):
        s0 = torch.median(x, dim=1).values
        s1 = torch.mean(x, dim=1)
        s2 = torch.mean(x**2, dim=1)
        tmp = torch.stack([s0, s1, s2], dim=1)
        tmp = self.signed_sqrt(tmp)
        tmp = torch.cat([tmp, tau.unsqueeze(1)], dim=1)
        return self._phi(tmp).squeeze(1)
# Model and loss function:1 ends here

# [[file:../post-2024-03-14.org::*Model and loss function][Model and loss function:2]]
class PinballLoss(nn.Module):
    def __init__(self):
        super(PinballLoss, self).__init__()

    def forward(self, predictions, targets, tau):
        err = targets - predictions
        loss = torch.where(err >= 0, tau * err, (tau - 1) * err)
        return torch.mean(loss)
# Model and loss function:2 ends here

# [[file:../post-2024-03-14.org::*Training loop][Training loop:2]]
def rand_dataset(num_replicates: int, replicate_size: int):
    mu_i = normal.Normal(torch.tensor([0.0]), torch.tensor([10.0])).sample(
        sample_shape=torch.Size([num_replicates])
    )
    x_i = (
        normal.Normal(loc=mu_i, scale=torch.tensor([1.0]))
        .sample(sample_shape=torch.Size([replicate_size]))
        .transpose(0, 1)
        .squeeze(2)
    )
    y_i = mu_i.squeeze(1)
    return y_i, x_i


def train_model(model, tau_dist, num_steps, train_data_gen):
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_function = PinballLoss()
    model.train()
    loss_history = []
    for step in range(num_steps):
        train_y, train_x = train_data_gen()
        train_tau = tau_dist.sample(sample_shape=train_y.shape).squeeze(1)
        preds = model(train_x, train_tau)
        loss = loss_function(preds, train_y, train_tau)
        step_loss = loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 500 == 0:
            print(f"Step {step} loss: {step_loss:.4f}")
            loss_history.append((step, step_loss))

    return model, loss_history


def record_loss_details(loss_history, loss_csv, loss_png, title_str):
    loss_df = pd.DataFrame(loss_history, columns=["step", "loss"])
    loss_df.to_csv(loss_csv)
    loss_p9 = nn_plot.plot_loss_curve(loss_df, x_var="step", x_lab="")
    loss_p9 = (
        loss_p9
        + ggtitle(title_str)
        + theme(plot_title=element_text(size=10, weight="bold"))
    )
    loss_p9.save(loss_png, height=2.9, width=4.1)


def test_coverage(model, xs, ys, alphas, num_replicates):
    coverage_results = []
    for ix in range(alphas.shape[0]):
        tau_0 = (0.5 * alphas[ix]).repeat(num_replicates)
        tau_1 = 1 - tau_0
        est_lower = model(xs, tau_0)
        est_upper = model(xs, tau_1)
        correct = torch.sum((est_lower <= ys) & (ys <= est_upper)).item()
        coverage_results.append((alphas[ix].item(), correct, num_replicates))
    coverage_df = pd.DataFrame(coverage_results, columns=["alpha", "correct", "total"])
    mse_of_coverage_err = (
        ((1 - coverage_df["alpha"]) - (coverage_df["correct"] / coverage_df["total"]))
        ** 2
    ).mean()
    return coverage_df, mse_of_coverage_err


def test_accuracy(model, xs, ys, num_replicates):
    tau_mid = torch.tensor([0.5]).repeat(num_replicates)
    est = model(xs, tau_mid)
    if est.dim() == 2:
        est = est.squeeze(1)
    point_df = pd.DataFrame(
        zip(est.tolist(), ys.tolist()), columns=["point_estimate", "truth"]
    )
    point_mse = ((point_df["point_estimate"] - point_df["truth"]) ** 2).mean()
    return point_df, point_mse


def plot_points(point_df, mse, title, filename):
    p = (
        ggplot(point_df, aes(x="truth", y="point_estimate"))
        + geom_point()
        + geom_abline(intercept=0, slope=1, color="red")
        + labs(x="Truth", y="Prediction", title=title, subtitle=f"MSE: {mse:.3f}")
        + theme_bw()
        + theme(plot_title=element_text(size=10, weight="bold"))
    )
    p.save(filename, height=2.9, width=4.1)


def plot_coverage(coverage_df, mse_error, title, filename):
    p = (
        ggplot(
            coverage_df,
            aes(
                x="1-alpha", y="correct/total", shape="((correct/total) >= (1 - alpha))"
            ),
        )
        + geom_point()
        + geom_abline(intercept=0, slope=1, color="red")
        + scale_x_continuous(limits=(0, 1))
        + scale_y_continuous(limits=(0, 1))
        + labs(
            x="Desired coverage: α",
            y="Proportion: correct/total",
            title=title,
            subtitle=f"Proportion error MSE: {mse_error:.3f}",
        )
        + theme_bw()
        + theme(plot_title=element_text(size=10, weight="bold"), legend_position="none")
    )
    p.save(filename, height=2.9, width=4.1)

loss_a_png = "loss-a.png"
loss_a_csv = "loss-a.csv"
coverage_a_png = "coverage-a.png"
points_a_png = "points-a.png"
loss_b_png = "loss-b.png"
loss_b_csv = "loss-b.csv"
coverage_b_png = "coverage-b.png"
points_b_png = "points-b.png"

replicate_size = 10
train_num_replicates = 1000
train_num_steps = 20000
test_num_replicates = 10000

test_y, test_x = rand_dataset(test_num_replicates, replicate_size)
test_alpha = torch.linspace(0.05, 0.95, steps=20)
train_data_gen = lambda: rand_dataset(train_num_replicates, replicate_size)
# Training loop:2 ends here

# [[file:../post-2024-03-14.org::*Training loop][Training loop:3]]
model_title = "Base model"
loc_nb_a = LocationNB(replicate_size)
loc_nb_a, loss_history_a = train_model(
    loc_nb_a,
    uniform.Uniform(torch.tensor([0.0]), torch.tensor([1.0])),
    train_num_steps,
    train_data_gen,
)

record_loss_details(loss_history_a, loss_a_csv, loss_a_png, model_title)
coverage_a_df, mse_of_coverage_a_err = test_coverage(
    loc_nb_a, test_x, test_y, test_alpha, test_num_replicates
)
point_a_df, point_mse_a = test_accuracy(loc_nb_a, test_x, test_y, test_num_replicates)
plot_coverage(coverage_a_df, mse_of_coverage_a_err, model_title, coverage_a_png)
plot_points(point_a_df, point_mse_a, model_title, points_a_png)
# Training loop:3 ends here

# [[file:../post-2024-03-14.org::*Training loop][Training loop:4]]
model_title = "Beta tau samples model"
loc_nb_b = LocationNB(replicate_size)
loc_nb_b, loss_history_b = train_model(
    loc_nb_b,
    beta.Beta(torch.tensor([0.5]), torch.tensor([0.5])),
    train_num_steps,
    train_data_gen,
)

record_loss_details(loss_history_b, loss_b_csv, loss_b_png, model_title)
coverage_b_df, mse_of_coverage_b_err = test_coverage(
    loc_nb_b, test_x, test_y, test_alpha, test_num_replicates
)
point_b_df, point_mse_b = test_accuracy(loc_nb_b, test_x, test_y, test_num_replicates)
plot_coverage(coverage_b_df, mse_of_coverage_b_err, model_title, coverage_b_png)
plot_points(point_b_df, point_mse_b, model_title, points_b_png)
# Training loop:4 ends here
