# [[file:../post-2024-05-02.org::*Thanks][Thanks:1]]
import os

import optuna
from optuna.trial import TrialState

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data
from torchvision import datasets
from torchvision import transforms
import plotly.io as pio


DIR = os.getcwd()
DEVICE = torch.device("cpu")

BATCHSIZE = 128
INPUT_SIZE= 28 * 28
CLASSES = 10
EPOCHS = 5
LOSS_FN = nn.CrossEntropyLoss()

def define_model(trial):
    n_layers = trial.suggest_int("n_layers", 1, 3)
    layers = []

    in_features = INPUT_SIZE
    for i in range(n_layers):
	out_features = trial.suggest_int("n_units_l{}".format(i), 4, 128)
	layers.append(nn.Linear(in_features, out_features))
	layers.append(nn.ReLU())
	p = trial.suggest_float("dropout_l{}".format(i), 0.2, 0.5)
	layers.append(nn.Dropout(p))
	in_features = out_features

    layers.append(nn.Linear(in_features, CLASSES))
    layers.append(nn.LogSoftmax(dim=1))
    return nn.Sequential(*layers)

def get_mnist():
    train_loader = torch.utils.data.DataLoader(
	datasets.MNIST(DIR, train=True, download=True, transform=transforms.ToTensor()),
	batch_size=BATCHSIZE,
	shuffle=True,
    )
    valid_loader = torch.utils.data.DataLoader(
	datasets.MNIST(DIR, train=False, transform=transforms.ToTensor()),
	batch_size=BATCHSIZE,
	shuffle=True,
    )
    return train_loader, valid_loader

def objective(trial):
    model = define_model(trial).to(DEVICE)

    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "SGD"])
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=lr)

    train_loader, valid_loader = get_mnist()

    for epoch in range(EPOCHS):
	model.train()
	for batch_idx, (data, target) in enumerate(train_loader):
	    data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
	    optimizer.zero_grad()
	    output = model(data)
	    loss = LOSS_FN(output, target)
	    loss.backward()
	    optimizer.step()

	model.eval()
	validation_loss = 0
	with torch.no_grad():
	    for batch_idx, (data, target) in enumerate(valid_loader):
		data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
		output = model(data)
		loss = LOSS_FN(output, target)
		validation_loss += loss.item()

	trial.report(validation_loss, epoch)
	if trial.should_prune():
	    raise optuna.exceptions.TrialPruned()

    return validation_loss


if __name__ == "__main__":
    study = optuna.create_study()
    study.optimize(objective, n_trials=100, timeout=600)

    pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
    complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])

    print("Study statistics: ")
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: ", trial.value)

    print("  Params: ")
    for key, value in trial.params.items():
	print("    {}: {}".format(key, value))

    fig_opt_hist = optuna.visualization.plot_optimization_history(study)
    fig_opt_hist.write_image("optuna_history.png")
    fig_opt_hist.write_image("optuna_history.svg")
    fig_int_vals = optuna.visualization.plot_intermediate_values(study)
    fig_int_vals.write_image("optuna_intermediate_values.png")
    fig_int_vals.write_image("optuna_intermediate_values.svg")
    fig_par_cords = optuna.visualization.plot_parallel_coordinate(study)
    fig_par_cords.write_image("optuna_parallel_coordinate.png")
    fig_par_cords.write_image("optuna_parallel_coordinate.svg")
    fig_import_vals = optuna.visualization.plot_param_importances(study)
    fig_import_vals.write_image("optuna_param_importances.png")
    fig_import_vals.write_image("optuna_param_importances.svg")
# Thanks:1 ends here
