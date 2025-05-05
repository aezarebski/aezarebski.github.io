import sys
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import importlib
import cRealNVP
importlib.reload(cRealNVP)

# input_file = "training-data.pt"
# output_model_file = "trained-model.pt"
input_file, output_model_file = sys.argv[1], sys.argv[2]

num_epochs = 20
batch_size = 10
print_every = 5

flow = cRealNVP.CondRealNVP(1, 4, 2)
loss = cRealNVP.NegLogLikelihoodLoss()

# ====================================================================
optimiser = optim.Adam(flow.parameters(), lr=0.001)

data, labels = torch.load(input_file)
dataloader_1 = DataLoader(TensorDataset(data[labels == 0]), batch_size=batch_size, shuffle=True)
dataloader_2 = DataLoader(TensorDataset(data[labels == 1]), batch_size=batch_size, shuffle=True)
dataloader_3 = DataLoader(TensorDataset(data[labels == 2]), batch_size=batch_size, shuffle=True)
dataloader_4 = DataLoader(TensorDataset(data[labels == 3]), batch_size=batch_size, shuffle=True)

results = {
    "loss": []
}

summary_vec_1 = torch.tensor([1, 1]).unsqueeze(0)
summary_vec_2 = torch.tensor([1, -1]).unsqueeze(0)
summary_vec_3 = torch.tensor([-1, 1]).unsqueeze(0)
summary_vec_4 = torch.tensor([-1, -1]).unsqueeze(0)
summary_vec_iter = [summary_vec_1, summary_vec_2, summary_vec_3, summary_vec_4]

for ix in range(num_epochs):
    for mb_tuple in zip(dataloader_1, dataloader_2, dataloader_3, dataloader_4):
        for mb, summary_vec in zip(mb_tuple, summary_vec_iter):
            optimiser.zero_grad()
            batch_loss = loss(mb[0], summary_vec, flow)
            batch_loss.backward()
            optimiser.step()

    results["loss"].append((ix, batch_loss.item()))
    if ix % print_every == 0:
        print(f"Loss at epoch {ix}: {batch_loss}")
# ====================================================================
torch.save(flow, output_model_file)
