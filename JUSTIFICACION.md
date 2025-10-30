# JUSTIFICACION.md - Proyecto Backgammon

## 1. Resumen del Diseño General

El proyecto está diseñado siguiendo una arquitectura de separación de capas (Separation of Concerns). El objetivo principal fue aislar completamente la lógica de negocio del juego de cualquier interfaz de usuario.

Esto se logró creando un paquete `core` que contiene toda la lógica y las reglas del Backgammon. Las interfaces de usuario, `cli.py` (Interfaz de Línea de Comandos) y `pygame_ui.py` (Interfaz Gráfica), actúan como "clientes" de este paquete `core`.

* **Paquete `core`**: Es el cerebro del proyecto. No sabe si los datos se están mostrando en una consola o en una ventana gráfica. Contiene las clases `Game`, `Board`, `Player` y `Dice`.
* **Capas de Presentación (`cli.py`, `pygame_ui.py`)**: Estas capas importan `core.game` para funcionar. Se encargan de:
    1.  Recibir la entrada del usuario (clics del ratón o comandos de texto).
    2.  Llamar a los métodos correspondientes del objeto `Game` (ej. `game.move_piece()`, `game.roll_dice()`).
    3.  Recibir el estado actualizado del juego desde `core` y "dibujarlo" en la pantalla o consola.

Esta separación es una implementación directa del principio SOLID de Inversión de Dependencias (D), donde las capas de alto nivel (UI) dependen de las abstracciones de bajo nivel (lógica `core`), y no al revés.



