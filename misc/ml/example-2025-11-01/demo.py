import torch
import torch.optim as optim
from torch.distributions.binomial import Binomial
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline
import numpy as np


first_day = 1
last_day = 100
num_flips = 10

days_mesh = torch.arange(first_day, last_day + 1)
prop_heads = 0.5 + 0.25 * torch.sin(2 * 3.14159 * days_mesh / last_day)
num_heads = Binomial(num_flips, prop_heads).sample()

plt.figure()
plt.scatter(days_mesh.numpy(), num_heads.numpy(), facecolors='none', edgecolors='black')
plt.xlabel("Day")
plt.ylabel(f"Number of Heads")
plt.title("Number of Heads in 10 Flips Over 100 Days")
plt.savefig("binomial_data.png")


degree = 3
num_knots = 10
knots = torch.linspace(first_day, last_day, num_knots)
identity_matrix = torch.eye(num_knots + degree - 1)
numpy_knots = np.array([1.0,1.0,1.0] + knots.numpy().tolist() + [last_day,last_day,last_day])
spline_basis = [
    BSpline(numpy_knots, identity_matrix[ix].numpy(), degree)(days_mesh)
    for ix in range(num_knots + degree - 1)
]
spline_basis = torch.tensor(np.array(spline_basis).T,dtype=torch.float32)



def rand_func():
    rand_weights = torch.rand(num_knots + degree - 1)
    return torch.matmul(spline_basis, rand_weights)


fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(days_mesh.numpy(), spline_basis,
        color = "gray", alpha = 0.5)
for col in ["red", "orange", "yellow"]:
    ax.plot(days_mesh.numpy(), rand_func().numpy(),
            color = col)
plt.savefig("bsplines_and_random_function.png")

def neg_llhd(weights):
    probs = torch.matmul(spline_basis, weights)
    return -1 * sum(Binomial(num_flips, probs).log_prob(num_heads))

_weights = torch.rand(num_knots + degree - 1, requires_grad=True)
optimizer = optim.Adam([_weights], lr=0.01)
num_epochs = 2000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    loss = neg_llhd(_weights)
    loss.backward()
    optimizer.step()
    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")


plt.figure()
plt.plot(days_mesh.numpy(), torch.matmul(spline_basis, _weights).detach().numpy(),
         color='blue', label='Fitted Probabilities')
plt.scatter(days_mesh.numpy(), num_heads.numpy() / num_flips, facecolors='none', edgecolors='black')
plt.plot(days_mesh.numpy(), prop_heads.numpy(),
         color='red', label='True Probabilities')
plt.ylim(0, 1)
plt.legend()
plt.savefig("fitted_vs_true_probabilities.png")
