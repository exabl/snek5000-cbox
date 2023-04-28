import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from util import save_fig, figsize_halfpage, add_letter
from util_quantities import aspect_ratios, prandtls, get_quantity

# from save_Rec_vs_Pr import Re_As
rc("font", **{"family": "serif", "serif": ["Times"], "size": 16})
rc("text", usetex=True)

omega_norm_As = get_quantity("omega_norm_As")

names_regimes = {
    (1.0, 0.1): "FCC",
    (1.0, 0.2): "SCC",
    (1.0, 0.44): "FACo",
    (1.0, 1.0): "SSCo",
    (1.0, 2.0): "FSP",
    (1.0, 4.0): "FAP",
}

marker_regimes = {
    "FCC": "s",
    "SCC": "+",
    "FACo": "^",
    "SSCo": "*",
    "FSP": "P",
    "FAP": "d",
}


def get_regime(aspect_ratio, prandtl):
    if aspect_ratio == 0.5:
        if prandtl < 0.55:
            return "SCC"
        elif prandtl < 0.8:
            return "FACo"
        elif prandtl < 2.1:
            return "SSCo"
        else:
            return "FSP"

    elif aspect_ratio == 1.0:
        if prandtl < 0.2:
            return "FCC"
        elif prandtl < 0.45:
            return "SCC"
        elif prandtl < 0.63:
            return "FACo"
        elif prandtl < 2.1:
            return "SSCo"
        elif prandtl < 2.9:
            return "FSP"
        else:
            return "FAP"
    elif aspect_ratio == 1.5:
        if prandtl < 0.3:
            return "FCC"
        elif prandtl < 0.45:
            return "SCC"
        elif prandtl < 0.63:
            return "FACo"
        elif prandtl < 2.1:
            return "SSCo"
        else:
            return "FSP"
    elif aspect_ratio == 2.0:
        if prandtl < 0.4:
            return "FCC"
        elif prandtl < 0.63:
            return "FACo"
        elif prandtl < 2.1:
            return "SSCo"
        else:
            return "FSP"


def get_marker(aspect_ratio, prandtl):
    regime = get_regime(aspect_ratio, prandtl)
    try:
        marker = marker_regimes[regime]
    except KeyError:
        marker = "o"
    return marker


fig, ax = plt.subplots()
scale = 200

for i, aspect_ratio in enumerate(aspect_ratios):
    for j, prandtl in enumerate(prandtls):
        width = 1 / aspect_ratio
        im = ax.scatter(
            prandtl,
            aspect_ratio,
            c=np.log10(omega_norm_As[i][j]),
            s=scale,  # * Lh_As[i][j] / width,
            marker=get_marker(aspect_ratio, prandtl),
            vmin=np.log10(np.nanmin(omega_norm_As)),
            vmax=np.log10(np.nanmax(omega_norm_As)),
            # cmap="jet",
        )
        t = (aspect_ratio, prandtl)
        if t in names_regimes:
            ax.text(prandtl, aspect_ratio + 0.05, names_regimes[t])


# plt.legend()
cbar = plt.colorbar(im, ax=ax)
cbar.set_label(r"$\log_{10}(\omega/N_c)$", rotation=90)
ax.set_xlabel(r"$Pr$")
ax.set_ylabel(r"$A$")
ax.set_xscale("log")
add_letter(fig, "b")
plt.tight_layout()

save_fig(fig, "regimes_A_vs_Pr.png")
