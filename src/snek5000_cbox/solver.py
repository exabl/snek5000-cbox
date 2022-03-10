from pytest import param
from snek5000.info import InfoSolverMake

from snek5000.solvers.kth import SimulKTH


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

        self.par_sections_disabled = ("mesh", "scalar01", "cvode")


class SimulCbox(SimulKTH):
    """A solver which compiles and runs using a Snakefile."""

    InfoSolver = InfoSolverCbox

    @classmethod
    def _complete_params_with_default(cls, params):
        """Add missing default parameters."""
        params = super()._complete_params_with_default(params)
        params._set_attribs({"prandtl": 0.71, "rayleigh": 1.8e8})
        params._record_nek_user_params({"prandtl": 1, "rayleigh": 2})
        return params

    @classmethod
    def create_default_params(cls):
        """Set default values of parameters as given in reference
        implementation.

        """
        params = super().create_default_params()

        params.oper.nproc_min = 2

        params.nek.velocity.density = 1.0
        params.nek.temperature.rho_cp = 1.0

        params.nek.temperature.residual_tol = 1e-14
        params.nek.velocity.residual_tol = 1e-14
        params.nek.pressure.residual_tol = 1e-14

        params.oper._set_attribs({"mesh_stretch_factor": 0.0})
        params.oper._record_nek_user_params({"mesh_stretch_factor": 4})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for mesh stretching in .usr file (subroutine usrdat2):

- ``mesh_stretch_factor``: float
  
  Mesh stretch factor (default = 0.0, meaning no stretching). 
  The locations of the grid points are changed in the 3 directions (x, y, z)
  as follow: ``x_i  = x_i - stretch_factor_x*(sin(2pi*x_i/L_x))``.
  The stretching factors in different directions are computed such that
  elements at the corners are of aspect ratio 1. Typical reasonable values 
  could be between 0.05 and 0.1. 0.15 corresponds to a very strongly stretched 
  mesh.
"""
        )

        params.oper._set_attribs({"delta_T_lateral": 0.0})
        params.oper._record_nek_user_params({"delta_T_lateral": 5})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for lateral temperature difference in .usr file (subroutine userbc):

- ``delta_T_lateral``: float
  
  Lateral temperature difference (default = 0.0, meaning no temperature difference). 
  
"""
        )

        params.oper._set_attribs({"delta_T_vertical": 0.0})
        params.oper._record_nek_user_params({"delta_T_vertical": 6})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for vertical temperature difference in .usr file (subroutine userbc):

- ``delta_T_lateral``: float
  
  Vertical temperature difference (default = 0.0, meaning no temperature difference). 
  
"""
        )

        params.oper._set_attribs({"noise_amplitude": 1e-7})
        params.oper._record_nek_user_params({"noise_amplitude": 7})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for noise amplitude in .usr file (subroutine useric):

- ``noise_amplitude``: float
  
  Noise amplitude for initial condition(default = 1e7). 
  
"""
        )

        params.output.phys_fields._set_attribs(
            {"write_interval_pert_field": 1000},
        )
        params.output.phys_fields._record_nek_user_params(
            {"write_interval_pert_field": 3}
        )

        return params

    def __init__(self, params):

        if params.oper.delta_T_lateral == 1.0 and params.oper.delta_T_vertical == 0.0:
            if params.oper.dim == 2:

                params.oper.boundary = ["W"] * 4
                params.oper.boundary_scalars = ["t"] * 2 + ["I"] * 2

            else:

                params.oper.boundary = ["W"] * 6
                params.oper.boundary_scalars = ["t"] * 2 + ["I"] * 4

            params.nek.velocity.viscosity = params.prandtl / params.rayleigh ** (1 / 2)
            params.nek.temperature.conductivity = 1.0 / params.rayleigh ** (1 / 2)

        elif params.oper.delta_T_lateral == 0.0 and params.oper.delta_T_vertical == 1.0:
            if params.oper.dim == 2:

                params.oper.boundary = ["P"] * 2 + ["W"] * 2
                params.oper.boundary_scalars = ["P"] * 2 + ["t"] * 2

            else:

                params.oper.boundary = ["P"] * 2 + ["W"] * 2 + ["P"] * 2
                params.oper.boundary_scalars = ["P"] * 2 + ["t"] * 2 + ["P"] * 2

            params.nek.velocity.viscosity = params.prandtl
            params.nek.temperature.conductivity = 1.0

        elif params.oper.delta_T_lateral == 1.0 and params.oper.delta_T_vertical == 1.0:
            if params.oper.dim == 2:

                params.oper.boundary = ["W"] * 4
                params.oper.boundary_scalars = ["t"] * 2 + ["t"] * 2

            else:

                params.oper.boundary = ["W"] * 6
                params.oper.boundary_scalars = ["t"] * 4 + ["I"] * 2

            params.nek.velocity.viscosity = params.prandtl / params.rayleigh ** (1 / 2)
            params.nek.temperature.conductivity = 1.0 / params.rayleigh ** (1 / 2)

        super().__init__(params)


Simul = SimulCbox
