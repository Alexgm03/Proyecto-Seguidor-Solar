import tkinter as tk

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

class Simulador3D:

    def __init__(self, frame):

        self.frame = frame

                # Eliminar cualquier gráfica anterior
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.fig = Figure(figsize=(8,6), dpi=100)

        self.fig = Figure(
            figsize=(8,6),
            dpi=100
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.inicializar()

    def inicializar(self):

        self.ax.clear()

        self.ax.set_xlim([-1.2,1.2])

        self.ax.set_ylim([-1.2,1.2])

        self.ax.set_zlim([0,1.2])

        self.ax.set_xlabel("X")

        self.ax.set_ylabel("Y")

        self.ax.set_zlabel("Z")

        self.ax.set_title(
            "Seguidor Solar"
        )

        self.ax.plot(
            [-1,1],
            [0,0],
            [0,0],
            color="gray",
            linestyle="--"
        )

        self.ax.plot(
            [0,0],
            [-1,1],
            [0,0],
            color="gray",
            linestyle="--"
        )

        self.canvas.draw()

    def generarPanel(
        self,
        vector,
        tam=0.35
    ):

        if np.allclose(
            vector[:2],
            0
        ):

            u = np.array(
                [1,0,0]
            )

        else:

            u = np.array(
                [
                    -vector[1],
                    vector[0],
                    0
                ]
            )

            u = u / np.linalg.norm(u)

        v = np.cross(
            vector,
            u
        )

        r = np.linspace(
            -tam,
            tam,
            5
        )

        U,V = np.meshgrid(
            r,
            r
        )

        X = U*u[0] + V*v[0]

        Y = U*u[1] + V*v[1]

        if abs(vector[2]) > 1e-5:

            Z = -(
                vector[0]*X
                +
                vector[1]*Y
            ) / vector[2]

        else:

            Z = U*u[2] + V*v[2]

        return X,Y,Z

    def actualizar(
        self,
        azimuth,
        elevation,
        vector,
        roll,
        pitch,
        trayectoria
    ):

        self.ax.clear()

        # ----------------------------
        # Configuración de ejes
        # ----------------------------

        self.ax.set_xlim([-1.2,1.2])
        self.ax.set_ylim([-1.2,1.2])
        self.ax.set_zlim([0,1.2])

        self.ax.set_xlabel("Este (X)")
        self.ax.set_ylabel("Norte (Y)")
        self.ax.set_zlabel("Zenit (Z)")

        self.ax.plot(
            [-1,1],
            [0,0],
            [0,0],
            color="gray",
            linestyle="--",
            alpha=0.4
        )

        self.ax.plot(
            [0,0],
            [-1,1],
            [0,0],
            color="gray",
            linestyle="--",
            alpha=0.4
        )

        # ----------------------------
        # Trayectoria solar
        # ----------------------------

        if len(trayectoria) > 0:

            puntos = np.array(trayectoria)

            self.ax.plot(
                puntos[:,0],
                puntos[:,1],
                puntos[:,2],
                color="gold",
                linewidth=2,
                linestyle=":",
                label="Trayectoria"
            )

        # ----------------------------
        # Si el Sol está visible
        # ----------------------------

        if elevation >= 0:

            # Vector del Sol

            self.ax.quiver(
                0,
                0,
                0,
                vector[0],
                vector[1],
                vector[2],
                color="orange",
                linewidth=3,
                length=1
            )

            # Sol

            self.ax.scatter(
                vector[0],
                vector[1],
                vector[2],
                s=180,
                color="yellow",
                edgecolors="orange"
            )

            # Normal del panel

            self.ax.quiver(
                0,
                0,
                0,
                vector[0],
                vector[1],
                vector[2],
                color="blue",
                linewidth=3,
                length=0.8
            )

            # Panel

            X,Y,Z = self.generarPanel(vector)

            self.ax.plot_surface(
                X,
                Y,
                Z,
                color="royalblue",
                alpha=0.6
            )

            self.ax.set_title(

                f"Azimut {azimuth:.2f}°    Elevación {elevation:.2f}°"

            )

        else:

            self.ax.set_title("El Sol está bajo el horizonte")

        # ----------------------------
        # Información
        # ----------------------------

        texto = (
            f"Roll : {roll:.2f}°\n"
            f"Pitch: {pitch:.2f}°"
        )

        self.ax.text2D(
            0.02,
            0.92,
            texto,
            transform=self.ax.transAxes,
            bbox=dict(
                facecolor="white",
                alpha=0.8
            )
        )

        self.ax.legend(
            loc="lower left"
        )

        self.canvas.draw_idle()

    def finalizar(self):

        self.canvas.draw()