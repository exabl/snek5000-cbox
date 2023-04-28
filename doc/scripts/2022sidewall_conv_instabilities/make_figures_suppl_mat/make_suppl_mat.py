from subprocess import run

from util import has_to_be_made, here
from util_quantities import aspect_ratios, prandtls


def make_anim(name, source, args=None):
    if has_to_be_made(name, source):
        command = ["python", here / source, "SAVE"]

        if args is not None:
            command.extend(str(arg) for arg in args)

        run(command, check=True)


for aspect_ratio in aspect_ratios:
    for prandtl in prandtls:
        if (aspect_ratio in [0.5, 1.5, 2.0]) and prandtl == 4.0:
            continue
        else:
            make_anim(
                f"suppl_mat/anim_base_pert_A{aspect_ratio:.2f}_Pr{prandtl:.2f}.gif",
                source="save_anim_base_pert.py",
                args=[aspect_ratio, prandtl],
            )
            make_anim(
                f"suppl_mat/anim_vort_pert_A{aspect_ratio:.2f}_Pr{prandtl:.2f}.gif",
                source="save_anim_vort_pert.py",
                args=[aspect_ratio, prandtl],
            )
            make_anim(
                f"suppl_mat/anim_base_pert_stream_A{aspect_ratio:.2f}_Pr{prandtl:.2f}.gif",
                source="save_anim_base_pert_stream.py",
                args=[aspect_ratio, prandtl],
            )