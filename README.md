# Reloj Interactivo 

Este proyecto es una aplicación interactiva desarrollada en Python que muestra la hora en formato analógico (con manecillas) y digital. El reloj se sincroniza automáticamente con la hora del sistema, pero también permite ajustar manualmente la hora al arrastrar sus manecillas. Al soltar la manecilla, el reloj continúa avanzando a partir del "tiempo manual" establecido, y pulsando la tecla **R** se reinicia a la hora actual del sistema.

---

## Contenido del Proyecto

El proyecto se compone de dos módulos principales:

- **clock_list.py**  
  Implementa una lista circular doble para almacenar y recorrer los números que se muestran en la carátula del reloj (por ejemplo: 12, 1, 2, …, 11).  
  - **Node:** Clase que representa cada elemento con atributos `data`, `next` y `prev`.
  - **CircularDoublyLinkedList:** Clase que administra la lista. Métodos clave:
    - `insert(data)`: Agrega un nodo y mantiene la circularidad.
    - `traverse()`: Recorre la lista de forma cíclica y devuelve los datos en orden.

- **interactive_clock.py**  
  Es la aplicación principal, usando Pygame para crear la ventana gráfica, dibujar la cara del reloj, sus manecillas y la hora digital, y gestionar la interactividad.  
  - Configura parámetros gráficos (dimensiones, centro y radio).
  - Declara variables globales que gestionan el estado del reloj (por ejemplo, ángulos de manecilla, modo manual, etc.).
  - Implementa funciones auxiliares para:
    - Convertir coordenadas polares a cartesianas.
    - Calcular la distancia mínima entre un punto y una línea (para detectar clics cerca de las manecillas).
    - Dibujar la cara del reloj (círculo, ticks y números) y las manecillas.
    - Convertir los ángulos a un tiempo digital y dibujar ese tiempo.
    - Actualizar los ángulos en función de la hora del sistema o en modo manual.
  - Incorpora un bucle principal que actualiza y redibuja todo en tiempo real, procesando eventos del mouse y del teclado.

---

## Requisitos Previos

- **Python 3.10** o superior *(se puede verificar en la consola con `python --version`)*.
- **Git** (Para clonar el repositorio).
- **Pygame**: Librería externa que se instala a través de pip para la parte gráfica e interactividad.

> **Nota:** Se recomienda utilizar un entorno virtual para aislar las dependencias de este proyecto. La carpeta del entorno virtual (comúnmente llamada `env`) no se incluye en el repositorio.

---

## Instrucciones Paso a Paso para Configurar y Ejecutar el Proyecto

1. **Clonar el Repositorio**

   Abre una terminal y ejecuta:
   ```bash
    git init https://github.com/CamiloToroUCC/taller-Listas-Circulares-Dobles-.git
   ```


 2. **Instalar dependencias**:
 ```bash
python -m pip install pygame

 ```
 
 3. **Opcion de dependencias**:
 ```bash
py -m pip install pygame
 ```
 
 4. **Ejecutar el proyecto: Una vez instalada la dependencia, ejecuta el archivo principal:**:
 ```bash
 python interactiveClock.py
 ```
