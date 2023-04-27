import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

Rac_As = get_quantity("Rac_As")

Re_As = np.empty_like(Rac_As)

fig, ax = plt.subplots(figsize=figsize_halfpage)
for i in range(len(aspect_ratios)):
    for j in range(len(prandtls)):
        Re_As[i][j] = (Rac_As[i][j] ** 0.5) / prandtls[j]

for i in range(len(aspect_ratios)):
    ax.plot(prandtls, Re_As[i], ":s", label=rf"$A={aspect_ratios[i]:.1f}$")

x = np.array([0.1, 1])

ax.plot(x, 1e4 * x ** (0), linestyle="--")

x = np.array([1.2, 4.5])

ax.plot(x, 8e3 * x ** (2), linestyle="--")

plt.text(2.0, 0.8e5, r"$Pr^2$", fontsize=12)

ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$Re_c = Ra_c ^{0.5} / Pr$")
ax.set_xscale("log")
ax.set_yscale("log")
add_letter(fig, "b")
plt.tight_layout()

save_fig(fig, "Rec_vs_Pr.png")
