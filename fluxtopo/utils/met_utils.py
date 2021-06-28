import numpy as np
from utils import constants as c


# Moisture

def specific_humidity(e, P):
    """
    Calculates specific humidity based on vapor pressure and ambient air pressure.
    Peixoto & Oort 1996; Ross & Elliott 1996

    Args:
        e (float) : Vapor pressure [Pa]
        P (float) : Ambient air pressure [Pa]

    Returns:
        q (np.ndarray) : Specific humidity [g/g]
    """

    q = (c.eps * e) / (P - (1 - c.eps) * e)

    return np.asarray(q)


def actual_vp_q(q, P):
    """
    Calculates actual vapor pressure given specific humidity.

    Args:
        q (float) : Specific humidity [g/g]
        P (float) : Ambient air pressure(s) [Pa]

    Returns
        e (np.ndarray) : Actual vapor pressure [Pa]
    """

    e = (P * q) / (c.eps + (1 - c.eps) * q)

    return np.asarray(e)


def es_wexler(T_K, slope=False):
    """
    Calculates saturation vapor pressure over water at each temperature
    based on Wexler 1976, with coefficients from Hardy 1998 (ITS-90).

    Args:
        T_K (np.ndarray (dimension<=2), float, list of floats) : Air or Dewpoint Temperatures [K]

    Returns:
        es : np.ndarray of saturation vapor pressures [Pa]
    """

    powers = np.arange(-2, 5).reshape((1, 1, 7))

    T_K = np.atleast_3d(T_K).astype(dtype=np.float64)
    temps = np.repeat(T_K, 8, axis=-1)

    temps[..., :-1] = c.gs[..., :-1] * np.power(temps[..., :-1], powers)
    temps[..., -1] = c.gs[..., -1] * np.log(temps[..., -1])

    es = np.squeeze(np.exp(temps.sum(axis=-1)))

    return es


def s_wexler(T_K):
    """
    Calculates slope of saturation vapor pressure curve over water at each temperature
    based on Wexler 1976, with coefficients from Hardy 1998 (ITS-90).

    Args:
        T_K (np.ndarray (dimension<=2), float, list of floats) : Air or Dewpoint Temperatures [K]

    Returns:
        s : np.ndarray of slopes [Pa / deg C]
    """

    powers = np.arange(-3, 4).reshape((1, 1, 7))
    pow_coeffs = powers.copy() + 1

    T_K = np.atleast_3d(T_K).astype(dtype=np.float64)
    temps = np.repeat(T_K, 8, axis=-1)

    temps[..., :-1] = pow_coeffs * c.gs[..., :-1] * np.power(temps[..., :-1], powers)
    temps[..., -1] = -1. * c.gs[..., -1] * temps[..., -1] ** -1

    s = np.squeeze(temps.sum(axis=-1)) * es_wexler(T_K)

    return s


# Ground heat flux

def gflux_storage(del_temp, del_time, theta_v, rho_b=1300., z=0.08):
    """
    Calculate heat storage between the soil heat flux plate and surface.

    Args:
        del_temp : change in temperature over a given timestep [deg C or K]
        del_time : timestep [s]
        theta_v : volumetric water content []
        rho_b : bulk density of the soil
        z : depth of soil heat flux plates [m]

    Returns:
        s : storage of heat within the soil layer and the surface [w m^-2]

    """

    cs = c.c_dry + theta_v * (rho_b / c.rho_w) * c.c_wet

    s = (rho_b * cs * del_temp * z) / del_time

    return s


def gflux_pd(df, gflux_1='shfp_avg_1', gflux_2='shfp_avg_2', vwc_col='vwc',
             temp_col='tsoil_tcav_avg'):
    """
    Calculate ground heat flux based on values from pandas.DataFrame columns.

    Args:

    Returns:
    """

    delta_time = df.index.to_series().diff().dt.seconds
    delta_temp = df[temp_col].diff()

    storage = gflux_storage(delta_temp, delta_time, df['vwc'])
    gflux_1 = df[gflux_1] + storage
    gflux_2 = df[gflux_2] + storage
    gflux_avg = (gflux_1 + gflux_2) / 2.

    return storage, gflux_1, gflux_2, gflux_avg


def c_p(q):
    """
    Calculate the specific heat of air at constant pressure

    Stull, pg. 640

    Args:
        q (float) : specific humidity [g/g]

    Returns:
        c_p (float) : specific heat of air at constant pressure [J kg^-1 K^-1]

    """

    cp = c.c_pd * (1 + 0.84 * q)

    return cp


def rho_air(ea, P, t_air):
    """
    Calculate density of air.

    Wallace and Hobbs, pg. 67 right before equation 3.15

    Args:
        ea (float) : actual vapor pressure [Pa]
        P (float) : ambient pressure [Pa]
        t_air (float) : air temperature [K]

    Returns:
        rhoa (float) : density of air [kg m^-3]

    """
    rhoa = (P / (c.R_d * t_air)) * (1 - (ea / P) * (1 - c.eps))

    return rhoa


def L_v(t_air):
    """
    Calculate latent heat of vaporization at a given temperature.
    Stull, pg. 641

    Args:
        t_air (float) : Air temperature [deg C]

    Returns:
        lv : Latent heat of vaporization at t_air [J kg^-1]

    """

    lv = (2.501 - 0.00237 * t_air) * 1e6

    return lv


def psychro_const(c_p, P, L_v=2.45e6):
    """
    Calculate the psychrometric constant
    FAO 1998

    Args:

    Returns:

    """

    g = (c_p * P) / (c.eps * L_v)

    return g


def pressure_fao(z=1331):
    """
    Calculate the pressure for a certain elevation if no measurements are available.
    FAO 1998

    Args:

    Returns:
        p (float) : atmospheric pressure [hPa]

    """

    p = 101.3 * ((293 - 0.0065 * z) / 293.) ** 5.26

    return p * 1e1


def potential_temp(t, pres, pres_ref=100000, k=0.286):
    """
    Calculate potential temperature

    Args:
        t (float) : temperature [K]
        pres (float) : pressure [Pa]
        pres_ref (float) : standard pressure [Pa]
        k : R / cp [ ]

    Returns:
        theta : potential temperature [K]

    """

    theta = t * (pres_ref / pres) ** k

    return theta
