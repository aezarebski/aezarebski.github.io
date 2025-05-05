import sys
import torch
import torch.distributions as dist

# output_file = "training-data.pt"
output_file = sys.argv[1]

torch.manual_seed(0)

num_per_mode = 1000
num_modes = 4
num_features = 2

tmp = 0.25 * torch.randn(num_per_mode * num_modes, num_features)
means = torch.tensor([[1,1], [1,-1], [-1,1], [-1,-1]]).repeat_interleave(num_per_mode, dim=0)
data = tmp + means

labels = torch.arange(num_modes).repeat_interleave(num_per_mode)

torch.save((data, labels), output_file)
