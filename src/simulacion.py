import threading
import time


class ControlSimulacion:

    def __init__(self):

        self.pausado = False
        self.detenido = False
        self.velocidad = 1

        self.lock = threading.Lock()

    ##################################################

    def pausar(self):

        with self.lock:

            self.pausado = True

    ##################################################

    def continuar(self):

        with self.lock:

            self.pausado = False

    ##################################################

    def detener(self):

        with self.lock:

            self.detenido = True

    ##################################################

    def reiniciar(self):

        with self.lock:

            self.detenido = False
            self.pausado = False

    ##################################################

    def cambiarVelocidad(self, velocidad):

        with self.lock:

            self.velocidad = velocidad

    ##################################################

    def esperar(self):

        while self.pausado and not self.detenido:

            time.sleep(0.1)

        if self.detenido:

            return False

        time.sleep(0.05 / self.velocidad)

        return True