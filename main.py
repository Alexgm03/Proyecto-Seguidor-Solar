from datetime import datetime, timedelta
from pytz import timezone
from src.simulacion import ControlSimulacion

from src.Control import calcularAngulosControl, solarVector
from src.Solar import getSolarPosition
from src.graficos import Simulador3D


def iniciar_simulacion(
        fecha_base,
        duracion_horas,
        callback=None,
        frame=None,
        control=None):

    # Crear el simulador 3D dentro del Frame de Tkinter
    simulador = Simulador3D(frame)

    zona = timezone("America/Guayaquil")

    inicio = datetime.combine(
        fecha_base,
        datetime.min.time()
    ).replace(hour=6)

    inicio = zona.localize(inicio)

    trayectoria = []

    pasos = duracion_horas * 4

    if control is None:

        control = ControlSimulacion()

    for paso in range(pasos):

        if not control.esperar():

            break

        tiempo = inicio + timedelta(minutes=15 * paso)

        azimuth, elevation = getSolarPosition(
            date=tiempo
        )

        vector = solarVector(
            azimuth,
            elevation
        )

        roll, pitch = calcularAngulosControl(
            vector
        )

        if elevation >= 0:
            trayectoria.append(vector)

        simulador.actualizar(
            azimuth,
            elevation,
            vector,
            roll,
            pitch,
            trayectoria
        )

        if callback:

            callback(
                azimuth,
                elevation,
                roll,
                pitch,
                tiempo.strftime("%H:%M")
            )

    simulador.finalizar()