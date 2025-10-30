import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game import Game, InvalidMoveError, NotYourTurnError
from core.player import Player 

WIDTH, HEIGHT = 1000, 700
MARGIN_X, MARGIN_Y = 40, 40
BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TEXT = (25, 25, 25)
HIGHLIGHT_COLOR = (255, 255, 100)
MSG_COLOR = (200, 0, 0)

MAX_VISIBLE_STACK = 5


def point_index_to_display(idx):
    if 0 <= idx <= 11:
        return 'top', 11 - idx
    else:
        return 'bottom', idx - 12


def draw_triangle(surface, board_rect, col_vis, row, color):
    x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
    x1 = x0 + (board_rect.width / 12.0)
    x_mid = (x0 + x1) / 2.0
    
    y0 = board_rect.top if row == 'top' else board_rect.bottom
    y1 = board_rect.top + (board_rect.height / 2.0) if row == 'top' else board_rect.bottom - (board_rect.height / 2.0)
    
    points = [(x0, y0), (x1, y0), (x_mid, y1)]
    pygame.draw.polygon(surface, color, points)


def draw_checker(surface, center, radius, color, label, font):
    pygame.draw.circle(surface, (20, 20, 20), center, radius)
    pygame.draw.circle(surface, color, center, radius - 2)
    
    if label:
        text_surf = font.render(label, True, (200, 200, 200) if color == BLACK else (50, 50, 50))
        text_rect = text_surf.get_rect(center=center)
        surface.blit(text_surf, text_rect)


def draw_board_and_pieces(surface, board_state, font, selected_idx=None):
    surface.fill(BG_COLOR)
    
    board_rect = pygame.Rect(
        MARGIN_X, MARGIN_Y,
        WIDTH - 2 * MARGIN_X, HEIGHT - 2 * MARGIN_Y
    )
    pygame.draw.rect(surface, BOARD_COLOR, board_rect)

    bar_width = board_rect.width / 13.0
    bar_rect = pygame.Rect(
        board_rect.left + 6 * (board_rect.width / 12.0) - bar_width / 2.0,
        board_rect.top,
        bar_width,
        board_rect.height
    )
    pygame.draw.rect(surface, LINE, bar_rect, 2)

    hitmap = {i: [] for i in range(24)}
    hitmap['bar_white'] = []
    hitmap['bar_black'] = []
    hitmap['off_white'] = []
    hitmap['off_black'] = []

    radius = (board_rect.width / 12.0) * 0.4

    for idx, data in enumerate(board_state['positions']):
        row, col_vis = point_index_to_display(idx)
        
        tri_color = TRI_A if (col_vis % 2) == (0 if row == 'top' else 1) else TRI_B
        if idx == selected_idx:
            tri_color = HIGHLIGHT_COLOR
            
        draw_triangle(surface, board_rect, col_vis, row, tri_color)
        
        if data:
            color_name, count = data
            
            for i in range(min(count, MAX_VISIBLE_STACK)):
                cy_base = board_rect.top + radius if row == 'top' else board_rect.bottom - radius
                cy_offset = (i * radius * 2) if row == 'top' else -(i * radius * 2)
                cy = cy_base + cy_offset
                
                x_center = board_rect.left + col_vis * (board_rect.width / 12.0) + (board_rect.width / 24.0)
                cx = x_center
                
                label = None
                if i == MAX_VISIBLE_STACK - 1 and count > MAX_VISIBLE_STACK:
                    label = str(count)
                
                draw_checker(surface, (cx, cy), radius, WHITE if color_name == 'white' else BLACK, label, font)
                hitmap[idx].append((cx, cy, radius))

    cx_bar = bar_rect.centerx
    
    count_bar_white = board_state['bar']['white']
    for i in range(min(count_bar_white, MAX_VISIBLE_STACK)):
        cy = bar_rect.top + radius + (i * radius * 2)
        label = None
        if i == MAX_VISIBLE_STACK - 1 and count_bar_white > MAX_VISIBLE_STACK:
            label = str(count_bar_white)
        draw_checker(surface, (cx_bar, cy), radius, WHITE, label, font)
        hitmap['bar_white'].append((cx_bar, cy, radius))

    count_bar_black = board_state['bar']['black']
    for i in range(min(count_bar_black, MAX_VISIBLE_STACK)):
        cy = bar_rect.bottom - radius - (i * radius * 2)
        label = None
        if i == MAX_VISIBLE_STACK - 1 and count_bar_black > MAX_VISIBLE_STACK:
            label = str(count_bar_black)
        draw_checker(surface, (cx_bar, cy), radius, BLACK, label, font)
        hitmap['bar_black'].append((cx_bar, cy, radius))
        
    if selected_idx == 'bar_white' or selected_idx == 'bar_black':
         pygame.draw.rect(surface, HIGHLIGHT_COLOR, bar_rect, 3)

    return hitmap


def draw_game_info(surface, game, dice_values, message, font):
    player = game.get_current_player()
    player_text = f"Turno de: {player.name} ({player.color.capitalize()})"
    player_surf = font.render(player_text, True, TEXT)
    surface.blit(player_surf, (MARGIN_X, MARGIN_Y / 2 - 10))

    dice_text = f"Dados: {dice_values if dice_values else '--'}"
    dice_surf = font.render(dice_text, True, TEXT)
    dice_rect = dice_surf.get_rect(center=(WIDTH / 2, MARGIN_Y / 2))
    surface.blit(dice_surf, dice_rect)

    inst_text = "[R] Tirar | [E] Fin Turno | [Q] Salir"
    inst_surf = font.render(inst_text, True, TEXT)
    inst_rect = inst_surf.get_rect(topright=(WIDTH - MARGIN_X, MARGIN_Y / 2 - 10))
    surface.blit(inst_surf, inst_rect)
    
    msg_surf = font.render(message, True, MSG_COLOR if "Error" in message or "Inválido" in message else TEXT)
    msg_rect = msg_surf.get_rect(center=(WIDTH / 2, HEIGHT - MARGIN_Y / 2))
    surface.blit(msg_surf, msg_rect)


def hit_test(hitmap, pos):
    mx, my = pos
    
    for bar_key in ('bar_white', 'bar_black'):
        circles = hitmap.get(bar_key, [])
        if circles:
            (cx, cy, r) = circles[-1]
            dx, dy = mx - cx, my - cy
            if dx * dx + dy * dy <= r * r:
                return bar_key

    for idx, circles in hitmap.items():
        if isinstance(idx, int) and circles:
            (cx, cy, r) = circles[-1]
            dx, dy = mx - cx, my - cy
            if dx * dx + dy * dy <= r * r:
                return idx
                
    board_rect_width = WIDTH - 2 * MARGIN_X
    board_rect_height = HEIGHT - 2 * MARGIN_Y
    
    for idx in range(24):
        if idx not in hitmap or not hitmap[idx]:
            row, col_vis = point_index_to_display(idx)
            
            x0 = MARGIN_X + col_vis * (board_rect_width / 12.0)
            x1 = x0 + (board_rect_width / 12.0)
            
            y0 = MARGIN_Y if row == 'top' else (MARGIN_Y + board_rect_height / 2.0)
            y1 = (MARGIN_Y + board_rect_height / 2.0) if row == 'top' else (HEIGHT - MARGIN_Y)
            
            if x0 <= mx <= x1 and y0 <= my <= y1:
                return idx
                
    return None


def main():
    pygame.init()
    pygame.display.set_caption("Backgammon (Pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font_main = pygame.font.SysFont(None, 28)
    font_checker = pygame.font.SysFont(None, 20)

    game = Game("Jugador 1", "Jugador 2")
    game.start()

    hitmap = {}
    
    selected_piece_idx = None
    dice_values = []
    game_message = f"¡Bienvenido! Turno de {game.get_current_player().name}. Presiona [R] para tirar."
    
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                
                elif e.key == pygame.K_r:
                    try:
                        game.roll_dice()
                        dice_values = game.get_dice().get_available_values()
                        game_message = f"Dados: {dice_values}"
                    except (NotYourTurnError, InvalidMoveError) as err:
                        game_message = str(err)
                
                elif e.key == pygame.K_e:
                    try:
                        game.end_turn()
                        dice_values = []
                        selected_piece_idx = None
                        game_message = f"Turno de: {game.get_current_player().name}. Presiona [R]."
                    except (NotYourTurnError, InvalidMoveError) as err:
                        game_message = str(err)
            
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                idx = hit_test(hitmap, e.pos)
                game_message = ""
                
                if idx is None:
                    selected_piece_idx = None
                    continue
                
                current_player = game.get_current_player()
                current_color = current_player.color
                board_state = game.get_board().get_state()

                if selected_piece_idx is None:
                    if idx == f'bar_{current_color}':
                        selected_piece_idx = idx
                        game_message = "Pieza de la barra seleccionada."
                    
                    elif isinstance(idx, int) and board_state["positions"][idx] and board_state["positions"][idx][0] == current_color:
                        selected_piece_idx = idx
                        game_message = f"Pieza seleccionada en {idx}."
                    
                    else:
                        game_message = "Posición inválida o sin piezas."
                
                else:
                    if idx == selected_piece_idx:
                        selected_piece_idx = None
                        game_message = "Movimiento cancelado."
                        continue
                    
                    from_pos = selected_piece_idx
                    to_pos = idx
                    selected_piece_idx = None
                    
                    if not isinstance(to_pos, int):
                        game_message = "Movimiento inválido (destino no es un triángulo)."
                        continue
                    
                    try:
                        game.move_piece(from_pos, to_pos)
                        game_message = f"Movimiento exitoso: {from_pos} -> {to_pos}"
                        dice_values = game.get_dice().get_available_values()
                    
                    except (InvalidMoveError, NotYourTurnError) as err:
                        game_message = str(err)
                        

        current_board_state = game.get_board().get_state()
        
        hitmap = draw_board_and_pieces(screen, current_board_state, font_checker, selected_piece_idx)
        
        draw_game_info(screen, game, dice_values, game_message, font_main)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print("Saliendo de Pygame.")


if __name__ == "__main__":
    main()