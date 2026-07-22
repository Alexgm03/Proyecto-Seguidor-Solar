import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
from src.simulacion import ControlSimulacion

from main import iniciar_simulacion


class App:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("☀ Seguidor Solar de 2 GDL - EPN")

        self.root.geometry("1400x850")

        self.root.configure(bg="#ECECEC")

        self.root.minsize(1200,700)

        self.crearVariables()

        self.crearMenu()

        self.crearInterfaz()

        self.root.mainloop()

    #####################################################################

    def crearVariables(self):

        self.fecha = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )

        self.duracion = tk.IntVar(
            value=12
        )

        self.velocidad = tk.IntVar(
            value=1
        )

        self.control = ControlSimulacion()

        self.azimut = tk.StringVar(value="0.00°")
        self.elevacion = tk.StringVar(value="0.00°")
        self.roll = tk.StringVar(value="0.00°")
        self.pitch = tk.StringVar(value="0.00°")
        self.hora = tk.StringVar(value="06:00")
        self.estado = tk.StringVar(value="Esperando")

    #####################################################################

    def crearMenu(self):

        barra = tk.Menu(self.root)

        archivo = tk.Menu(barra, tearoff=0)

        archivo.add_command(
            label="Salir",
            command=self.root.destroy
        )

        barra.add_cascade(
            label="Archivo",
            menu=archivo
        )

        ayuda = tk.Menu(barra, tearoff=0)

        ayuda.add_command(
            label="Acerca de..."
        )

        barra.add_cascade(
            label="Ayuda",
            menu=ayuda
        )

        self.root.config(menu=barra)

    #####################################################################

    def crearInterfaz(self):

        izquierda = tk.Frame(
            self.root,
            width=300,
            bg="#F8F8F8",
            relief="ridge",
            bd=2
        )

        izquierda.pack(
            side="left",
            fill="y"
        )

        derecha = tk.Frame(
            self.root,
            bg="white"
        )

        derecha.pack(
            side="right",
            fill="both",
            expand=True
        )

        ###############################################################

        titulo = tk.Label(

            izquierda,

            text="CONFIGURACIÓN",

            font=("Arial",16,"bold"),

            bg="#F8F8F8"

        )

        titulo.pack(pady=15)

        ###############################################################

        tk.Label(
            izquierda,
            text="Fecha",
            bg="#F8F8F8"
        ).pack()

        tk.Entry(
            izquierda,
            textvariable=self.fecha,
            width=25
        ).pack(pady=5)

        ###############################################################

        tk.Label(
            izquierda,
            text="Duración",
            bg="#F8F8F8"
        ).pack()

        ttk.Spinbox(

            izquierda,

            from_=1,

            to=24,

            textvariable=self.duracion,

            width=20

        ).pack(pady=5)

        ###############################################################

        tk.Label(
            izquierda,
            text="Velocidad",
            bg="#F8F8F8"
        ).pack()

        ttk.Combobox(

            izquierda,

            values=["1","2","5","10"],

            textvariable=self.velocidad,

            width=17

        ).pack(pady=5)

        ###############################################################

        tk.Button(

            izquierda,

            text="▶ Iniciar",

            command=self.iniciar,

            bg="#2ECC71",

            fg="white",

            font=("Arial",11,"bold")

        ).pack(fill="x",padx=20,pady=8)

        tk.Button(

            izquierda,

            text="⏸ Pausar",

            command=self.pausar,

            bg="#F1C40F"

        ).pack(fill="x",padx=20,pady=5)

        tk.Button(

            izquierda,

            text="⏹ Detener",

            command=self.detener,

            bg="#E74C3C",

            fg="white"

        ).pack(fill="x",padx=20,pady=5)

        tk.Button(

            izquierda,

            text="🔄 Reiniciar",

            command=self.reiniciar,

        ).pack(fill="x",padx=20,pady=5)

        ###############################################################

        ttk.Separator(
            izquierda
        ).pack(fill="x",pady=20)

        tk.Label(

            izquierda,

            text="DATOS",

            font=("Arial",14,"bold"),

            bg="#F8F8F8"

        ).pack()

        self.crearDato(
            izquierda,
            "Azimut",
            self.azimut
        )

        self.crearDato(
            izquierda,
            "Elevación",
            self.elevacion
        )

        self.crearDato(
            izquierda,
            "Pitch",
            self.pitch
        )

        self.crearDato(
            izquierda,
            "Roll",
            self.roll
        )

        self.crearDato(
            izquierda,
            "Hora",
            self.hora
        )

        self.crearDato(
            izquierda,
            "Estado",
            self.estado
        )

        ###############################################################

        self.frameGrafica = tk.Frame(

            derecha,

            bg="white"

        )

        self.frameGrafica.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )

    #####################################################################

    def crearDato(self,padre,texto,var):

        frame = tk.Frame(
            padre,
            bg="#F8F8F8"
        )

        frame.pack(fill="x",padx=15,pady=4)

        tk.Label(

            frame,

            text=texto,

            width=12,

            anchor="w",

            bg="#F8F8F8",

            font=("Arial",10,"bold")

        ).pack(side="left")

        tk.Label(

            frame,

            textvariable=var,

            bg="#F8F8F8",

            fg="blue"

        ).pack(side="right")

    #####################################################################

    def actualizarDatos(

        self,

        az,

        el,

        roll,

        pitch,

        hora

    ):

        self.root.after(

            0,

            lambda: self.azimut.set(f"{az:.2f}°")

        )

        self.root.after(

            0,

            lambda: self.elevacion.set(f"{el:.2f}°")

        )

        self.root.after(

            0,

            lambda: self.roll.set(f"{roll:.2f}°")

        )

        self.root.after(

            0,

            lambda: self.pitch.set(f"{pitch:.2f}°")

        )

        self.root.after(

            0,

            lambda: self.hora.set(hora)

        )

    #####################################################################

    def iniciar(self):

        self.estado.set("Simulando")

        fecha = datetime.strptime(
            self.fecha.get(),
            "%Y-%m-%d"
        ).date()

        hilo = threading.Thread(

            target=iniciar_simulacion,

            args=(

                fecha,

                self.duracion.get(),

                self.actualizarDatos,

                self.frameGrafica,

                self.control

            )

        )

        hilo.daemon = True

        hilo.start()

            ####################################################

    def pausar(self):

        self.control.pausar()

        self.estado.set("Pausado")

    ####################################################

    def detener(self):

        self.control.detener()

        self.estado.set("Detenido")

    ####################################################

    def reiniciar(self):

        self.control.reiniciar()

        self.estado.set("Esperando")


if __name__ == "__main__":

    App()


