#
# Base class for particle cracking models.
#
import pybamm


class BaseCracking(pybamm.BaseSubModel):
    """Base class for particle cracking models.
    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    domain : dict, optional
        Dictionary of either the electrode for "Positive" or "Nagative" 
    **Extends:** :class:`pybamm.BaseSubModel`
    """
    def __init__(self, param, domain):
        self.domain = domain
        super().__init__(param)

    def get_fundamental_variables(self):
        l_cr_n=pybamm.Variable("Negative electrode particle crack length [m]")  # crack length in anode particles
        variables = {"Negative electrode particle crack length [m]": l_cr_n}
        variables.update(self._get_standard_surface_variables(l_cr_n))
        return variables

    def _get_standard_surface_variables(self, l_cr_n):
        """
        A private function to obtain the standard variables which
        can be derived from the local particle crack surfaces.
        Parameters
        ----------
        l_cr_n : :class:`pybamm.Symbol`
            The crack length in anode particles.
        Returns
        -------
        variables : dict
        The variables which can be derived from the crack length.
        """
        rho_cr=pybamm.mechanical_parameters.rho_cr
        w_cr=pybamm.mechanical_parameters.w_cr
        a_n=pybamm.standard_parameters_lithium_ion.a_n
        a_n_cr= a_n*l_cr_n*2*w_cr*rho_cr # crack surface area

        a_n_cr_xavg=pybamm.x_average(a_n_cr)
        variables = {
            "Crack surface to volume ratio [m-1]": a_n_cr,
            "X-averaged crack surface to volume ratio [m-1]": a_n_cr_xavg,
        }
        return variables