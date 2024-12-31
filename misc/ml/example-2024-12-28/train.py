import torch
import torch.optim as optim
from torch.distributions import Categorical, MultivariateNormal
from torch.distributions.multivariate_normal import MultivariateNormal
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt
import pickle
import realNV as realNVP

torch.manual_seed(7)

batch_size = 64
num_epochs = 1000
print_every = 50
num_training_samples = 1000
learning_rate = 0.0002
num_layers = 8


class MixtureOfGaussians:
    def __init__(self, weights, means, covariances):
        self.weights = Categorical(probs=weights)
        self.components = [
            MultivariateNormal(mean, covariance)
            for mean, covariance in zip(means, covariances)
        ]

    def sample(self, sample_shape=torch.Size()):
        num_samples = sample_shape[0]
        rnd_c_ixs = self.weights.sample(sample_shape)
        samples = []
        for i in range(num_samples):
            samples.append(self.components[rnd_c_ixs[i]].sample())
        return torch.stack(samples, dim=0)


mvn_base = MultivariateNormal(torch.tensor([0.0, 0.0]), torch.eye(2))
weights = torch.tensor([0.5, 0.5])
means = [torch.tensor([2.0, 2.0]), torch.tensor([-2.0, -2.0])]
covariances = [torch.eye(2), torch.eye(2)]
mvn_target = MixtureOfGaussians(weights, means, covariances)

training_data = mvn_target.sample((num_training_samples,))


def plot_and_save(x, stem, with_title=True):
    plt.figure()
    plt.scatter(x[:, 0], x[:, 1])
    if with_title:
        plt.title(f"Mean of x: {np.mean(x, axis=0)}")
    plt.savefig(stem + ".png")
    plt.close()
    np.savetxt(stem + ".csv", x, fmt="%.4f", delimiter=",")


tmp = training_data.detach().numpy()
plot_and_save(tmp, "training_data")
del tmp


flow = realNVP.RealNVP(1, 1, num_layers)

z = flow(training_data).detach().numpy()
plot_and_save(z, "z_0")

loss = realNVP.NegLogLikelihoodLoss()

# ====================================================================
optimiser = optim.Adam(flow.parameters(), lr=learning_rate)

dataset = TensorDataset(training_data)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

for i in range(num_epochs):
    for minibatch in dataloader:
        x_batch = minibatch[0]
        optimiser.zero_grad()
        batch_loss = loss(x_batch, flow)
        batch_loss.backward()
        optimiser.step()

    if i % print_every == 0:
        print(f"Loss at epoch {i}: {batch_loss}")
# ====================================================================


z = flow(training_data).detach().numpy()
plot_and_save(z, "z_1")

test_data = mvn_base.sample((1000,))
x = flow.reverse(test_data).detach().numpy()
plot_and_save(x, "x_1")

x_intermediates = flow.reverse_with_intermediates(test_data)

fig, axs = plt.subplots(8 + 1, 1, figsize=(5, 40 + 5))
for ix, x in enumerate(x_intermediates):
    axs[ix].scatter(x[:, 0], x[:, 1])
axs[-1].scatter(training_data[:, 0], training_data[:, 1], color="red")
fig.tight_layout()
plt.savefig("x_1_intermediates.png")

with open("training-results.pkl", "wb") as f:
    pickle.dump(
        {
            "training_data": training_data,
            "intermediates": x_intermediates,
        },
        f,
    )
