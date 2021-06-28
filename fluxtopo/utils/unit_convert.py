import numpy as np
from utils import met_utils
from utils import constants as c


# Wind speed and direction
# based on http://tornado.sfsu.edu/geosciences/classes/m430/Wind/WindDirection.html
def uv_to_wswd(u, v):
    """

    Args:
        u (float) : u component of wind vector (positive east) [m/s]
        v (float) : v component of wind vector (positive north) [m/s]

    Returns:
        ws (float) : Wind speed [m/s]
        wd (float) : Wind direction in meteorological degrees (0 North, 90 East) [deg]
    """

    ws = np.sqrt(u**2 + v**2)
    wd = np.mod(np.degrees(np.arctan2(-u, -v)), 360)

    return ws, wd


def wswd_to_uv(ws, wd):
    """

    Args:
        ws (float) : Wind speed [m/s]
        wd (float) : Wind direction in meteorological degrees (0 North, 90 East) [deg]

    Returns:
        u (float) : u component of wind vector (positive east) [m/s]
        v (float) : v component of wind vector (positive north) [m/s]

    """

    u = - ws * np.sin(np.radians(wd))
    v = - ws * np.cos(np.radians(wd))

    return u, v


# Gases

def ppm_to_pa(ppm, pres):
    """
    Convert ppm (umol mol^-1) to a partial pressure

    Args:
        ppm (float) : ppm of gas [umol mol^-1]
        pres (float) : atmospheric pressure [Pa]

    Returns:
        pa (float) : partial pressure of gas [Pa]
    """

    pa = ppm * 1e-6 * pres

    return pa


def umol_to_sm(gs, t, pres=860e2):
    """
    Convert resistance in s m^2 umol^-1 to s m^-1
    From CLM5 Docs
    """

    sm = 1e-9 * c.R_g * 1e3 * (met_utils.potential_temp(t, pres) / pres) * gs

    return sm


def sm_to_umol(gs, t, pres=860e2):
    """
    Convert resistance in s m^-1 to s m^2 umol^-1
    From CLM5 Docs
    """

    umol = gs / (1e-9 * c.R_g * 1e3 * (met_utils.potential_temp(t, pres) / pres))

    return umol
