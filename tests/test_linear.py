from shutil import rmtree, copyfile

import pytest

import numpy as np

from snek5000_cbox.solver import Simul
from snek5000 import load
from snek5000 import load_params


@pytest.mark.linear
def test_simple_simul():

    params = Simul.create_default_params()

    aspect_ratio = 1.0
    params.prandtl = 0.71

    # for aspect ratio 1, Ra_c = 1.825E08
    params.rayleigh = 1.81e08

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 8
    params.oper.nx = nb_elements
    params.oper.ny = nb_elements
    params.oper.nz = nb_elements

    Lx = params.oper.Lx = 1.0
    Ly = params.oper.Ly = Lx * aspect_ratio

    params.oper.mesh_stretch_factor = 0.1
    
    params.oper.elem.order = 7

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

    num_steps = params.nek.general.num_steps = 10000
    params.nek.general.write_interval = 500

    params.nek.general.variable_dt = False
    params.nek.general.dt = 0.05
    params.nek.general.time_stepper = "BDF3"
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 500
    params.output.history_points.write_interval = 10

    sim1 = Simul(params)

    sim1.make.exec("run_fg", resources={"nproc": 2})

    sim1 = load(sim1.path_run)
    coords, df = sim1.output.history_points.load()

    assert coords.ndim == 2 and coords.shape == (n1d ** 2, 2)

    times = df[df.index_points == 0].time
    t_max = times.max()

    assert t_max == num_steps * params.nek.general.dt
    assert (
        len(times) == num_steps / params.output.history_points.write_interval + 1
    )

    # check a physical result: since there is no probe close to the center,
    # the temperature values at the end are > 0.15 and < 0.4
    temperature_last = df[df.time == t_max].temperature
    assert temperature_last.abs().max() < 0.4
    assert temperature_last.abs().min() > 0.15

    ## linear simulation

    params = load_params(sim1.path_run)

    params.nek.general.start_from = "base_flow.restart"

    params.rayleigh = 1.845e08
    params.nek.general.write_interval = params.nek.general.end_time
    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"
    params.NEW_DIR_RESULTS = True
    restart_file = params.output.path_session + "/cbox0.f00020"
    params.nek.general.extrapolation = "standard"

    sim2 = Simul(params)

    copyfile(restart_file, sim2.params.output.path_session / "base_flow.restart")

    sim2.make.exec("run_fg", resources={"nproc": 2})

    sim2 = load(sim2.path_run)
    coords, df = sim2.output.history_points.load()

    assert coords.ndim == 2 and coords.shape == (n1d ** 2, 2)

    times = df[df.index_points == 0].time
    t_max = times.max()

    assert t_max == num_steps * params.nek.general.dt
    assert (
        len(times) == num_steps / params.output.history_points.write_interval + 1
    )

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim1.path_run, ignore_errors=True)
    rmtree(sim2.path_run, ignore_errors=True)