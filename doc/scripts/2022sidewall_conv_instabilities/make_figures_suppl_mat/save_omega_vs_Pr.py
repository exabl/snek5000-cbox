import matplotlib.pyplot as plt

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

omega_As = get_quantity("omega_As")

fig, ax = plt.subplots(figsize=figsize_halfpage)

for i in range(len(aspect_ratios)):
    ax.plot(prandtls, omega_As[i], ":o", label=rf"$A={aspect_ratios[i]:.1f}$")

ax.legend()
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$\omega$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(ymin=0.2, ymax=3.8)
add_letter(fig, "a")
plt.tight_layout()
# plt.show()
save_fig(fig, "omega_vs_Pr.png")
