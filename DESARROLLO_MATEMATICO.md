# Desarrollo matemático — Seguidor solar de 2 grados de libertad

Este documento deduce las ecuaciones que usa `src/Control.py` para calcular
los ángulos de control **pitch** y **roll** a partir de la posición solar
(elevación `θ` y azimuth `α`), tal como lo pide el objetivo del proyecto.

## 1. Sistema de coordenadas

Se trabaja en un sistema local **Este–Norte–Cenit** (E, N, U), con origen en
el punto donde está instalado el seguidor:

* Eje **E** (x): apunta al Este.
* Eje **N** (y): apunta al Norte.
* Eje **U** (z): apunta al Cenit (vertical, hacia arriba).

## 2. Vector unitario hacia el sol

Con `θ` (elevación, medida desde la superficie hacia el sol) y `α`
(azimuth, medido desde el norte), el vector unitario que apunta al sol es:

```
S = ( sin(α)·cos(θ),   cos(α)·cos(θ),   sin(θ) )
      \_____E_____/    \_____N_____/    \_U_/
```

Esto se deduce proyectando el vector solar: su componente vertical es
`sin(θ)` y su proyección horizontal tiene magnitud `cos(θ)`, la cual se
reparte entre Este y Norte según el ángulo `α` medido desde el norte.

## 3. Orientación del panel: de (pitch, roll) a la normal del panel

Los ángulos de control de la EPN son, según el enunciado:

* **roll**: giro alrededor del eje que mira al **norte**.
* **pitch**: giro alrededor del eje que mira al **este** (en vez de yaw,
  como aclara el `[IMPORTANTE]` del enunciado).

La normal del panel parte del cenit `(0, 0, 1)` (panel mirando hacia
arriba, en reposo) y se orienta aplicando primero un giro **pitch**
alrededor del eje Este y luego un giro **roll** alrededor del eje Norte:

```
n = Ry(roll) · Rx(pitch) · (0, 0, 1)ᵀ
```

donde las matrices de rotación son:

```
Rx(pitch) =  1        0            0
             0    cos(pitch)  -sin(pitch)
             0    sin(pitch)   cos(pitch)

Ry(roll)  =  cos(roll)   0   sin(roll)
                 0       1       0
            -sin(roll)   0   cos(roll)
```

Multiplicando:

```
Rx(pitch)·(0,0,1)ᵀ = ( 0,  -sin(pitch),  cos(pitch) )

Ry(roll)·( 0, -sin(pitch), cos(pitch) )ᵀ =
    ( sin(roll)·cos(pitch),  -sin(pitch),  cos(roll)·cos(pitch) )
```

Por lo tanto:

```
n = ( sin(roll)·cos(pitch),   -sin(pitch),   cos(roll)·cos(pitch) )
```

(esto es exactamente lo que implementa `Control.vectorPanel(roll, pitch)`).

## 4. Igualar n = S y despejar pitch, roll

Para que el panel quede perpendicular a la luz solar incidente, su normal
debe coincidir con el vector solar: `n = S`. Igualando componente a
componente:

```
Este:   sin(roll)·cos(pitch) = sin(α)·cos(θ)      (i)
Norte:  -sin(pitch)          = cos(α)·cos(θ)      (ii)
Cenit:  cos(roll)·cos(pitch) = sin(θ)              (iii)
```

**De (ii)** se despeja `pitch` directamente, sin depender de `roll`:

```
pitch = -arcsin( cos(α)·cos(θ) )
```

**Dividiendo (i) entre (iii)** se elimina `cos(pitch)` y se obtiene `roll`
sin ambigüedad de cuadrante (usando `atan2`):

```
roll = atan2( sin(α)·cos(θ),  sin(θ) )
```

Estas son las dos ecuaciones que implementa
`Control.calcularAngulosControl(vector_solar)`.

## 5. Caso especial: sol bajo el horizonte

Si `θ < 0` el sol está bajo el horizonte y no hay a qué apuntar: el
programa "parquea" el panel (no se calculan pitch/roll con la fórmula
anterior; se omite el seguimiento hasta que el sol vuelva a salir).

## 6. Verificación de perpendicularidad (producto punto)

Para comprobar numéricamente que el panel efectivamente queda
perpendicular a la luz solar, se calcula el ángulo entre el vector solar
`S` y la normal del panel `n` mediante el producto punto:

```
cos(φ) = (S · n) / (|S| |n|)
```

Como ambos son vectores unitarios, `S · n = 1` (es decir, `φ = 0°`)
cuando el seguimiento es perfecto. Esta verificación está implementada en
`Control.anguloEntre(v1, v2)` y se muestra en vivo en la GUI como
"Verificación ⊥".

## 7. Resumen de fórmulas implementadas

| Cantidad | Fórmula | Función |
|---|---|---|
| Vector solar | `S = (sin α cos θ, cos α cos θ, sin θ)` | `Control.solarVector` |
| Pitch | `pitch = -asin(cos α cos θ)` | `Control.calcularAngulosControl` |
| Roll | `roll = atan2(sin α cos θ, sin θ)` | `Control.calcularAngulosControl` |
| Normal del panel | `n = (sin(roll)cos(pitch), -sin(pitch), cos(roll)cos(pitch))` | `Control.vectorPanel` |
| Verificación ⊥ | `φ = acos(S · n)` (debe ser ≈ 0°) | `Control.anguloEntre` |
