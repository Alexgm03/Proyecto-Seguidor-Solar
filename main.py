# main.py
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pytz import timezone
from src.control import calcularAngulosControl, solarVector
from src.graficos import actualizarEscena3D, inicializarGrafica3D
from src.solar import getSolarPosition

print("=============================================")
print("  CONFIGURACIÓN DE LA SIMULACIÓN SOLAR EPN   ")
print("=============================================\n")

# 1. Ingreso de parámetros por el usuario (Requerimiento de la guía)
fecha_str = input(
    "Ingrese la fecha de simulación (AAAA-MM-DD) [Presione Enter para hoy]: "
)
if not fecha_str.strip():
    fecha_base = datetime.now().date()
else:
    fecha_base = datetime.strptime(fecha_str.strip(), "%Y-%m-%d").date()

duracion_horas = input("Ingrese la duración de la simulación en horas [Por defecto 12]: ")
duracion_horas = int(duracion_horas.strip()) if duracion_horas.strip() else 12

# Definir la hora de inicio (por defecto a las 6:00 AM para capturar la salida del sol)
zona_horaria = timezone("America/Guayaquil")
dt_simulacion = datetime.combine(fecha_base, datetime.min.time()).replace(hour=6)
dt_simulacion = zona_horaria.localize(dt_simulacion)

print(f"\nIniciando simulación interactiva para el día: {fecha_base}")
print(f"Intervalo visualizado: desde las 06:00 AM durante {duracion_horas} horas.\n")

# 2. Inicializar componentes gráficos
plt.ion()  # Activar modo interactivo de matplotlib
fig, ax = inicializarGrafica3D()

trayectoria_historica = []
pasos_totales = duracion_horas * 4  # Muestreos cada 15 minutos

# 3. Bucle de ejecución temporal interactiva
for paso in range(pasos_totales):
    # Calcular la estampa de tiempo actual del paso
    tiempo_actual = dt_simulacion + timedelta(minutes=paso * 15)

    # Obtener Azimut y Elevación usando tu función original de solar.py
    azimuth, elevation = getSolarPosition(date=tiempo_actual)

    # Convertir a Vector usando tu función de control.py
    vector_sol = solarVector(azimuth, elevation)

    # Calcular los ángulos cinemáticos Pitch y Roll modificados
    roll, pitch = calcularAngulosControl(vector_sol)

    # Acumular la trayectoria si el sol está sobre el horizonte
    if elevation >= 0:
        trayectoria_historica.append(vector_sol)

    # Refrescar la pantalla 3D de manera interactiva
    actualizarEscena3D(
        ax, azimuth, elevation, vector_sol, roll, pitch, trayectoria_historica
    )

print("Simulación completada con éxito.")
plt.ioff()  # Desactivar modo interactivo
plt.show()  # Dejar la ventana abierta al finalizar