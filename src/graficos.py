# src/graficos.py
import matplotlib.pyplot as plt
import numpy as np


def inicializarGrafica3D():
    """Configura la ventana tridimensional con sus límites y ejes cardinales."""
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([0, 1.2])

    ax.set_xlabel("Oeste <--- ESTE (X) ---> Este")
    ax.set_ylabel("Sur <--- NORTE (Y) ---> Norte")
    ax.set_zlabel("CENIT (Z)")
    ax.set_title("Simulación de Seguimiento Solar 3D - EPN")

    # Líneas de referencia para simular el suelo plano
    ax.plot([-1, 1], [0, 0], [0, 0], color="gray", linestyle="--", alpha=0.4)
    ax.plot([0, 0], [-1, 1], [0, 0], color="gray", linestyle="--", alpha=0.4)

    return fig, ax


def generarMallaPanel(v_panel, tamano=0.35):
    """Genera una malla de puntos cuadrada orientada perpendicularmente al vector dado."""
    # Buscamos un vector ortogonal en el plano horizontal
    if np.allclose(v_panel[:2], 0):
        u = np.array([1, 0, 0])
    else:
        u = np.array([-v_panel[1], v_panel[0], 0])
        u = u / np.linalg.norm(u)

    # El segundo vector ortogonal mutuo
    v = np.cross(v_panel, u)

    # Grilla local del panel
    r = np.linspace(-tamano, tamano, 5)
    U, V = np.meshgrid(r, r)

    # Conversión al espacio global 3D
    X_p = U * u[0] + V * v[0]
    Y_p = U * u[1] + V * v[1]

    if abs(v_panel[2]) > 1e-5:
        Z_p = -(v_panel[0] * X_p + v_panel[1] * Y_p) / v_panel[2]
    else:
        Z_p = U * u[2] + V * v[2]

    return X_p, Y_p, Z_p


def actualizarEscena3D(
    ax, azimuth, elevation, vector_sol, roll, pitch, trayectoria_puntos=None
):
    """Limpia la ventana y redibuja todos los componentes interactivos."""
    ax.cla()

    # Volver a establecer límites fijos del plano tras el borrado
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([0, 1.2])
    ax.set_xlabel("Oeste <--- ESTE (X) ---> Este")
    ax.set_ylabel("Sur <--- NORTE (Y) ---> Norte")
    ax.set_zlabel("CENIT (Z)")

    ax.plot([-1, 1], [0, 0], [0, 0], color="gray", linestyle="--", alpha=0.4)
    ax.plot([0, 0], [-1, 1], [0, 0], color="gray", linestyle="--", alpha=0.4)

    # 1. Graficar la trayectoria recorrida acumulada (puntos amarillos tenues)
    if trayectoria_puntos is not None and len(trayectoria_puntos) > 0:
        pts = np.array(trayectoria_puntos)
        ax.plot(
            pts[:, 0],
            pts[:, 1],
            pts[:, 2],
            color="gold",
            linestyle=":",
            alpha=0.7,
            label="Trayectoria Solar",
        )

    # 2. Dibujar Vector del Sol (Flecha Naranja) si el sol está sobre el horizonte
    if elevation >= 0:
        ax.quiver(
            0,
            0,
            0,
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="darkorange",
            length=1.0,
            label="Vector Solar ($\vec{v}_{sol}$)",
            linewidth=2,
        )
        # Dibujar el Sol (Esfera)
        ax.scatter(
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="gold",
            s=180,
            edgecolors="orange",
        )

        # 3. Dibujar Vector Normal del Panel (Flecha Azul)
        ax.quiver(
            0,
            0,
            0,
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="blue",
            length=0.7,
            label="Normal del Panel ($\vec{n}_{panel}$)",
            linewidth=2,
        )

        # 4. Dibujar superficie del Panel Solar
        X_p, Y_p, Z_p = generarMallaPanel(vector_sol)
        ax.plot_surface(X_p, Y_p, Z_p, color="royalblue", alpha=0.6, shade=True)
        ax.set_title(
            f"Simulación Interactiva Solar\nAz: {azimuth:.1f}° | El: {elevation:.1f}°"
        )
    else:
        ax.set_title("Simulación Interactiva Solar\n[ El Sol está oculto (Noche) ]")

    # Desplegar los valores numéricos de control requeridos por la rúbrica
    info_panel = f"Ángulos de Control:\n• Roll (Giro Norte): {roll:.2f}°\n• Pitch (Giro Este): {pitch:.2f}°"
    ax.text2D(
        0.02,
        0.92,
        info_panel,
        transform=ax.transAxes,
        fontsize=9.5,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    ax.legend(loc="lower left")
    plt.pause(0.05)  # Breve pausa para forzar el refresco de la animación interactiva