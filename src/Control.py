# src/control.py
import numpy as np


def solarVector(azimuth, elevation):
    """Convierte el azimut y la elevación en un vector tridimensional unitario."""
    azimuth_rad = np.radians(azimuth)
    elevation_rad = np.radians(elevation)

    x = np.cos(elevation_rad) * np.sin(azimuth_rad)
    y = np.cos(elevation_rad) * np.cos(azimuth_rad)
    z = np.sin(elevation_rad)

    return np.array([x, y, z])


def calcularAngulosControl(vector_solar):
    """Calcula los ángulos de control Pitch y Roll (en grados) para el seguidor

    de la EPN a partir del vector solar unitario.
    """
    x, y, z = vector_solar

    # Evitamos desbordamientos matemáticos limitando el rango a [-1, 1]
    y_clipped = np.clip(y, -1.0, 1.0)

    # Ecuaciones deducidas para la cinemática Roll-Pitch de la EPN
    pitch_rad = -np.arcsin(y_clipped)
    roll_rad = np.arctan2(x, z)

    return np.degrees(roll_rad), np.degrees(pitch_rad)