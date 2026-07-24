from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pytz import FixedOffset

from src.Control import calcularAngulosControl, solarVector, vectorPanel, anguloEntre
from src.Solar import getSolarPosition
from src.graficos import (
    inicializarGraficas,
    actualizarEscena3D,
    graficarSeries2D,
    moverMarcador2D,
)

# Valores por defecto: Campus EPN, huso horario de Ecuador continental (UTC-5)
LAT_DEFECTO = -0.2105367
LON_DEFECTO = -78.491614
TZ_DEFECTO = -5


def generar_frames(
    fecha_base,
    dias=1,
    lat=LAT_DEFECTO,
    lon=LON_DEFECTO,
    tz_horas=TZ_DEFECTO,
    paso_min=10,
):
    """Calcula todos los cuadros de la simulación (sin dibujar nada).

    Al no llamar a matplotlib, esta función es segura para ejecutarse
    en un hilo secundario (como hace ``gui.py``); el dibujo se hace
    siempre desde el hilo principal.

    ``dias`` permite simular varios días consecutivos (antes solo se
    podían pedir horas dentro de un mismo día).
    """

    zona = FixedOffset(int(tz_horas * 60))

    inicio = zona.localize(
        datetime.combine(fecha_base, datetime.min.time())
    )

    pasos_por_dia = int(1440 / paso_min)

    frames = []

    for dia in range(dias):

        inicio_dia = inicio + timedelta(days=dia)

        for paso in range(pasos_por_dia):

            tiempo_actual = inicio_dia + timedelta(
                minutes=paso_min * paso
            )

            azimuth, elevation = getSolarPosition(
                latitude=lat,
                longitude=lon,
                date=tiempo_actual,
            )

            vector_sol = solarVector(
                azimuth,
                elevation
            )

            roll, pitch = calcularAngulosControl(
                vector_sol
            )

            vector_panel = vectorPanel(roll, pitch)
            angulo_verificacion = anguloEntre(vector_sol, vector_panel) if elevation >= 0 else float("nan")

            frames.append(dict(
                tiempo=tiempo_actual,
                azimuth=azimuth,
                elevation=elevation,
                vector_sol=vector_sol,
                vector_panel=vector_panel,
                roll=roll,
                pitch=pitch,
                angulo_verificacion=angulo_verificacion,
            ))

    return frames


def iniciar_simulacion(
    fecha_base,
    dias=1,
    lat=LAT_DEFECTO,
    lon=LON_DEFECTO,
    tz_horas=TZ_DEFECTO,
    callback=None,
):
    """
    Ejecuta la simulación en modo standalone (abre su propia ventana con
    la figura combinada: domo 3D + gráficas 2D de elevación/pitch y
    azimuth/roll). Para uso embebido en la GUI de Tkinter, usar
    ``generar_frames`` en su lugar (ver gui.py).

    callback recibe: azimuth, elevation, roll, pitch
    """

    plt.ion()

    fig, ax3d, ax_a, ax_b = inicializarGraficas()

    frames = generar_frames(fecha_base, dias, lat, lon, tz_horas)

    if not frames:
        return

    linea_a, linea_b = graficarSeries2D(ax_a, ax_b, frames)

    trayectoria = []
    trayectoria_panel = []

    for frame in frames:

        if frame["elevation"] >= 0:
            trayectoria.append(frame["vector_sol"])
            trayectoria_panel.append(frame["vector_panel"])

        actualizarEscena3D(
            ax3d,
            frame["azimuth"],
            frame["elevation"],
            frame["vector_sol"],
            frame["vector_panel"],
            frame["roll"],
            frame["pitch"],
            trayectoria,
            trayectoria_panel,
            frame["angulo_verificacion"],
            forzar_refresco=False,
        )
        moverMarcador2D(linea_a, linea_b, frame["tiempo"])

        fig.canvas.draw_idle()
        plt.pause(0.03)

        if callback is not None:

            callback(
                frame["azimuth"],
                frame["elevation"],
                frame["roll"],
                frame["pitch"],
            )

    plt.ioff()
    plt.show()


if __name__ == "__main__":

    iniciar_simulacion(
        datetime.now().date(),
        dias=1,
    )