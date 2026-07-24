import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import generar_frames, LAT_DEFECTO, LON_DEFECTO, TZ_DEFECTO
from src.graficos import (
    inicializarGraficas,
    actualizarEscena3D,
    graficarSeries2D,
    moverMarcador2D,
)

# ---- paleta (misma familia de colores que la versión standalone) ----
BG = "#070b14"
PANEL = "#0f1626"
PANEL2 = "#141d33"
LINE = "#26314a"
TEXT = "#e7ecf7"
TEXT_DIM = "#8b96b3"
SUN = "#f2a93b"
PANEL_BLUE = "#5b9dd6"
OK = "#5fd3a3"

VELOCIDADES = {
    "Muy lenta": 800,
    "Lenta": 400,
    "Normal": 150,
    "Rápida": 40,
    "Muy rápida": 1
}


class VentanaPrincipal:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Seguidor Solar de 2 GDL - EPN")
        self.root.geometry("1560x980")
        self.root.minsize(1240, 820)
        self.root.configure(bg=BG)

        # Estado de la reproducción / navegación de cuadros
        self.frames = []
        self.trayectoria = []
        self.trayectoria_panel = []
        self.indice_frame = 0
        self.reproduciendo = False
        self._despues_id = None

        # ===========================
        # Variables
        # ===========================
        self.fecha = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.dias = tk.IntVar(value=1)
        self.lat = tk.StringVar(value=str(LAT_DEFECTO))
        self.lon = tk.StringVar(value=str(LON_DEFECTO))
        self.tz = tk.StringVar(value=str(TZ_DEFECTO))

        self.azimut = tk.StringVar(value="—")
        self.elevacion = tk.StringVar(value="—")
        self.pitch = tk.StringVar(value="—")
        self.roll = tk.StringVar(value="—")
        self.verificacion = tk.StringVar(value="—")
        self.estado = tk.StringVar(value="Configura los parámetros y presiona “Calcular trayectoria”.")
        self.tiempo_actual = tk.StringVar(value="—")
        self.velocidad = tk.StringVar(value="Normal")

        self._construir_estilo()
        self._crear_interfaz()

    # ------------------------------------------------------------------
    def _construir_estilo(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=PANEL)
        style.configure("TLabel", background=PANEL, foreground=TEXT_DIM, font=("Segoe UI", 9))
        style.configure("Header.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 11))
        style.configure("TEntry", fieldbackground="#0a1120", foreground=TEXT)
        style.configure("TSpinbox", fieldbackground="#0a1120", foreground=TEXT, arrowsize=12)
        style.configure("Accent.TButton", background=SUN, foreground="#1a1002",
                         font=("Segoe UI Semibold", 10), padding=8)
        style.map("Accent.TButton", background=[("active", "#ffbd5a")])
        style.configure("Ghost.TButton", background=PANEL2, foreground=TEXT, padding=6)
        style.configure("Danger.TButton", background="#c0392b", foreground="white", padding=8)
        style.configure("Horizontal.TScale", background=PANEL, troughcolor=LINE)

    # ------------------------------------------------------------------
    def _crear_interfaz(self):

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(header, text="Simulador de seguidor solar de 2 GDL", bg=BG, fg=TEXT,
                 font=("Segoe UI Semibold", 19)).pack(anchor="w")
        tk.Label(header, text="pitch (eje este) y roll (eje norte), calculados a partir de la posición solar real (pysolar).",
                 bg=BG, fg=TEXT_DIM, font=("Segoe UI", 10)).pack(anchor="w")

        cuerpo = tk.Frame(self.root, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=18, pady=8)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # =================================
        # PANEL IZQUIERDO (control + lectura)
        # =================================
        izquierda = tk.Frame(cuerpo, bg=BG, width=300)
        izquierda.grid(row=0, column=0, sticky="ns", padx=(0, 16))

        config = ttk.Frame(izquierda, style="TFrame", padding=14)
        config.pack(fill="x")
        ttk.Label(config, text="CONFIGURACIÓN", style="Header.TLabel").pack(anchor="w", pady=(0, 6))

        self._campo(config, "LATITUD", self.lat)
        self._campo(config, "LONGITUD", self.lon)
        self._campo(config, "HUSO HORARIO (UTC offset, h)", self.tz)
        self._campo(config, "FECHA DE INICIO (AAAA-MM-DD)", self.fecha)

        tk.Label(config, text="DURACIÓN (DÍAS)", bg=PANEL, fg=TEXT_DIM, font=("Consolas", 8)).pack(anchor="w", pady=(8, 2))
        ttk.Spinbox(config, from_=1, to=30, textvariable=self.dias, width=10).pack(anchor="w")

        ttk.Button(config, text="▶  Calcular trayectoria", style="Accent.TButton",
                   command=self.ejecutar).pack(fill="x", pady=(14, 6))
        ttk.Button(config, text="Salir", style="Danger.TButton",
                   command=self.root.destroy).pack(fill="x")

        lectura = ttk.Frame(izquierda, style="TFrame", padding=14)
        lectura.pack(fill="x", pady=(16, 0))
        ttk.Label(lectura, text="LECTURA EN VIVO", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")

        self._tarjetas = {}
        specs = [("elevacion", "Elevación θ", self.elevacion, SUN),
                 ("azimut", "Azimuth α", self.azimut, SUN),
                 ("pitch", "Pitch", self.pitch, PANEL_BLUE),
                 ("roll", "Roll", self.roll, PANEL_BLUE)]
        for i, (clave, etiqueta, var, color) in enumerate(specs):
            fila, col = 1 + i // 2, i % 2
            tarjeta = tk.Frame(lectura, bg="#0a1120", highlightbackground=LINE, highlightthickness=1)
            tarjeta.grid(row=fila, column=col, sticky="nsew", padx=3, pady=3)
            tk.Label(tarjeta, text=etiqueta.upper(), bg="#0a1120", fg=TEXT_DIM, font=("Consolas", 8)).pack(anchor="w", padx=8, pady=(6, 0))
            tk.Label(tarjeta, textvariable=var, bg="#0a1120", fg=color, font=("Segoe UI Semibold", 16)).pack(anchor="w", padx=8, pady=(0, 6))
        lectura.columnconfigure(0, weight=1)
        lectura.columnconfigure(1, weight=1)

        tarjeta_v = tk.Frame(lectura, bg="#0a1120", highlightbackground=LINE, highlightthickness=1)
        tarjeta_v.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=3, pady=(6, 3))
        tk.Label(tarjeta_v, text="VERIFICACIÓN ⊥  (producto punto S·n)", bg="#0a1120", fg=TEXT_DIM,
                 font=("Consolas", 8)).pack(anchor="w", padx=8, pady=(6, 0))
        tk.Label(tarjeta_v, textvariable=self.verificacion, bg="#0a1120", fg=OK,
                 font=("Segoe UI Semibold", 16)).pack(anchor="w", padx=8, pady=(0, 6))

        estado_fila = tk.Frame(lectura, bg=PANEL)
        estado_fila.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self._punto_estado = tk.Canvas(estado_fila, width=10, height=10, bg=PANEL, highlightthickness=0)
        self._punto_estado.pack(side="left")
        self._punto_estado.create_oval(1, 1, 9, 9, fill=OK, outline="")
        tk.Label(estado_fila, textvariable=self.estado, bg=PANEL, fg=TEXT_DIM,
                 font=("Consolas", 9), wraplength=230, justify="left").pack(side="left", padx=6)

        transporte = ttk.Frame(izquierda, style="TFrame", padding=14)
        transporte.pack(fill="x", pady=(16, 0))
        fila_t = tk.Frame(transporte, bg=PANEL)
        fila_t.pack(fill="x")
        self.boton_play = ttk.Button(fila_t, text="▶", width=3, style="Ghost.TButton", command=self._alternar_reproduccion)
        self.boton_play.pack(side="left")
        self.slider = ttk.Scale(fila_t, from_=0, to=0, orient="horizontal", command=self._al_mover_slider)
        self.slider.pack(side="left", fill="x", expand=True, padx=8)
        tk.Label(
            transporte,
            text="Velocidad de reproducción",
            bg=PANEL,
            fg=TEXT_DIM,
            font=("Consolas",8)
        ).pack(anchor="w", pady=(10,2))

        self.combo_velocidad = ttk.Combobox(
            transporte,
            textvariable=self.velocidad,
            values=list(VELOCIDADES.keys()),
            state="readonly",
            width=18
        )

        self.combo_velocidad.pack(fill="x")
        self.combo_velocidad.bind(
            "<<ComboboxSelected>>",
            self._cambiar_velocidad
    )
        self.slider.state(["disabled"])
        tk.Label(transporte, textvariable=self.tiempo_actual, bg=PANEL, fg=TEXT_DIM,
                 font=("Consolas", 9)).pack(anchor="center", pady=(6, 0))

        # =================================
        # PANEL DERECHO (gráfica combinada 3D + 2D)
        # =================================
        derecha = tk.Frame(cuerpo, bg=BG)
        derecha.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax3d, self.ax_a, self.ax_b = inicializarGraficas()
        self.canvas = FigureCanvasTkAgg(self.fig, master=derecha)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()

    def _campo(self, padre, etiqueta, var):
        tk.Label(padre, text=etiqueta, bg=PANEL, fg=TEXT_DIM, font=("Consolas", 8)).pack(anchor="w", pady=(8, 2))
        ttk.Entry(padre, textvariable=var).pack(fill="x")

    # ------------------------------------------------------------------
    # CÁLCULO (hilo secundario) Y REPRODUCCIÓN (hilo principal)
    # ------------------------------------------------------------------
    def ejecutar(self):

        self._detener_reproduccion()

        try:
            fecha = datetime.strptime(self.fecha.get().strip(), "%Y-%m-%d").date()
            lat = float(self.lat.get())
            lon = float(self.lon.get())
            tz = float(self.tz.get())
            dias = max(1, min(30, int(self.dias.get())))
        except ValueError:
            messagebox.showerror("Datos inválidos",
                                  "Revisa latitud, longitud, huso horario, fecha (AAAA-MM-DD) y duración.")
            return

        self.estado.set("Calculando posición solar...")

        hilo = threading.Thread(target=self._calcular_frames, args=(fecha, dias, lat, lon, tz))
        hilo.daemon = True
        hilo.start()

    def _calcular_frames(self, fecha, dias, lat, lon, tz):
        # Cálculo puro (pysolar + trigonometría), sin tocar matplotlib/Tk:
        # seguro de ejecutar en un hilo secundario.
        frames = generar_frames(fecha, dias, lat, lon, tz)
        self.root.after(0, lambda: self._preparar_reproduccion(frames))

    def _preparar_reproduccion(self, frames):

        self.frames = frames
        self.trayectoria = []
        self.trayectoria_panel = []
        self.indice_frame = 0

        if not self.frames:
            messagebox.showinfo("Sin datos", "No se generaron cuadros para simular.")
            return

        # Series completas de una sola vez en los gráficos 2D
        self.linea_a, self.linea_b = graficarSeries2D(self.ax_a, self.ax_b, self.frames)

        self.slider.state(["!disabled"])
        self.slider.configure(from_=0, to=len(self.frames) - 1)
        self.slider.set(0)

        self.estado.set(f"{len(self.frames)} cuadros listos — usa el slider o ▶.")
        self._dibujar_frame(0, avanzar_trayectoria=True)

    def _dibujar_frame(self, idx, avanzar_trayectoria=False):

        if not self.frames:
            return

        frame = self.frames[idx]

        if avanzar_trayectoria:
            frames_hasta_aqui = self.frames[: idx + 1]
            self.trayectoria = [f["vector_sol"] for f in frames_hasta_aqui if f["elevation"] >= 0]
            self.trayectoria_panel = [f["vector_panel"] for f in frames_hasta_aqui if f["elevation"] >= 0]

        actualizarEscena3D(
            self.ax3d,
            frame["azimuth"],
            frame["elevation"],
            frame["vector_sol"],
            frame["vector_panel"],
            frame["roll"],
            frame["pitch"],
            self.trayectoria,
            self.trayectoria_panel,
            frame["angulo_verificacion"],
            forzar_refresco=False,
        )
        moverMarcador2D(self.linea_a, self.linea_b, frame["tiempo"])
        self.canvas.draw_idle()

        self.azimut.set(f"{frame['azimuth']:.1f}°")
        self.elevacion.set(f"{frame['elevation']:.1f}°")
        self.pitch.set(f"{frame['pitch']:.1f}°")
        self.roll.set(f"{frame['roll']:.1f}°")
        if frame["elevation"] >= 0:
            self.verificacion.set(f"{frame['angulo_verificacion']:.3f}°  (≈0° = ⊥ perfecta)")
        else:
            self.verificacion.set("— (sin seguimiento, sol oculto)")
        self.tiempo_actual.set(frame["tiempo"].strftime("%Y-%m-%d  %H:%M") + " (hora local)")
        self.estado.set("Rastreando el sol" if frame["elevation"] >= 0 else "Parqueado — sol bajo el horizonte")

        color = OK if frame["elevation"] >= 0 else "#5a5f70"
        self._punto_estado.delete("all")
        self._punto_estado.create_oval(1, 1, 9, 9, fill=color, outline="")

    # ------------------------------------------------------------------
    # SLIDER Y REPRODUCCIÓN AUTOMÁTICA
    # ------------------------------------------------------------------
    def _al_mover_slider(self, valor):
        # ttk.Scale dispara este "command" tanto si el usuario arrastra el
        # slider como si el código llama a slider.set(...) (como hace
        # _paso_reproduccion en cada cuadro). Sin esta bandera, cada cuadro
        # de la reproducción se autodetenía a sí mismo.
        if getattr(self, "_moviendo_slider_programaticamente", False):
            return
        self._detener_reproduccion()
        self.indice_frame = int(float(valor))
        self._dibujar_frame(self.indice_frame, avanzar_trayectoria=True)

    def _alternar_reproduccion(self):
        if not self.frames:
            return
        if self.reproduciendo:
            self._detener_reproduccion()
        else:
            self.reproduciendo = True
            self.boton_play.configure(text="⏸")
            self._paso_reproduccion()

    def _cambiar_velocidad(self, event=None):

        # Si la animación está detenida, no hacemos nada.
        if not self.reproduciendo:
            return

        # Cancelar el temporizador actual
        if self._despues_id is not None:
            self.root.after_cancel(self._despues_id)

        # Programar nuevamente usando la nueva velocidad
        espera = VELOCIDADES[self.velocidad.get()]

        self._despues_id = self.root.after(
            espera,
            self._paso_reproduccion
        )            

    def _paso_reproduccion(self):
        if not self.reproduciendo:
            return
        self.indice_frame = (self.indice_frame + 1) % len(self.frames)

        self._moviendo_slider_programaticamente = True
        self.slider.set(self.indice_frame)
        self._moviendo_slider_programaticamente = False

        self._dibujar_frame(self.indice_frame, avanzar_trayectoria=True)
        espera = VELOCIDADES[self.velocidad.get()]

        self._despues_id = self.root.after(
            espera,
        self._paso_reproduccion
    )

    def _detener_reproduccion(self):
        self.reproduciendo = False
        self.boton_play.configure(text="▶")
        if self._despues_id is not None:
            self.root.after_cancel(self._despues_id)
            self._despues_id = None

    # ------------------------------------------------------------------
    def iniciar(self):
        self.root.mainloop()


if __name__ == "__main__":

    app = VentanaPrincipal()
    app.iniciar()
