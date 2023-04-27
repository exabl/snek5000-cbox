import matplotlib.pyplot as plt

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

Grc_As = get_quantity("Grc_As")

fig, ax = plt.subplots(figsize=figsize_halfpage)

for i in range(len(aspect_ratios)):
    ax.plot(prandtls, Grc_As[i], "o", label=rf"$A={aspect_ratios[i]:.1f}$")

ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$Gr_c$")
ax.set_xscale("log")
ax.set_yscale("log")
add_letter(fig, "b")

plt.tight_layout()

save_fig(fig, "Grc_vs_Pr.png")
