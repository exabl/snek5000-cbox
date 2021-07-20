from snek5000.info import InfoSolverMake
from snek5000.solvers.base import SimulNek
# To use KTH Framework import SimulKTH instead
# from snek5000.solvers.kth import SimulKTH


class InfoSolverCbox(InfoSolverMake):
    """Contain the information on a :class:`snek5000_cbox.solver.Simul`
    instance.

    """

    def _init_root(self):
        super()._init_root()
        self.module_name = "snek5000_cbox.solver"
        self.class_name = "Simul"
        self.short_name = "cbox"

        self.classes.Output.module_name = "snek5000_cbox.output"
        self.classes.Output.class_name = "OutputCbox"


class SimulCbox(SimulNek):
    """A solver which compiles and runs using a Snakefile.

    """
    InfoSolver = InfoSolverCbox

    @staticmethod
    def _complete_params_with_default(params):
        """Add missing default parameters."""
        params = SimulNek._complete_params_with_default(params)
        # Extend with new default parameters here, for example:

        # params.nek.velocity._set_attrib("advection", True)
        return params

    @classmethod
    def create_default_params(cls):
        """Set default values of parameters as given in reference
        implementation.

        """
        params = super().create_default_params()
        # Re-define default values for parameters here, if necessary
        # following ``cbox.par``, ``cbox.box`` and ``SIZE`` files

        params.oper.dim = 2

        params.oper.Lx = 1
        params.oper.Ly = 1
        params.oper.Lz = 1

        params.oper.boundary = ['W', 'W', 'W', 'W']
        params.oper.boundary_scalars = ['t', 't', 'I', 'I']

        params.nek.temperature.conductivity = 1.
        params.nek.problemtype.variable_properties = True

        params.oper.elem.order = 9
        params.oper.elem.order_out = 9

        # params.nek.general.time_stepper = "BDF3"

        params.nek.general.user_params = {2: 0.71, 3: 1.8e8}

        return params


Simul = SimulCbox
