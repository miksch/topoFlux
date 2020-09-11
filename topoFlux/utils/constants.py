import numpy as np

# General meteorological constants
k = 0.41  # Von Karman's constant
R_d = 287.0  # Gas constant for dry air [J kg^-1 K^-1]
R_v = 461.51  # Gas constant for water vapor [J kg^-1 K^-1]
eps = 0.622  # R_d/R_v []
c_pd = 1004.67  # Specific heat capacity of dry air at constant pressure [J kg^-1 K^-1]
g = 9.80665  # Standard Gravity (3rd CGPM) [m s^-2]
R_g = 8.3144598  # Universal gas constant [J mol^-1 K^-1]

# Heat flux constants
c_dry = 840.  # specific heat capacity (bulk value) of dry soil components [J kg^-1 K^-1]
c_wet = 4181.3  # specific heat capacity of water [J kg^-1 K^-1]
rho_w = 1000.  # bulk density of water [kg m^-3]

# Approximation for C_p and l_v terms
l_v_const = 1.45  # Latent heat of vaporization at 20°C
c_p_const = 1.013e-3  # Specific heat of air at constant pressure [MJ kg^-1 °C^-1]

# Coefficients used in calculating saturation vapor pressure (met_utils)
gs = np.array((-2.8365744e3,
              -6.028076559e3,
              1.954263612e1,
              -2.737830188e-2,
              1.6261698e-5,
              7.0229056e-10,
              -1.8680009e-13,
              2.7150305)).reshape((1,1,8))