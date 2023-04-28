import matplotlib.pyplot as plt
from matplotlib import rc

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

omega_norm_As = get_quantity("omega_norm_As")

fig, ax = plt.subplots(figsize=figsize_halfpage)

for i in range(len(aspect_ratios)):
    ax.plot(prandtls, omega_norm_As[i], ":s", label=rf"$A={aspect_ratios[i]:.1f}$")

ax.legend(loc="upper right", prop={"size": 10})
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$\omega/N_c$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.axhline(1.0)

add_letter(fig, "a")
plt.tight_layout()
# plt.show()
save_fig(fig, "omega_norm_vs_Pr.png")
