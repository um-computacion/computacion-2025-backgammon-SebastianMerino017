Este documento registra la secuencia de prompts utilizados para generar, refinar y estructurar las pruebas unitarias, de integración y de aceptación del proyecto Backgammon. El objetivo es asegurar la robustez de la lógica del juego y mantener una trazabilidad completa del proceso de Quality Assurance (QA).

1. Pruebas Unitarias (Core)

El objetivo de esta fase es aislar y probar cada componente (.py) de la lógica core de forma independiente.

test_checker.py

    Prompt Inicial: "Empecemos por lo más simple. Genera el archivo test_checker.py usando unittest. Necesito probar la clase Checker.

        Test 1: Probar el constructor (__init__) por defecto. Verificar que get_color() funciona, get_position() es None y is_captured() es False.

        Test 2: Probar el constructor con una posición inicial (ej. Checker("white", 5)).

        Test 3: Probar el método set_position().

        Test 4: Probar el método capture(). Verificar que is_captured() devuelva True y get_position() devuelva None.

        Test 5: Probar el método release(pos). Empezar con una ficha capturada, llamar a release(10) y verificar que is_captured() devuelva False y get_position() devuelva 10."

test_dice.py (Prueba de la función get_dice)

    Prompt Inicial: "Necesito probar la función get_dice() en dice.py. Esta función depende de random.randint, así que no es determinista. Debo usar unittest.mock.patch sobre random.randint para simular sus resultados."

    Prompt de Casos: "Genera la clase TestDice(unittest.TestCase):

        Test 1 (test_simple): Simular una tirada normal. Usa @patch('random.randint', side_effect=[5, 2]). Verifica que la tupla devuelta por get_dice() sea (5, 2).

        Test 2 (test_double o test_complex): Simular una tirada de dobles. Usa @patch('random.randint', side_effect=[4, 4]). Verifica que la tupla devuelta sea (4, 4, 4, 4).

        Test 3 (test_error): Simular un fallo en random.randint. Usa @patch('random.randint', side_effect=Exception("error!!")). Verifica que get_dice() maneje la excepción y devuelva una tupla vacía ()."

    Refinamiento: "Añadir más casos de prueba a test_dice.py para asegurar que patch funciona correctamente en diferentes contextos, como usarlo con with."

test_dice_class.py (Prueba de la clase Dice)

    Prompt Inicial: "Ahora, necesito un unittest para la clase Dice. Esta clase importa y usa la función get_dice() que ya probamos. Por lo tanto, en lugar de mockear random.randint, debo mockear la función get_dice."

    Prompt de Casos: "Genera test_dice_class.py:

        Test 1 (test_roll_and_values): Mockear core.dice.get_dice para que return_value sea (3, 4).

            Crear d = Dice() y llamar a d.roll().

            Verificar que d.get_values() sea [3, 4].

            Verificar que d.get_available_values() sea [3, 4].

            Verificar que d.is_double() sea False.

            Verificar que d.has_available_values() sea True.

        Test 2 (test_double_roll_and_use): Mockear get_dice con return_value=(2, 2, 2, 2).

            Llamar a d.roll().

            Verificar que d.is_double() sea True.

            Verificar que d.get_available_values() devuelva [2, 2, 2, 2].

            Llamar a d.use_value(2).

            Verificar que d.get_available_values() ahora devuelva [2, 2, 2] (solo quitó uno).

        Test 3 (test_use_value_invalid): En una tirada de (3, 4), probar que d.use_value(5) (un valor no disponible) devuelva False.

        Test 4 (test_str_variants): Probar el método __str__ en diferentes estados (sin tirar, tirada normal, tirada doble)."

test_player.py

    Prompt Inicial (CRÍTICO): "Genera test_player.py. La clase Player usa atributos de clase (estáticos) como current_turn y game_pieces. Esto es un gran problema para las pruebas unitarias, porque el estado de un test se "filtrará" al siguiente.

        Solución: Debo usar setUp y tearDown en mi unittest.TestCase.

        En setUp, debo llamar a Player.reset_game() antes de cada test.

        En tearDown, debo llamar a Player.reset_game() después de cada test.

        Esto garantiza que cada test comience con un estado limpio (current_turn = 'white', contadores en 0, etc.)."

    Prompt de Casos (con setUp/tearDown):

        test_initial_state: Crear p1 y p2. Verificar que p1.color es 'white', p2.color es 'black', y Player.current_turn es 'white'.

        test_turns: Verificar que p1.is_my_turn() es True y p2.is_my_turn() es False.

        test_switch_turn: Llamar a Player.switch_turn(). Ahora verificar que p1.is_my_turn() sea False y p2.is_my_turn() sea True.

        test_roll_dice_invalid_turn: (Basado en el método roll_dice de player.py). Verificar que p2.roll_dice() (cuando no es su turno) devuelva None.

        test_bear_off_piece: Probar p1.bear_off_piece(). Verificar que Player.game_pieces['white']['on_board'] sea 14 y ['off_board'] sea 1.

test_board.py

    Prompt Inicial: "Este es el test unitario más complejo. Necesito probar board.py a fondo. Genera test_board.py."

    Prompt de Casos (Estado Inicial):

        test_initial_setup: Verificar que las 15 fichas blancas y 15 negras estén en sus posiciones iniciales correctas. Ser muy específico: self.assertEqual(board.__pos__[0], ["white", 2]), self.assertEqual(board.__pos__[11], ["white", 5]), self.assertEqual(board.__pos__[23], ["black", 2]), etc.

        Verificar que __bar__ y __off_board__ estén en 0.

    Prompt de Casos (Movimiento):

        test_move_piece_simple: Probar un movimiento legal simple de 'white', sin captura (ej. de 11 a 15). Verificar que __pos__[11] reduce su contador y __pos__[15] lo incrementa.

        test_move_piece_capture_blot: Configurar un 'blot' (una ficha enemiga sola). Ej: Poner board.__pos__[5] en ['black', 1]. Ejecutar un movimiento blanco (ej. de 0 a 5).

            Verificar que board.__pos__[5] ahora sea ['white', 1].

            Verificar que board.__bar__['black'] haya incrementado a 1.

        test_is_target_valid_enemy_block: Probar que is_target_valid (y por extensión is_valid_move) devuelva False si el destino está bloqueado (ej. mover a __pos__[5] que tiene ['black', 2]).

        test_invalid_direction_white: Probar que is_valid_move para 'white' devuelva False si to_point <= from_point.

        test_invalid_direction_black: Probar que is_valid_move para 'black' devuelva False si to_point >= from_point.

    Prompt de Casos (Barra):

        test_enter_from_bar_valid: Manipular el tablero: board.__bar__['white'] = 1. Probar board.enter_from_bar(20, 'white'). Verificar que __bar__['white'] baje a 0 y __pos__[20] sea ['white', 1].

        test_enter_from_bar_blocked: Poner board.__bar__['white'] = 1 y board.__pos__[20] = ['black', 2]. Probar que board.enter_from_bar(20, 'white') devuelva False.

        test_enter_from_bar_invalid_zone: Poner board.__bar__['white'] = 1. Probar que board.enter_from_bar(5, 'white') (un punto fuera del home del oponente) devuelva False.

    Prompt de Casos ('Bear Off'):

        test_can_bear_off_false: En el tablero inicial, verificar que board.can_bear_off('white') devuelva False.

        test_can_bear_off_true: Crear un estado de tablero ficticio donde todas las 15 fichas de 'white' estén en su 'home board' (puntos 18-23). Verificar que can_bear_off('white') devuelva True.

        test_bear_off_invalid_state: Probar que board.bear_off(20, 'white') falle si can_bear_off es False.

        test_bear_off_valid: Con can_bear_off en True, probar un bear_off(20, 'white') válido. Verificar que el contador board.__off_board__['white'] incremente.

2. Pruebas de Integración (test_game.py)

El objetivo es probar que los componentes core (Board, Player, Dice) funcionan correctamente juntos, orquestados por la clase Game.

    Prompt Inicial: "Crear el unittest de integración para la clase Game. Este test no debe mockear Board o Player. Sí puede mockear Dice para forzar escenarios."

    Prompt de Estado: "Al igual que test_player.py, la clase Game depende del estado estático de Player. Por lo tanto, test_game.py debe usar setUp y tearDown para llamar a Player.reset_game()."

    Prompt de Casos (Flujo de Turno):

        test_initialization: Verificar que Game() cree las instancias p1, p2, board y dice.

        test_start_game: Llamar a game.start() y verificar que __game_started__ sea True.

        test_roll_dice_flow: Llamar a game.start(). Verificar que game.roll_dice() funcione (devuelva una tupla) y que __dice_rolled__ sea True.

        test_roll_dice_twice_raises_error: Llamar a game.roll_dice(). Inmediatamente después, verificar que self.assertRaises(InvalidMoveError, game.roll_dice).

        test_move_piece_before_roll_raises_error: Llamar a game.start(). Verificar que self.assertRaises(InvalidMoveError, game.move_piece, 0, 3).

        test_end_turn_before_roll_raises_error: Verificar que self.assertRaises(InvalidMoveError, game.end_turn).

    Prompt de Casos (Lógica de Movimiento):

        test_move_piece_valid: Mockear los dados. Hacer que game.roll_dice() sea seguido por game.__dice__ = ... (o mockear game.get_dice()) para que tenga un valor (ej. [3]). Probar un game.move_piece(0, 3) válido. Verificar que el dado fue 'usado' (ej. game.get_dice().has_available_values() es False).

        test_move_piece_invalid_dice_value: Mockear dados para que sean [3]. Probar self.assertRaises(InvalidMoveError, game.move_piece, 0, 5).

        test_move_piece_while_in_bar_raises_error: Poner una ficha en la barra del jugador actual (game.get_board().__bar__['white'] = 1). Mockear dados (ej. [3, 4]). Verificar que self.assertRaises(InvalidMoveError, game.move_piece, 0, 3). El juego debe forzar a usar enter_from_bar.

        test_end_turn_with_unused_dice_raises_error: Simular una tirada (ej. (3, 4)) pero no usar los dados. Verificar self.assertRaises(InvalidMoveError, game.end_turn).

        test_full_turn_flow: Simular un turno completo: roll_dice(), move_piece(), move_piece(), end_turn(). Verificar que game.get_current_player() ahora sea p2.

    Prompt de Casos (Fin de Juego):

        test_game_over_condition: Manipular el game.get_board() para que __off_board__['white'] sea 15. Verificar que game.is_game_over() devuelva True y game.get_winner() devuelva al jugador 1 (p1).

3. Pruebas de Interfaz (Aceptación) (test_cli.py)

El objetivo es probar que la interfaz (cli.py) reacciona correctamente a la entrada del usuario y maneja las excepciones de la lógica del juego sin "crashear".

    Prompt Inicial (CRÍTICO): "Generar test_cli.py. Esta es una prueba de aceptación y NO debe depender de la lógica real del juego. La capa de presentación (CLI) debe estar desacoplada de la capa de negocio (Game).

        Solución: Debo usar MagicMock(spec=Game) para mockear toda la clase Game. La cli interactuará con este 'doble' del juego.

        Debo usar patch('builtins.input') con side_effect para simular la entrada del teclado del usuario.

        Debo usar patch('builtins.print') para capturar la salida de la consola y verificar que se le está mostrando la información correcta al usuario."

    Prompt de Casos (Comandos del Usuario):

        test_handle_dice_roll_success:

            Mockear cli.__game__.roll_dice.return_value = (3, 4).

            Simular el comando 'r' llamando a cli.handle_dice_roll().

            Verificar que mock_print fue llamado con algo como "Jugador 1 tiro: (3, 4)".

        test_handle_move_success:

            Simular input con side_effect=['5', '8'] (para "Desde:" y "Hasta:").

            Llamar a cli.handle_move().

            Verificar que cli.__game__.move_piece fue llamado exactamente con (5, 8).

            Verificar que mock_print fue llamado con "Movimiento exitoso".

        test_handle_move_error_gracefully (¡El más importante!):

            Mockear cli.__game__.move_piece.side_effect = InvalidMoveError("Movimiento bloqueado").

            Simular input side_effect=['5', '9'].

            Llamar a cli.handle_move().

            Verificar que la CLI no crashee.

            Verificar que mock_print fue llamado con el mensaje de error: "Error: Movimiento bloqueado".

        test_handle_other_errors: Repetir el test anterior para NotYourTurnError y NoPiecesInBarError.

        test_main_menu_quit: Simular input side_effect=['q'] para verificar que el bucle main_menu termina correctamente."

    Refinamiento: "Asegurar que los mocks de cli.py también cubran los handlers de handle_enter_from_bar y handle_bear_off, verificando que los inputs numéricos se parsean a int antes de pasarlos al game mockeado."