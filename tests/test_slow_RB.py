from shutil import rmtree

import pytest

import numpy as np

from snek5000_cbox.solver import Simul
from snek5000 import load


@pytest.mark.slow
def test_simple_simul():

    params = Simul.create_default_params()

    aspect_ratio = 9.0
    params.prandtl = 0.71

    params.rayleigh = 3000

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.dim = 2

    params.oper.delta_T_vertical = 1.0

    nb_elements = ny = 1
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements * aspect_ratio)
    params.oper.nz = int(nb_elements * aspect_ratio)

    Ly = params.oper.Ly = 1.0
    Lx = params.oper.Lx = Ly * aspect_ratio
    Lz = params.oper.Lz = Ly * aspect_ratio

    params.oper.elem.order = params.oper.elem.order_out = 7

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

    num_steps = params.nek.general.num_steps = 5000
    params.nek.general.write_interval = 500

    params.nek.general.variable_dt = False
    params.nek.general.dt = -0.005
    params.nek.general.time_stepper = "BDF3"
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 500
    params.output.history_points.write_interval = 10

    sim = Simul(params)

    sim.make.exec("run_fg", resources={"nproc": 2})

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    assert coords.ndim == 2 and coords.shape == (n1d ** 2, 2)

    times = df[df.index_points == 0].time
    t_max = times.max()

    assert t_max == num_steps * abs(params.nek.general.dt)
    assert len(times) == num_steps / params.output.history_points.write_interval + 1

    # check a physical result: since there is no probe close to the center,
    temperature_last = df[df.time == t_max].temperature
    assert temperature_last.abs().max() < 0.45
    assert temperature_last.abs().min() > 0.0

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)
