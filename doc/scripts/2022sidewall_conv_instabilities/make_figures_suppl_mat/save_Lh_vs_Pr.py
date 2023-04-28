import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

Lh_As = get_quantity("Lh_As")

b = np.empty_like(Lh_As)

for i in range(len(aspect_ratios)):
    for j in range(len(prandtls)):
        width = 1 / aspect_ratios[i]
        Lh = Lh_As[i][j]
        if Lh / width > 0.8:
            Lh = width
        b[i][j] = Lh


fig, ax = plt.subplots(figsize=figsize_halfpage)

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

for i, aspect_ratio in enumerate(aspect_ratios):
    color = colors[i]  # select a color from the list
    # markers = ['s'] * len(prandtls)  # set default marker as square for all points
    marker = "s"
    ax.plot(
        prandtls,
        b[i],
        linestyle="--",
        marker=marker,
        color=color,
        label=rf"$A={aspect_ratio:.1f}$",
    )
    ax.axhline(1 / aspect_ratio, linestyle="--", color=color)

# ax.legend(loc="upper right", prop={"size": 10})
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$L_h/H$")
ax.set_xscale("log")
ax.set_xscale("log")
add_letter(fig, "a")

plt.tight_layout()

save_fig(fig, "Lh_vs_Pr.png")
