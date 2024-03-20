# [[file:../post-2024-03-28.org::*Overview][Overview:1]]
import collections
import copy
import time
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score

torch.manual_seed(0)

import numpy as np
import pandas as pd
import plotnine as p9
from plotnine import *

import sys
import os
from pathlib import Path

current_directory = Path(os.getcwd())
sys.path.append(str(current_directory))

import niceneuron.plot as nn_plot
import niceneuron.io as nn_io
import niceneuron.data as nn_data

images_path = "data/train-images.idx3-ubyte"
labels_path = "data/train-labels.idx1-ubyte"
test_images_path = "data/t10k-images.idx3-ubyte"
test_labels_path = "data/t10k-labels.idx1-ubyte"
loss_csv = "example-2024-03-28/loss.csv"
training_png = "example-2024-03-28/training.png"
oc_training_png = "example-2024-03-28/oc_training.png"
oc_scores_png = "example-2024-03-28/oc_scores.png"
results_json = "example-2024-03-28/results.json"
results_dict = {}

cnn_training_epochs = 15
oc_training_epochs = 15

in_labels = [0, 1, 2, 3, 4]

images = nn_io.read_idx(images_path)
images = images.astype(np.float32)
labels = nn_io.read_idx(labels_path)
in_mask = np.isin(labels, in_labels)
labels_in = labels[in_mask]
images_in = images[in_mask]

train_dataset = nn_data.MNISTDataset(
    images_in, labels_in, flatten=False, normalise=True
)
train_dataloader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True
)


test_images = nn_io.read_idx(test_images_path)
test_images = test_images.astype(np.float32)
test_labels = nn_io.read_idx(test_labels_path)
in_mask_test = np.isin(test_labels, in_labels)
test_labels_in = test_labels[in_mask_test]
test_images_in = test_images[in_mask_test]

test_dataset_in = nn_data.MNISTDataset(
    test_images_in, test_labels_in, flatten=False, normalise=True
)
test_dataloader_in = torch.utils.data.DataLoader(
    test_dataset_in, batch_size=64, shuffle=True
)
test_dataset = nn_data.MNISTDataset(
    test_images, test_labels, flatten=False, normalise=True
)
test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=True)
# Overview:1 ends here

# [[file:../post-2024-03-28.org::*CNN classifier][CNN classifier:1]]
class DemoCNN(nn.Module):
    def __init__(self):
        super(DemoCNN, self).__init__()
        self._conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2)
        self._pool1 = nn.AvgPool2d(2)
        self._conv2 = nn.Conv2d(6, 16, kernel_size=5, padding=0)
        self._pool2 = nn.AvgPool2d(2)
        self._fc1 = nn.Linear(5 * 5 * 16, 84)
        self._fc2 = nn.Linear(84, 10)
        self._relu = nn.ReLU()

    def backbone(self, x):
        x = self._pool1(self._relu(self._conv1(x)))
        x = self._pool2(self._relu(self._conv2(x)))
        x = x.view(-1, 5 * 5 * 16)
        return x

    def forward(self, x):
        x = self.backbone(x)
        x = self._relu(self._fc1(x))
        x = self._fc2(x)
        return x
# CNN classifier:1 ends here

# [[file:../post-2024-03-28.org::*Orthonormal certificates][Orthonormal certificates:1]]
class OrthonormalCertificates(nn.Module):
    def __init__(self, dim_in, num_certificates):
        super(OrthonormalCertificates, self).__init__()
        self._dim_in = dim_in
        self._num_certificates = num_certificates
        self._certificates = nn.Parameter(
            torch.randn(self._dim_in, self._num_certificates)
        )

    def forward(self, x):
        # Permute the dimensions of x to vectorise over a batch
        return torch.matmul(self._certificates.t(), x.permute((1, 0)))

    def ctc(self):
        return torch.matmul(self._certificates.t(), self._certificates)

    def get_num_certificates(self):
        return self._num_certificates
# Orthonormal certificates:1 ends here

# [[file:../post-2024-03-28.org::*Training and loss function][Training and loss function:1]]
model = DemoCNN()
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

model.train()
loss_history = []
training_start_time = time.time()
for epoch in range(cnn_training_epochs):
    epoch_cumloss = 0
    for images, label in train_dataloader:
        images = images.unsqueeze(1)
        logits = model(images)
        loss = loss_fn(logits, label)
        epoch_cumloss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch} loss: {epoch_cumloss}")
    loss_history.append((epoch, epoch_cumloss))

training_finish_time = time.time()
print(f"Training took: {training_finish_time - training_start_time}")


loss_df = pd.DataFrame(loss_history, columns=["epoch", "loss"])
loss_df["model"] = "training"
plot_df = loss_df
plot_df.to_csv(loss_csv, index=False)

training_p9 = nn_plot.plot_loss_curve(plot_df) + p9.scale_y_log10()
training_p9.save(training_png, width=10, height=10, dpi=300)


model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, label in test_dataloader_in:
        images = images.unsqueeze(1)
        logits = model(images)
        _, predicted = torch.max(logits, 1)
        total += label.size(0)
        correct += (predicted == label).sum().item()

print(f"Accuracy of the network on the in test images: {100 * correct / total}%")
results_dict["accuracy_on_test_data"] = {
    "correct": correct,
    "total": total,
    "accuracy": 100 * correct / total,
}
# Training and loss function:1 ends here

# [[file:../post-2024-03-28.org::*Training and loss function][Training and loss function:2]]
num_certificates = 1000
oc_model = OrthonormalCertificates(5 * 5 * 16, num_certificates)
oc_optimizer = optim.Adam(oc_model.parameters(), lr=1e-3)

oc_model.train()
oc_loss_history = []
for epoch in range(oc_training_epochs):
    epoch_cumloss = 0
    for images, label in train_dataloader:
        images = images.unsqueeze(1)
        bbs = model.backbone(images)
        oc_loss = torch.mean(torch.square(oc_model(bbs)))
        reg_loss = torch.mean(
            torch.square(oc_model.ctc() - torch.eye(num_certificates))
        )
        loss = oc_loss + 1e-2 * reg_loss
        epoch_cumloss += loss.item()
        oc_optimizer.zero_grad()
        loss.backward()
        oc_optimizer.step()

    print(f"Epoch {epoch} loss: {epoch_cumloss}")
    oc_loss_history.append((epoch, epoch_cumloss))
# Training and loss function:2 ends here

# [[file:../post-2024-03-28.org::*Training and loss function][Training and loss function:3]]
oc_loss_df = pd.DataFrame(oc_loss_history, columns=["epoch", "loss"])
oc_loss_df["model"] = "OC"

oc_training_p9 = (
    nn_plot.plot_loss_curve(oc_loss_df)
    + p9.scale_y_log10()
    + p9.theme(legend_position="none")
)
oc_training_p9.save(oc_training_png, width=5, height=5, dpi=300)

oc_model.eval()
oc_scores = []
oc_labels = []
with torch.no_grad():
    for images, label in test_dataloader:
        images = images.unsqueeze(1)
        bbs = model.backbone(images)
        scores = oc_model(bbs)
        oc_scores.append(torch.sum(torch.square(scores), dim=0))
        oc_labels.append(label)

oc_scores = torch.cat(oc_scores).tolist()
oc_labels = torch.cat(oc_labels).tolist()

oc_df = pd.DataFrame({"score": oc_scores, "label": oc_labels})

oc_p9 = (
    p9.ggplot(oc_df, p9.aes(x="label < 5", y="score"))
    + p9.geom_boxplot()
    + p9.scale_x_discrete(
        breaks=[False, True],
        labels=["Out", "In"],
        name="In/Out of training distribution",
    )
    + p9.scale_y_continuous(name="OC score")
    + p9.theme_minimal()
)

oc_p9.save(oc_scores_png, width=6, height=6, dpi=300)

oc_df_grouped = oc_df
oc_df_grouped["in"] = oc_df_grouped["label"] < 5
oc_df_grouped = oc_df.groupby("in").agg({"score": ["mean", "std"]}).reset_index()
roc_auc = roc_auc_score([0 if ocl < 5 else 1 for ocl in oc_labels], oc_scores)

results_dict["oc_results"] = {"roc_auc": roc_auc}
nn_io.save_dict_to_json(results_json, results_dict)
# Training and loss function:3 ends here
