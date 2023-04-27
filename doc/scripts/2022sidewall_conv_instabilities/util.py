from pathlib import Path
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from fluiddyn.util import has_to_be_made as _has_to_be_made

path_base = 'path to directory of datasets'

here = Path(__file__).absolute().parent
tmp_dir = here.parent / "tmp"
tmp_dir.mkdir(exist_ok=True)
sup_mat_dir = tmp_dir / "suppl_mat"
sup_mat_dir.mkdir(exist_ok=True)


def has_to_be_made(name, sources: list):
    if not isinstance(name, str):
        names = name
        return any(has_to_be_made(name, sources) for name in names)

    if isinstance(sources, str):
        sources = [sources]

    sources.append("util.py")

    if not any(name.endswith(ext) for ext in (".png", ".tex", ".gif", ".mp4")):
        name += ".png"

    if "DEBUG" in sys.argv:
        print(f"{tmp_dir / name}, {sources}")

    return _has_to_be_made(tmp_dir / name, sources, source_dir=here)


has_to_save = "SAVE" in sys.argv


def save_fig(fig, name):
    if has_to_save:
        path = tmp_dir / name
        print(f"Saving {path.relative_to(Path.cwd())}")
        fig.savefig(path)
        plt.close(fig)
    else:
        plt.show()


def save_anim(anim, name):
    if has_to_save:
        path = sup_mat_dir / name
        print(f"Saving {path.relative_to(Path.cwd())}")
        anim.save(path)
    else:
        plt.show()


def add_letter(fig, letter):
    fig.text(0.05, 0.95, f"({letter})")


figsize_halfpage = 0.6 * np.array([6.4, 4.8])
