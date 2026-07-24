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


def vectorPanel(roll_deg, pitch_deg):
    """Calcula el vector normal unitario del panel (x=Este, y=Norte, z=Cenit)

    a partir de los ángulos de control roll (giro sobre el eje Norte) y
    pitch (giro sobre el eje Este). Cuando el seguimiento es perfecto,
    este vector coincide con el vector solar.
    """
    roll_rad = np.radians(roll_deg)
    pitch_rad = np.radians(pitch_deg)

    x = np.sin(roll_rad) * np.cos(pitch_rad)
    y = -np.sin(pitch_rad)
    z = np.cos(roll_rad) * np.cos(pitch_rad)

    return np.array([x, y, z])


def anguloEntre(v1, v2):
    """Ángulo (en grados) entre dos vectores usando el producto punto.

    Sirve para VERIFICAR que el panel quede perpendicular a la luz solar
    incidente: si ``v1`` es el vector solar y ``v2`` la normal del panel,
    un seguimiento perfecto da como resultado 0°, ya que ambos vectores
    unitarios quedan alineados (producto punto = 1).
    """
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-9 or n2 < 1e-9:
        return float("nan")
    cos_phi = np.dot(v1, v2) / (n1 * n2)
    cos_phi = np.clip(cos_phi, -1.0, 1.0)
    return np.degrees(np.arccos(cos_phi))