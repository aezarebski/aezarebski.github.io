import sys
import torch
import pandas as pd
import plotnine as p9

# input_file = "training-data.pt"
# output_png = "foobar.png"
input_file, output_png = sys.argv[1], sys.argv[2]

data, labels = torch.load(input_file)
df_data = pd.DataFrame(data.numpy(), columns=["x", "y"])
df_labels = pd.DataFrame(labels.numpy(), columns=["label"])
df_labels["label"] = df_labels["label"].astype("category")
plot_df = pd.concat([df_data, df_labels], axis=1)

plot = (
    p9.ggplot(plot_df) +
    p9.geom_point(mapping = p9.aes(x="x", y="y", color="label"),
                  alpha=0.25) +
    p9.labs(title="Training Data") +
    p9.xlim(-3, 3) +
    p9.ylim(-3, 3) +
    p9.theme_bw() +
    p9.theme(axis_title_x=p9.element_blank(),
             axis_title_y=p9.element_blank()) +
    p9.coord_fixed()
)

# print(plot)
p9.ggsave(plot, output_png, width=6, height=6, dpi=300)
