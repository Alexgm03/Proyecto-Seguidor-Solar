# Proyecto: Seguidor Solar de 2 Grados de Libertad

## Descripción

Este proyecto implementa un **seguidor solar de 2 grados de libertad (2 GDL)** capaz de calcular y simular la orientación óptima de un panel solar para mantenerlo **perpendicular a la radiación solar incidente**, maximizando así el aprovechamiento de la energía solar.

A partir de la posición del Sol, definida por los ángulos de **azimut (α)** y **elevación (θ)**, el sistema calcula los ángulos de control **roll** y **pitch**, genera la orientación del panel y verifica matemáticamente que el seguimiento sea correcto mediante el producto punto entre el vector solar y la normal del panel.

---

# Objetivos

- Calcular la posición solar para una fecha y ubicación determinadas.
- Obtener los ángulos solares de **azimut** y **elevación**.
- Calcular los ángulos de control **roll** y **pitch** de un seguidor solar de 2 GDL.
- Simular el movimiento del panel solar en un entorno tridimensional.
- Graficar la trayectoria del Sol y del panel.
- Verificar que el panel permanezca perpendicular a la radiación solar incidente.

---

# Características

El programa permite:

- Seleccionar fecha de inicio de la simulación.
- Configurar la duración de la simulación en días.
- Configurar latitud, longitud y zona horaria.
- Calcular automáticamente la posición solar utilizando **Pysolar**.
- Calcular los ángulos de control **Roll** y **Pitch**.
- Mostrar una simulación interactiva en 3D.
- Visualizar la trayectoria del Sol y del panel.
- Graficar Elevación/Pitch y Azimut/Roll.
- Controlar la reproducción mediante slider y reproducción automática.
- Verificar el seguimiento mediante el ángulo entre el vector solar y la normal del panel.

---

# Desarrollo Matemático

El proyecto incluye la deducción completa de las ecuaciones utilizadas para el cálculo de los ángulos de control.

El documento contiene:

- Sistema de coordenadas Este–Norte–Cenit.
- Construcción del vector solar.
- Matrices de rotación.
- Obtención de la normal del panel.
- Deducción de las ecuaciones de **Roll** y **Pitch**.
- Verificación mediante producto punto.

📄 **Consultar:** `DESARROLLO_MATEMATICO.md`

---

# Tecnologías utilizadas

- Python 3
- NumPy
- Matplotlib
- Tkinter
- Pysolar

---

# Estructura del proyecto

```text
Proyecto/
│
├── gui.py
├── main.py
├── requirements.txt
├── README.md
├── DESARROLLO_MATEMATICO.md
│
└── src/
    ├── control.py
    ├── graficos.py
    ├── Solar.py
    └── animation.py
```

---

# Funcionamiento

El flujo del programa es el siguiente:

```text
Posición Solar
        │
        ▼
Azimut y Elevación
        │
        ▼
Vector Solar
        │
        ▼
Roll y Pitch
        │
        ▼
Vector Normal del Panel
        │
        ▼
Simulación 3D
        │
        ▼
Verificación (Producto Punto)
```

---

# Ejecución

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la interfaz gráfica:

```bash
python gui.py
```

También es posible ejecutar únicamente la simulación con Matplotlib:

```bash
python main.py
```

---

# Evidencias del proyecto

El proyecto incluye:

- Desarrollo matemático.
- Informe final.
- Presentación.
- Video demostrativo (30 segundos).
- Código fuente.

---

# Integrantes

- Danny Caiza
- Alexander Mena
- Melanie Peñafiel
- Eduardo Verdezoto