import pygame
from vector import * 
from player import *
from utils import *

# Inicialización de Pygame
pygame.init()

# Carga y reproducción de música de fondo y efecto de sonido
pygame.mixer.music.load('./../resources/champions.mp3')
pygame.mixer.music.play(-1)
referee = pygame.mixer.Sound('./../resources/referee.mp3')

# Configuración de la ventana
window_width = 800
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("UEFA Champions League")

# Inicialización de la fuente
pygame.font.init()
font = pygame.font.Font(None, int(window_height / 10))

# Inicialización del mapa del mundo
world_map = []

# Definición de los mapas para los modos de juego
partido = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

entrenamiento = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Configuración de FPS y reloj
fps = 144
clock = pygame.time.Clock()
juego = False
welcome_screen = True
selected_option = 0 

# Definición de colores
background_color = (235, 235, 195)
text_color = (20, 34, 62)
highlight_color = (0, 149, 182)  # Un azul cobalto brillante

# Carga y redimensionamiento del logo
logo_image_path = './../resources/UEFA_Champions_League.png'
logo_image = pygame.image.load(logo_image_path)
logo_image = pygame.transform.scale(logo_image, (150, 150))

# Posición del logo
logo_x = window_width - logo_image.get_width() - 10
logo_y = window_height - logo_image.get_height() - 10

# Inicialización de fuentes para el menú de bienvenida
welcome_font = pygame.font.Font(None, int(window_height / 15))
option_font = pygame.font.Font(None, int(window_height / 20))

# Creación de textos para el menú
welcome_text = welcome_font.render("UEFA Champions League", True, text_color)
controls_text = option_font.render("Enter para seleccionar, AWSD para jugar, ESC para salir", True, text_color)

# Posición de los textos del menú
welcome_rect = welcome_text.get_rect(center=(window_width / 2, window_height / 4))
controls_rect = controls_text.get_rect(center=(window_width / 2, window_height - 30))

# Definición de opciones del menú
menu_options = ["Jugar Partido", "Entrenamiento"]
menu_rects = []

# Creación de rectángulos para las opciones del menú
for i, option in enumerate(menu_options):
    option_text = option_font.render(option, True, text_color)
    option_rect = option_text.get_rect(center=(window_width / 2, window_height / 2 + i * 40))
    menu_rects.append((option_text, option_rect))

# Bucle principal del menú de bienvenida
while welcome_screen:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            welcome_screen = False

    # Lectura de entradas del teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        juego = True
        world_map = partido if selected_option == 0 else entrenamiento
        welcome_screen = False
    elif keys[pygame.K_ESCAPE]:
        pygame.quit()
        break

    # Navegación en el menú
    if keys[pygame.K_w] and selected_option > 0:
        selected_option -= 1  
    elif keys[pygame.K_s] and selected_option < len(menu_options) - 1:
        selected_option += 1 

    # Dibujado de elementos en la ventana
    window.fill(background_color)
    window.blit(logo_image, (logo_x, logo_y))
    window.blit(welcome_text, welcome_rect)
    window.blit(controls_text, controls_rect)

    # Resaltado de la opción seleccionada
    for i, (option_text, option_rect) in enumerate(menu_rects):
        if i == selected_option:
            highlighted_text = option_font.render(menu_options[i], True, highlight_color)
            window.blit(highlighted_text, option_rect)
        else:
            window.blit(option_text, option_rect)

    # Actualización de la pantalla y control de FPS
    pygame.display.update()
    clock.tick(fps)

# Configuración inicial del mapa y del jugador
CELLSIZE = 64
ancho = len(world_map[0]) * CELLSIZE
alto = len(world_map) * CELLSIZE

# Inicialización del jugador
posicion = vector(ancho / 2, alto / 2)
player = Player(posicion, 80 * math.pi / 180, 0, 25, 3)

# Bucle principal del juego
run = True
while run:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                referee.play()

    # Ejecución del juego
    if juego:
        delta_time = clock.tick(fps) / 1000

        # Limpieza de la ventana
        window.fill((0, 0, 0))

        # Tamaño del minimapa
        minimap_size = 20

        # Renderizado del juego
        render(window, player, CELLSIZE, window_width, window_height, world_map)
        draw_map(window, world_map, minimap_size, window_width, window_height)
        draw_player(window, player, len(world_map) * minimap_size, len(world_map[0]) * minimap_size, ancho, alto, window_width, window_height)

        # FPS
        fpsFONT = pygame.font.Font(None, int(window_height / 20))
        fps_text = fpsFONT.render(f"FPS: {int(clock.get_fps())}", True, (15, 15, 15))
        text_rect = fps_text.get_rect()
        text_rect.topleft = (0, 0)
        background_rect = pygame.Rect(text_rect.left, text_rect.top, text_rect.width, text_rect.height)
        pygame.draw.rect(window, background_color, background_rect)
        window.blit(fps_text, text_rect)

        # Movimiento y rotación del jugador
        player.moverse(delta_time, pygame.key.get_pressed(), world_map, CELLSIZE)
        
        # Indicador de falta
        falta_font = pygame.font.Font(None, int(window_height / 20))
        falta_text = falta_font.render("Presiona Space para pitar falta", True, (15, 15, 15))
        falta_rect = falta_text.get_rect()
        falta_rect.midbottom = (window_width / 2, window_height - 10)
        window.blit(falta_text, falta_rect)

        # Actualización de la ventana
        pygame.display.update()

        # Manejo de salida del juego
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            juego = False
            run = False
