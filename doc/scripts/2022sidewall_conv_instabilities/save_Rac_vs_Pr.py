import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

Rac_As = get_quantity("Rac_As")

fig, ax = plt.subplots(figsize=figsize_halfpage)


for i in range(len(aspect_ratios)):
    ax.plot(prandtls, Rac_As[i], "s", label=rf"$A={aspect_ratios[i]:.1f}$")

x = np.array([0.1, 1])

ax.plot(x, 1e9 * x ** (2), linestyle="--")
ax.plot(x, 0.5e9 * x ** (3), linestyle="--")

plt.text(2e-1, 1.0e8, r"$Pr^2$", fontsize=12)
plt.text(2e-1, 0.8e6, r"$Pr^3$", fontsize=12)

x = np.array([1, 4.5])

ax.plot(x, 5e7 * x ** (5), linestyle="--")

plt.text(2.5, 0.8e9, r"$Pr^5$", fontsize=12)

ax.legend(loc="upper left", prop={"size": 10})
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$Ra_c$")
ax.set_xscale("log")
ax.set_yscale("log")
add_letter(fig, "a")

plt.tight_layout()

save_fig(fig, "Rac_vs_Pr.png")
