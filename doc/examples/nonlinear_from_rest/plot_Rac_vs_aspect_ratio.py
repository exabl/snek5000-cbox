import numpy as np

import matplotlib.pyplot as plt

from critical_Ra_sidewall import Ra_c

# Ra_c = {0.5: 3.2e8, 0.875: 2.855e8, 1.0: 1.875e8, 1.125: 1.125e8}

aspect_ratios = np.array(list(Ra_c.keys()))
Ra_c = np.array(list(Ra_c.values()))

fig, ax = plt.subplots()

ax.plot(aspect_ratios, Ra_c, "o")
Ra_c_theo_old = 1.93e8 * aspect_ratios**-3.15
ax.plot(aspect_ratios, Ra_c_theo_old, "k")


ax.set_yscale("log")
ax.set_xlabel("aspect ratio")
ax.set_ylabel("$Ra_c$")

plt.show()
