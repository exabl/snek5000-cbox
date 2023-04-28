import matplotlib.pyplot as plt
from matplotlib import rc

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

Nc_As = get_quantity("Nc_As")

fig, ax = plt.subplots(figsize=figsize_halfpage)

for i in range(len(aspect_ratios)):
    ax.plot(prandtls, Nc_As[i], ":s", label=rf"$A={aspect_ratios[i]:.1f}$")

ax.legend(loc="upper left", prop={"size": 10})
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$N_c$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(ymin=0.2, ymax=3.8)
add_letter(fig, "b")
plt.tight_layout()
# plt.show()
save_fig(fig, "Nc_vs_Pr.png")
