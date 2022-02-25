from shutil import rmtree, copyfile

import pytest

import numpy as np

from snek5000_cbox.solver import Simul
from snek5000 import load
from snek5000 import load_params


@pytest.mark.slow
def test_simple_simul():

    params = Simul.create_default_params()

    aspect_ratio = 1.0
    params.prandtl = 0.71

    # for aspect ratio 1, Ra_c = 1.820e08
    params.rayleigh = 1.845e08

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 8
    params.oper.nx = nb_elements
    params.oper.ny = nb_elements
    params.oper.nz = nb_elements

    Lx = params.oper.Lx = 1.0
    Ly = params.oper.Ly = Lx * aspect_ratio

    params.oper.mesh_stretch_factor = 0.08
    
    params.oper.elem.order = params.oper.elem.order_out = 10

    # creation of the coordinates of the points saved by history points
    n1d = 4
    small = Lx / 10

    xs = np.linspace(0, Lx, n1d)
    xs[0] = small
    xs[-1] = Lx - small

    ys = np.linspace(0, Ly, n1d)
    ys[0] = small
    ys[-1] = Ly - small

    coords = [(x, y) for x in xs for y in ys]

    params.output.history_points.coords = coords
    params.oper.max.hist = len(coords) + 1

    params.nek.general.dt = 0.5
    params.nek.general.time_stepper = "BDF3"
    params.nek.general.stop_at = "endTime"
    params.nek.general.write_control = "runTime"
    params.nek.general.write_interval = params.nek.general.end_time = 150
    params.output.history_points.write_interval = 10
    params.output.phys_fields.write_interval_pert_field = 70

    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"
    params.nek.general.extrapolation = "standard"

    restart_file = "../doc/examples/base_flow.restart"
    params.nek.general.start_from = "base_flow.restart"

    sim = Simul(params)

    copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

    sim.make.exec("run_fg", resources={"nproc": 2})
    
    coords, df = sim.output.history_points.load()

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    assert coords.ndim == 2 and coords.shape == (n1d ** 2, 2)

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)
