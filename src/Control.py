import numpy as np


def solarVector(azimuth, elevation):
    """
    Convierte elevación y azimuth
    a un vector cartesiano.
    """

    az = np.radians(azimuth)
    el = np.radians(elevation)

    x = np.cos(el) * np.sin(az)
    y = np.cos(el) * np.cos(az)
    z = np.sin(el)

    return np.array([x, y, z])


def calculateAngles(azimuth, elevation):
    """
    Esta función será reemplazada
    por el desarrollo matemático.

    Retorna:
        roll
        pitch
    """

    roll = azimuth
    pitch = 90 - elevation

    return roll, pitch