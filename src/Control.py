import numpy as np


def solarVector(azimuth, elevation):
    """
    Convierte los ángulos de azimut y elevación
    en un vector tridimensional unitario.

    Parámetros:
        azimuth: ángulo horizontal en grados.
        elevation: altura del Sol en grados.

    Retorna:
        Vector [x, y, z].
    """

    azimuth_rad = np.radians(azimuth)
    elevation_rad = np.radians(elevation)

    x = np.cos(elevation_rad) * np.sin(azimuth_rad)

    y = np.cos(elevation_rad) * np.cos(azimuth_rad)

    z = np.sin(elevation_rad)

    return np.array([x, y, z])