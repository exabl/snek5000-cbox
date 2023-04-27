import sys
from runpy import run_path

from util import has_to_be_made, here
from util_quantities import aspect_ratios, prandtls


def make_output(name, source=None, args=None):
    if source is None:
        source = f"save_{name}.py"
    if has_to_be_made(name, source):
        if args is not None:
            for arg in args:
                sys.argv.append(str(arg))
        print(f"Calling {source} to make {name}")

        if isinstance(source, list):
            source = source[0]

        run_path(here / source)

        if args is not None:
            for arg in args:
                del sys.argv[-1]


if __name__ == "__main__":
    print(f"{aspect_ratios = }")
    print(f"{prandtls = }")

    for prandtl in prandtls:
        if prandtl == 4.0:
            continue
        else:
            make_output(
                f"base_state_stream_subplots_Pr{prandtl:.2f}",
                source="save_base_flow_stream_subplotsPr.py",
                args=[prandtl],
            )

    for aspect_ratio in aspect_ratios:
        make_output(
            f"base_state_stream_subplots_A{aspect_ratio:.2f}",
            source="save_base_flow_stream_subplotsA.py",
            args=[aspect_ratio],
        )

    for aspect_ratio in aspect_ratios:
        for prandtl in prandtls:
            if (aspect_ratio in [0.5, 1.5, 2.0]) and prandtl == 4.0:
                continue
            else:
                make_output(
                    f"base_stream_amp_phase_A{aspect_ratio:.2f}_Pr{prandtl:.2f}",
                    source="save_base_stream_amp_phase_maps_regimes.py",
                    args=[aspect_ratio, prandtl],
                )

    make_output("omega_norm_vs_Pr", source="save_omega_norm_vs_Pr.py")
    make_output("regimes_A_vs_Pr", source="save_regimes_A_vs_Pr.py")
    make_output("Rac_vs_Pr", source="save_Rac_vs_Pr.py")
    make_output("Grc_vs_Pr", source="save_Grc_vs_Pr.py")
    make_output("Lh_vs_Pr", source="save_Lh_vs_Pr.py")
    make_output("Rec_vs_Pr", source="save_Rec_vs_Pr.py")
    make_output("Nc_vs_Pr", source="save_Nc_vs_Pr.py")
    make_output("omega_vs_Pr", source="save_omega_vs_Pr.py")
    make_output(
        "geometry_sketch", source=["save_geometry_sketch.py", "util_sketch.py"]
    )
    make_output(
        "diagnostic_sketch",
        source=["save_diagnostic_sketch.py", "util_sketch.py"],
    )
    make_output(
        "base_amp_maps_corner_regimes",
        source="save_base_amp_maps_corner_regimes.py",
    )
    make_output("graphical_abstract", source="save_graphical_abstract.py")
