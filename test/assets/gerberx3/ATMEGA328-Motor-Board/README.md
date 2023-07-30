# ATMEGA328-Motor-Board

La placa ATMEGA328-Motor-Board es una tarjeta controladora para motores utilizando un
microcontrolador ATMEGA328 y dos drivers para motores L298P, creada con plataforma Open
Source de diseño EDA [KiCad][1]

## Caracteristicas

- Tensión de alimentación para la circuiteria de control : 5 - 36 (VDC)
- Tensión de alimentación para la potencia de los motores : 7,5 - 46 (VDC)
- Permite controlar hasta 4 motores de corriente continua (max 3 Amperios), 2 motores de
  corriente continua (max 6 Amperios) o dos motores paso a paso (max 6 Amperios).
- Permite controlar hasta 4 servomotores a 5 VDC mediante señales PWM.
- Dispone de dos conectores para encoder incremental bicanal con tensión de alimentación
  configurable 5 o 24 VDC
- Dispone de dos conectores para potenciómetros o señales análogicas de consigna 0 - 5
  VDC.
- Permite monitorizar el consumo de cada uno de los cuatro canales de alimentación de
  motores de forma independiente.
- Dispone de tres entradas digitales 5 o 24 VDC optoacopladas para señales de propósito
  general (Enable, Run, Stop)
- Dispone de dos salidas digitales de tensión de salida configurable para señales de
  propósito general.
- Dispone de puerto Mini-USB para comunicación serie con el controlador de la tarjeta.
- Dispone de tres indicadores LED para la comunicación de diversos estados de los
  drivers o control.

## Imagenes

Cara superior ![Cara superior](/imagenes/cara_superior.png)

Cara inferior ![Cara inferior](/imagenes/cara_inferior.png)

## Lista de materiales

| Refencias | Valor | Total Uds |
| --------- | ----- | --------- |

## Licencia

Este diseño es Software Libre; usted puede redistribuirlo y/o modificarlo bajo los
términos de la "GNU General Public License" como lo publica la "FSF Free Software
Foundation", o (a su elección) de cualquier versión posterior.

Este diseño es distribuido con la esperanza de que le sea útil, pero SIN NINGUNA
GARANTIA; incluso sin la garantía implícita por la VENTA o EJERCICIO DE ALGUN PROPOSITO
en particular. Vea la "GNU General Public License" para más detalles.

[1]: http://kicad-pcb.org/

---

Source: https://github.com/AntonioMR/ATMEGA328-Motor-Board
