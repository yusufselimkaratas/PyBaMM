"""
The components that make up the model.
"""
import numpy as np

def electrolyte_diffusion(c, operators, flux_bcs, source=0):
    """The 1D diffusion equation.

    Parameters
    ----------
    c : array_like, shape (n,)
        The quantity being diffused.
    operators : pybamm.operators.Operators() instance
        The spatial operators.
    flux_bc_left : 2-tuple of array_like, shape (1,)
        Flux at the boundaries (Neumann BC).
    source : int or float or array_like, shape (n,), optional
        Source term in the PDE.

    Returns
    -------
    dcdt : array_like, shape (n,)
        The time derivative.

    """
    # Calculate internal flux
    N_internal = - operators.grad(c)

    # Add boundary conditions (Neumann)
    flux_bc_left, flux_bc_right = flux_bcs
    N = np.concatenate([flux_bc_left, N_internal, flux_bc_right])

    # Calculate time derivative
    dcdt = - operators.div(N) + source

    return dcdt

def electrolyte_current(*variables, operators, current_bcs, source=0):
    """The 1D diffusion equation.

    Parameters
    ----------
    c : array_like, shape (n,)
        The quantity being diffused.
    operators : pybamm.operators.Operators() instance
        The spatial operators.
    flux_bc_left : 2-tuple of array_like, shape (1,)
        Flux at the boundaries (Neumann BC).
    source : int or float or array_like, shape (n,), optional
        Source term in the PDE.

    Returns
    -------
    dedt : array_like, shape (n,)
        The time derivative of the potential.

    """
    # Calculate current density
    i = - current(variables, operators, current_bcs)

    # Calculate time derivative
    dedt = 1/param.gamma_dl * (operators.div(i) + source)

    return dedt

def current(*variables, operators, current_bcs):
    """The 1D diffusion equation.

    Parameters
    ----------
    c : array_like, shape (n,)
        The quantity being diffused.
    operators : pybamm.operators.Operators() instance
        The spatial operators.
    flux_bc_left : 2-tuple of array_like, shape (1,)
        Flux at the boundaries (Neumann BC).
    source : int or float or array_like, shape (n,), optional
        Source term in the PDE.

    Returns
    -------
    dedt : array_like, shape (n,)
        The time derivative of the potential.

    """
    c, e = variables

    lbc, rbc = current_bcs

    # Calculate time derivative
    dedt = 1/param.gamma_dl * (operators.div(i) + source)

    return dedt

def butler_volmer(param, cn, cs, cp, en, ep):
    jn = param.iota_ref_n * cn * np.sinh(en - param.U_Pb(cn))
    js = 0*cs
    jp = (param.iota_ref_p * cp**2 * param.cw(cp)
          * np.sinh(ep - param.U_PbO2(cp)))

    j = np.concatenate([jn, js, jp])
    return j, jn, jp