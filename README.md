# 🎲 Proyecto Backgammon – Computación 2025

Este proyecto implementa el clásico juego **Backgammon** en Python, desarrollado como parte del trabajo final de la materia **Computación 2025**.
El sistema cuenta con una arquitectura modular, pruebas unitarias y dos interfaces de usuario: una **CLI** (consola) y otra **gráfica con Pygame**.

---

## 🧠 Objetivo

El propósito del proyecto es aplicar los principios de **Programación Orientada a Objetos** y las buenas prácticas de ingeniería de software, desarrollando un sistema jugable, testeable y extensible.

---

## 🧩 Estructura del Proyecto

```
├── core/                # Lógica principal del juego
│   ├── board.py         # Representa el tablero y las posiciones
│   ├── checker.py       # Define las fichas y su color
│   ├── dice.py          # Simula los dados
│   ├── game.py          # Controla la lógica general del juego
│   └── player.py        # Maneja los jugadores y sus turnos
│
├── cli/                 # Interfaz de consola
│   └── cli.py
│
├── pygame_ui/           # Interfaz gráfica con Pygame
│   └── pygame_ui.py
│
├── tests/               # Pruebas unitarias
│   ├── test_board.py
│   ├── test_checker.py
│   ├── test_cli.py
│   ├── test_dice.py
│   ├── test_game.py
│   └── test_player.py
│
├── assets/diagramas/    # Diagramas y recursos gráficos
│   └── diagrama_clases.png
│
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

---

## 🧮 Principios de Diseño Aplicados

* **Encapsulamiento:** cada clase gestiona sus propios datos y comportamiento.
* **Abstracción:** el jugador o interfaz no manipula directamente el tablero ni los dados.
* **Composición:** `Game` contiene instancias de `Board`, `Dice` y `Player`.
* **Responsabilidad Única:** cada módulo tiene una función bien definida.

---

## 🕹️ Ejecución del Juego

### ▶️ Interfaz de Consola (CLI)

```bash
python3 cli/cli.py
```

### 🖥️ Interfaz Gráfica (Pygame)

```bash
python3 pygame_ui/pygame_ui.py
```

> Asegúrate de estar en la carpeta raíz del proyecto al ejecutar los comandos.

---

## 🧪 Pruebas Unitarias

El proyecto incluye un conjunto completo de **tests automáticos** para validar la lógica del juego y las excepciones personalizadas.

Ejecutar los tests:

```bash
pytest
```

Generar un informe de cobertura:

```bash
coverage run -m pytest
coverage report -m
```

---

## 🧾 Instalación

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd computacion-2025-backgammon
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---


## 🧠 Módulos Principales

| Módulo       | Descripción                                                               |
| ------------ | ------------------------------------------------------------------------- |
| `core/`      | Contiene toda la lógica del juego.                                        |
| `cli/`       | Proporciona una interfaz basada en texto.                                 |
| `pygame_ui/` | Proporciona una interfaz visual interactiva.                              |
| `tests/`     | Contiene las pruebas unitarias que garantizan el correcto funcionamiento. |

---

## 🧑‍💻 Autor

**Sebastián Ignacio Merino Roldan**
