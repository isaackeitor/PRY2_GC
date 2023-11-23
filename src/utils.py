import pygame
import math

# Functions


def draw_map(screen, map, cellSize, screen_width, screen_height):
    wallColor = (115, 115, 115)
    floorColor = (30, 175, 30)

    map_width = len(map[0]) * cellSize

    # Calcular la posición inicial del minimapa en la esquina superior derecha
    minimap_start_x = screen_width - map_width
    minimap_start_y = 0

    for y in range(len(map)):
        for x in range(len(map[0])):
            color = floorColor
            if map[y][x] == 1:
                color = wallColor

            current_x = x * cellSize + minimap_start_x
            current_y = y * cellSize + minimap_start_y

            pygame.draw.rect(
                screen,
                color,
                (
                    current_x,
                    current_y,
                    cellSize,
                    cellSize,
                ),
            )


def draw_player(
    screen, player, width, height, map_width, map_height, screen_width, screen_height
):
    minimap_start_x = screen_width - width
    minimap_start_y = 0

    minimap_x = int(player.position.x / map_width * width) + minimap_start_x
    minimap_y = int(player.position.y / map_height * height) + minimap_start_y

    minimap_player_size = 4

    # Coordenadas para la punta del triángulo
    point_x = minimap_x + math.cos(player.direction) * minimap_player_size * 2
    point_y = minimap_y + math.sin(player.direction) * minimap_player_size * 2

    # Coordenadas para la base del triángulo
    base_angle = math.pi / 2  # Ángulo para los puntos de la base
    base1_x = minimap_x + math.cos(player.direction - base_angle) * minimap_player_size
    base1_y = minimap_y + math.sin(player.direction - base_angle) * minimap_player_size

    base2_x = minimap_x + math.cos(player.direction + base_angle) * minimap_player_size
    base2_y = minimap_y + math.sin(player.direction + base_angle) * minimap_player_size

    # Dibujar el triángulo
    pygame.draw.polygon(
        screen,
        (255, 255, 255),
        [(point_x, point_y), (base1_x, base1_y), (base2_x, base2_y)],
    )


def render(screen, player, CELLSIZE, window_width, window_height, world_map):
    # Colores para el suelo y el cielo
    floor_color = (50, 205, 50)  # Un verde que puede representar césped
    sky_color = (135, 206, 250)  # Un azul claro para el cielo

    # Pinta el cielo
    screen.fill(sky_color)

    # Pinta el suelo
    pygame.draw.rect(
        screen, floor_color, (0, window_height / 2, window_width, window_height / 2)
    )

    initial_color = (
        130,
        130,
        130,
    )  # Un verde fresco y claro que podría representar la hierba iluminada por el sol.
    final_color = (
        80,
        80,
        80,
    )  # Un verde más oscuro que representa las áreas sombreadas del campo.

    half_cell = CELLSIZE / 2
    half_height = window_height / 2
    d = half_cell / math.tan(player.FOV / 2)

    current_angle = player.direction - player.FOV / 2
    step = player.FOV / (window_width - 1)
    for i in range(0, window_width):
        draw, length, draw_horizontal = player.cast_ray(
            current_angle, world_map, CELLSIZE, screen
        )
        h2 = (length / d) * half_cell
        if h2 != 0:
            line_ratio = half_cell / h2
            half_line_length = half_height * line_ratio
            if draw:
                color = final_color
                if draw_horizontal:
                    color = initial_color
                pygame.draw.line(
                    screen,
                    color,
                    (i, half_height + half_line_length),
                    (i, half_height - half_line_length),
                )
            current_angle += step
