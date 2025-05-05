import sys
import torch
import pandas as pd
import plotnine as p9
import cRealNVP

# input_model_file = "trained-model.pt"
# output_png = "barfoo.png"
# output_extra_png = "barfoo-extra.png"
input_model_file, output_png, output_extra_png = sys.argv[1], sys.argv[2], sys.argv[3]

flow = torch.load(input_model_file)

summ_1 = torch.tensor([1, 1]).unsqueeze(0)
summ_2 = torch.tensor([1, -1]).unsqueeze(0)
summ_3 = torch.tensor([-1, 1]).unsqueeze(0)
summ_4 = torch.tensor([-1, -1]).unsqueeze(0)

testing_data = torch.randn(1000, 2)
testing_output_1 = flow.reverse(testing_data, summ_1)
testing_output_2 = flow.reverse(testing_data, summ_2)
testing_output_3 = flow.reverse(testing_data, summ_3)
testing_output_4 = flow.reverse(testing_data, summ_4)

plot_df_1 = pd.DataFrame(testing_output_1.detach().numpy(), columns=["x", "y"])
plot_df_1["label"] = "0"
plot_df_2 = pd.DataFrame(testing_output_2.detach().numpy(), columns=["x", "y"])
plot_df_2["label"] = "1"
plot_df_3 = pd.DataFrame(testing_output_3.detach().numpy(), columns=["x", "y"])
plot_df_3["label"] = "2"
plot_df_4 = pd.DataFrame(testing_output_4.detach().numpy(), columns=["x", "y"])
plot_df_4["label"] = "3"

plot_df = pd.concat([plot_df_1, plot_df_2, plot_df_3, plot_df_4], axis=0)
plot_df["label"] = plot_df["label"].astype("category")


plot = (
    p9.ggplot(plot_df) +
    p9.geom_point(mapping = p9.aes(x="x", y="y", color="label"),
                  alpha=0.25) +
    p9.labs(title="Generated Data") +
    p9.xlim(-3, 3) +
    p9.ylim(-3, 3) +
    p9.theme_bw() +
    p9.theme(axis_title_x=p9.element_blank(),
             axis_title_y=p9.element_blank()) +
    p9.coord_fixed()
)

# print(plot)
p9.ggsave(plot, output_png, width=6, height=6, dpi=300)

summ_extra = torch.tensor([0, 2]).unsqueeze(0)
testing_output_extra = flow.reverse(testing_data, summ_extra)
plot_df_extra = pd.DataFrame(testing_output_extra.detach().numpy(), columns=["x", "y"])

plot_extra = (
    p9.ggplot() +
    p9.geom_point(data = plot_df,
                  mapping = p9.aes(x="x", y="y"),
                  colour="green",
                  alpha=0.15) +
    p9.geom_point(data = plot_df_extra,
                  mapping = p9.aes(x="x", y="y"),
                  colour="purple",
                  alpha=0.25) +
    p9.labs(title="Extrapolated Data") +
    p9.xlim(-3, 3) +
    p9.ylim(-3, 3) +
    p9.theme_bw() +
    p9.theme(axis_title_x=p9.element_blank(),
             axis_title_y=p9.element_blank()) +
    p9.coord_fixed()
)

# print(plot_extra)
p9.ggsave(plot_extra, output_extra_png, width=6, height=6, dpi=300)
