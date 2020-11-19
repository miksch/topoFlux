import numpy as np
import pandas as pd

def rotate_2d(x0, y0, theta):
    """
    Rotate point or vector by theta (+ anticlockwise)
    
    Args:
        x0 (float) : x-component of wind vector (u) [m/s]
        y0 (float) : y-component of wind vector (v) [m/s]
        theta (float) : angle of rotation (+ anticlockwise) [deg]
        
    Returns:
        x1 (float) : rotated x-component of wind vector
        y1 (float) : rotated y-component of wind vector
    """
    
    cos_theta = np.cos(np.radians(theta))
    sin_theta = np.sin(np.radians(theta))
    
    x1 = x0 * cos_theta - y0 * sin_theta
    y1 = x0 * sin_theta + y0 * cos_theta
    
    return x1, y1



def double_rotate(df, u, v, w):
    """
    Perform double rotation method on wind components

    Follows https://www.licor.com/env/support/EddyPro/topics/anemometer-tilt-correction.html#Doublerotationmethod
    """

    # Rotation 1
    rot1_mean = df.mean()

    theta = np.arctan(rot1_mean[v] / rot1_mean[u])
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    u_temp = rot1_mean[u] * cos_theta + rot1_mean[v] * sin_theta
    v_temp = -1 * rot1_mean[u] * sin_theta + rot1_mean[v] * cos_theta
    
    # Rotation 2
    phi = np.arctan(rot1_mean[w] / utmp)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    #df[f"{u}_rot"] = u_temp * cos_phi

    # Store rotations in original dataframe along with theta and phi (also returned in function)


    return df, theta, phi
    

def pd_double_rotate(df, u, v, w, time_freq):

    #Split data into groups dictated by time_freq
    df_grouped = df.groupby(pd.Grouper(freq=time_freq))


