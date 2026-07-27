# src/graficos.py
import matplotlib.pyplot as plt
import numpy as np
from pysolar import elevation


def inicializarGrafica3D():
    """Configura la ventana tridimensional con sus límites y ejes cardinales.

    Se mantiene por compatibilidad con código existente que solo necesita
    el eje 3D (por ejemplo, scripts propios de prueba). Para la GUI
    combinada usar ``inicializarGraficas()``.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim([-1.55, 1.55])
    ax.set_ylim([-1.55, 1.55])
    ax.set_zlim([0, 1.55])

    ax.set_xlabel("Oeste <--- ESTE (X) ---> Este")
    ax.set_ylabel("Sur <--- NORTE (Y) ---> Norte")
    ax.set_zlabel("CENIT (Z)")
    ax.set_title("Simulación de Seguimiento Solar 3D - EPN")

    # Líneas de referencia para simular el suelo plano
    ax.plot([-1, 1], [0, 0], [0, 0], color="gray", linestyle="--", alpha=0.4)
    ax.plot([0, 0], [-1, 1], [0, 0], color="gray", linestyle="--", alpha=0.4)

    return fig, ax


# ======================================================================
# FIGURA COMBINADA: domo 3D (grande) + 2 gráficos 2D (elevación/pitch,
# azimuth/roll) -- combina la vista 3D del proyecto original con las
# gráficas de series de tiempo de la versión standalone.
# ======================================================================
BG = "#0f1626"
FG = "#e7ecf7"
GRID = "#26314a"
SUN_C = "#f2a93b"
PANEL_C = "#5b9dd6"


def inicializarGraficas():
    """Crea la figura combinada: eje 3D arriba (más grande) y dos ejes 2D

    abajo (elevación/pitch y azimuth/roll vs. tiempo). Devuelve
    ``(fig, ax3d, ax_a, ax_b)``.
    """
    fig = plt.figure(figsize=(13, 11), facecolor=BG)
    gs = fig.add_gridspec(2, 2, height_ratios=[2.1, 1], hspace=0.32, wspace=0.25,
                           left=0.05, right=0.97, top=0.95, bottom=0.09)

    ax3d = fig.add_subplot(gs[0, :], projection="3d")
    ax_a = fig.add_subplot(gs[1, 0])
    ax_b = fig.add_subplot(gs[1, 1])

    _formatear_ejes_3d(ax3d)
    for ax in (ax_a, ax_b):
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=8)
        ax.grid(color=GRID, linewidth=0.6)
        for spine in ax.spines.values():
            spine.set_color(GRID)

    return fig, ax3d, ax_a, ax_b


def _formatear_ejes_3d(ax):
    ax.set_facecolor(BG)
    ax.set_xlim([-1.55, 1.55])
    ax.set_ylim([-1.55, 1.55])
    ax.set_zlim([0, 1.55])
    ax.set_xlabel("Oeste <--- ESTE (X) ---> Este", color=FG, fontsize=9)
    ax.set_ylabel("Sur <--- NORTE (Y) ---> Norte", color=FG, fontsize=9)
    ax.set_zlabel("CENIT (Z)", color=FG, fontsize=9)
    ax.tick_params(colors=FG, labelsize=7)
    ax.set_title("Simulación de Seguimiento Solar 3D - EPN", color=FG, fontsize=12)

    # Los "paneles" de fondo de mplot3d NO se pintan con ax.set_facecolor():
    # por defecto quedan gris claro y le quitan contraste al sol y al panel.
    # Hay que colorearlos explícitamente para que el tema oscuro se note.
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor("#0b1220")
        axis.pane.set_edgecolor(GRID)
        axis.pane.set_alpha(1.0)
        axis.line.set_color(GRID)
        axis._axinfo["grid"]["color"] = (0.16, 0.19, 0.29, 0.6)
        axis._axinfo["grid"]["linewidth"] = 0.5

    ax.view_init(elev=24, azim=-55)

    # Piso de referencia (disco tenue) en vez de solo dos líneas, ayuda a
    # ubicar la altura del sol/panel de un vistazo
    tita = np.linspace(0, 2 * np.pi, 60)
    ax.plot(np.cos(tita), np.sin(tita), np.zeros_like(tita), color=GRID, linewidth=1, alpha=0.8)
    ax.plot([-1.3, 1.3], [0, 0], [0, 0], color=GRID, linestyle="--", alpha=0.5)
    ax.plot([0, 0], [-1.3, 1.3], [0, 0], color=GRID, linestyle="--", alpha=0.5)


def graficarSeries2D(ax_a, ax_b, frames):
    """Dibuja, de una sola vez, las series completas de theta/pitch y

    alpha/roll a lo largo de toda la simulación, y devuelve las líneas
    verticales que marcan el instante actual (para moverlas con
    ``moverMarcador2D`` sin tener que rehacer la gráfica completa).
    """
    tiempos = [f["tiempo"] for f in frames]
    elevaciones = [f["elevation"] for f in frames]
    azimuts = [f["azimuth"] for f in frames]
    pitches = [f["pitch"] for f in frames]
    rolls = [f["roll"] for f in frames]

    for ax in (ax_a, ax_b):
        ax.clear()
        ax.set_facecolor(BG)
        ax.grid(color=GRID, linewidth=0.6)
        ax.tick_params(colors=FG, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(GRID)

    ax_a.plot(tiempos, elevaciones, color=SUN_C, linewidth=1.6, label="Elevación θ")
    ax_a.plot(tiempos, pitches, color=PANEL_C, linewidth=1.6, linestyle="--", label="Pitch")
    ax_a.set_title("Elevación θ / Pitch", color=FG, fontsize=10, loc="left")
    ax_a.legend(fontsize=8, facecolor=BG, labelcolor=FG, edgecolor=GRID)

    ax_b.plot(tiempos, azimuts, color=SUN_C, linewidth=1.6, label="Azimuth α")
    ax_b.plot(tiempos, rolls, color=PANEL_C, linewidth=1.6, linestyle="--", label="Roll")
    ax_b.set_title("Azimuth α / Roll", color=FG, fontsize=10, loc="left")
    ax_b.legend(fontsize=8, facecolor=BG, labelcolor=FG, edgecolor=GRID)

    for ax in (ax_a, ax_b):
        ax.figure.autofmt_xdate()

    linea_a = ax_a.axvline(tiempos[0], color=FG, alpha=0.35, linestyle=":")
    linea_b = ax_b.axvline(tiempos[0], color=FG, alpha=0.35, linestyle=":")
    return linea_a, linea_b


def moverMarcador2D(linea_a, linea_b, tiempo):
    """Mueve la línea vertical de 'instante actual' en ambos gráficos 2D."""
    linea_a.set_xdata([tiempo, tiempo])
    linea_b.set_xdata([tiempo, tiempo])


def generarMallaPanel(
    v_panel,
    tamano=0.45,
    distancia_montaje=0.35,
):
    """Genera una malla cuadrada que representa físicamente la placa del panel,

    orientada perpendicularmente a ``v_panel`` y montada a una distancia
    ``distancia_montaje`` del origen (simulando el poste/soporte del
    seguidor), en lugar de atravesar el origen.
    """
    # Buscamos un vector ortogonal en el plano horizontal
    if np.allclose(v_panel[:2], 0):
        u = np.array([1, 0, 0])
    else:
        u = np.array([-v_panel[1], v_panel[0], 0])
        u = u / np.linalg.norm(u)

    # El segundo vector ortogonal mutuo
    v = np.cross(v_panel, u)
    v = v / np.linalg.norm(v)

    centro = v_panel * distancia_montaje

    # Grilla local del panel
    r = np.linspace(-tamano, tamano, 6)
    U, V = np.meshgrid(r, r)

    # Conversión al espacio global 3D, centrada en el punto de montaje
    X_p = centro[0] + U * u[0] + V * v[0]
    Y_p = centro[1] + U * u[1] + V * v[1]
    Z_p = centro[2] + U * u[2] + V * v[2]

    return X_p, Y_p, Z_p, centro


def actualizarEscena3D(
    ax,
    azimuth,
    elevation,
    vector_sol,
    vector_panel,
    roll,
    pitch,
    trayectoria_puntos=None,
    trayectoria_panel_puntos=None,
    angulo_verificacion=None,
    forzar_refresco=True,
):

    ax.cla()
    _formatear_ejes_3d(ax)


    # ==============================
    # 1. Trayectoria del Sol
    # ==============================

    if trayectoria_puntos is not None and len(trayectoria_puntos) > 0:
        pts = np.array(trayectoria_puntos)

        ax.plot(
            pts[:,0],
            pts[:,1],
            pts[:,2],
            color="gold",
            linestyle=":",
            alpha=0.7,
            label="Trayectoria Solar"
        )


    # ==============================
    # 2. Trayectoria del panel
    # ==============================

    if trayectoria_panel_puntos is not None and len(trayectoria_panel_puntos) > 0:
        pts_p = np.array(trayectoria_panel_puntos)

        ax.plot(
            pts_p[:,0],
            pts_p[:,1],
            pts_p[:,2],
            color="#8fd0ff",
            linestyle="--",
            alpha=0.6,
            linewidth=1.2,
            label="Trayectoria Panel"
        )


    # ==============================
    # 3. Dibujar Sol solamente de día
    # ==============================

    if elevation >= 0:

        ax.quiver(
            0,
            0,
            0,
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="darkorange",
            length=1,
            linewidth=2.2,
            label="Vector Solar"
        )


        ax.scatter(
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="#ffcf6b",
            s=1600,
            alpha=0.18
        )


        ax.scatter(
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="#ffdd7a",
            s=420,
            alpha=0.9
        )


        ax.scatter(
            vector_sol[0],
            vector_sol[1],
            vector_sol[2],
            color="#fff6de",
            s=170
        )


        estado_txt = (
            f"Az: {azimuth:.1f}° | "
            f"El: {elevation:.1f}°"
        )


    else:

        estado_txt = (
            "[ Noche ]\n"
            "Panel en posición de parqueo"
        )


    # ==============================
    # 4. Posición del panel
    # ==============================

    if elevation >= 0:

        panel_actual = vector_panel

    else:

        # posición de seguridad nocturna
        panel_actual = np.array([0,0,1])


    X_p, Y_p, Z_p, centro = generarMallaPanel(
        panel_actual
    )


    # Soporte

    ax.plot(
        [0,centro[0]],
        [0,centro[1]],
        [0,centro[2]],
        color="#9aa3b5",
        linewidth=6
    )


    ax.scatter(
        0,
        0,
        0,
        color="#9aa3b5",
        s=70
    )


    # Superficie del panel

    ax.plot_surface(
        X_p,
        Y_p,
        Z_p,
        color="#2f6fb3",
        alpha=0.92,
        shade=False
    )


    # Bordes del panel

    ax.plot(
        X_p[0,:],
        Y_p[0,:],
        Z_p[0,:],
        color="#eaf4ff",
        linewidth=2
    )

    ax.plot(
        X_p[-1,:],
        Y_p[-1,:],
        Z_p[-1,:],
        color="#eaf4ff",
        linewidth=2
    )

    ax.plot(
        X_p[:,0],
        Y_p[:,0],
        Z_p[:,0],
        color="#eaf4ff",
        linewidth=2
    )

    ax.plot(
        X_p[:,-1],
        Y_p[:,-1],
        Z_p[:,-1],
        color="#eaf4ff",
        linewidth=2
    )


    ax.scatter(
        *centro,
        color="#eaf4ff",
        s=55,
        label="Panel Solar"
    )


    # ==============================
    # Información
    # ==============================

    info_panel = (
        f"{estado_txt}\n\n"
        "Ángulos de Control:\n"
        f"• Roll: {roll:.2f}°\n"
        f"• Pitch: {pitch:.2f}°"
    )


    if angulo_verificacion is not None:

        info_panel += (
            f"\n\nVerificación ⊥:\n"
            f"{angulo_verificacion:.3f}°"
        )


    ax.text2D(
        0.02,
        0.93,
        info_panel,
        transform=ax.transAxes,
        fontsize=10.5,
        color="#1a1002",
        verticalalignment="top",
        bbox=dict(
            facecolor="#f2a93b",
            alpha=0.9,
            edgecolor="none"
        )
    )


    ax.legend(
        loc="lower left",
        fontsize=9,
        facecolor=BG,
        labelcolor=FG,
        edgecolor=GRID
    )


    if forzar_refresco:
        plt.pause(0.05)