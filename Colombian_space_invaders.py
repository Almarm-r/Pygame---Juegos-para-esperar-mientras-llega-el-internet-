import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juegos para esperar mientras carga el internet")
background_image = pygame.image.load("background Domestika-original.jpg")  
background_rect = background_image.get_rect()


# Definir la nave espacial del jugador
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5

# Definir enemigos
enemy_radius = 25
enemy_speed = 3
enemies = [{"x": random.randint(0, width - 2 * enemy_radius), "y": random.randint(50, 200)} for _ in range(4)]

# Definir disparos del jugador
bullet_size = 10
bullet_speed = 7
bullets = []

# Contador de puntos
score = 0

max_enemies_on_floor = 5
game_state = "playing"
enemies_on_floor = 0  

# Configuración del reloj
clock = pygame.time.Clock()

# Función para dibujar la nave espacial del jugador
def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, player_size, player_size])

# Función para dibujar un enemigo como círculo
def draw_enemy(x, y):
    pygame.draw.circle(screen, WHITE, (x + enemy_radius, y + enemy_radius), enemy_radius)

# Función para dibujar un disparo
def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, bullet_size, bullet_size])

# Función para mostrar el puntaje en la pantalla
def show_score(score):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Puntuación: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
#Función con las intrucciones del menú
def show_instructions():
    font = pygame.font.SysFont(None, 12)
    instruction_text = font.render("Press: P to pause or Q to exit", True, WHITE)
    screen.blit(instruction_text, (width - 200, 25))
    
# Función para mostrar el menú de pausa
def show_pause_menu():
    font = pygame.font.SysFont(None, 50)
    pause_text = font.render("Juego en Pausa", True, WHITE)
    score_text = font.render("Puntuación: " + str(score), True, WHITE)
    screen.blit(pause_text, (width // 2 - 150, height // 2 - 50))
    screen.blit(score_text, (width // 2 - 150, height // 2 + 50))
    pygame.display.flip()

    # Bucle de pausa
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
 #                   game_state = "playing"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()



# Función para mostrar el menú de Game Over
def show_game_over_menu():
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Presiona 'R' para reiniciar", True, WHITE)
    screen.blit(game_over_text, (width // 2 - 150, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - 180, height // 2 + 50))
    pygame.display.flip()

    # Bucle hasta que el jugador presione 'R'
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "playing":
                # Agregar un disparo a la lista de disparos
                bullets.append({"x": player_x + player_size // 2 - bullet_size // 2, "y": player_y})
            elif event.key == pygame.K_p and game_state == "playing":
                # Pausar el juego
                game_state = "paused"
                show_pause_menu()
                if event.key == pygame.K_q:
                # Salir del juego
                   pygame.quit()
                   sys.exit()
                elif event.key == pygame.K_p and game_state == "paused":
                     game_state = "playing"
                
                 
                
            elif event.key == pygame.K_r and game_state == "game over":
                # Reiniciar el juego
                player_x = width // 2 - player_size // 2
                player_y = height - 2 * player_size
                enemies = [{"x": random.randint(0, width - 2 * enemy_radius), "y": random.randint(50, 200)} for _ in range(4)]
                bullets = []
                score = 0
                game_state = "playing"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed

    if game_state == "playing":
        # Actualizar posición de enemigos y comprobar colisiones
	# Contador de enemigos que han llegado al piso
        for enemy in enemies:
            enemy["y"] += enemy_speed


            for bullet in bullets:
                if (
                        bullet["x"] < enemy["x"] + 2 * enemy_radius
                        and bullet["x"] + bullet_size > enemy["x"]
                        and bullet["y"] < enemy["y"] + 2 * enemy_radius
                        and bullet["y"] + bullet_size > enemy["y"]
                ):
                    # Colisión del disparo con un enemigo
                    bullets.remove(bullet)
                    enemy["y"] = 0
                    enemy["x"] = random.randint(0, width - 2 * enemy_radius)
                    score += 1

            if enemy["y"] > height:
                enemy["y"] = 0
                enemy["x"] = random.randint(0, width - 2 * enemy_radius)
                enemies_on_floor += 1

        # Eliminar disparos que salen de la pantalla
        bullets = [bullet for bullet in bullets if bullet["y"] > 0]

        # Actualizar posición de los disparos
        for bullet in bullets:
            bullet["y"] -= bullet_speed

        # Verificar colisión de jugador con enemigo
        if any(
                player_x < enemy["x"] + 2 * enemy_radius
                and player_x + player_size > enemy["x"]
                and player_y < enemy["y"] + 2 * enemy_radius
                and player_y + player_size > enemy["y"]
                for enemy in enemies
        ) or enemies_on_floor > max_enemies_on_floor:
            game_state = "game over"
            show_game_over_menu()
            # Reiniciar el juego
            player_x = width // 2 - player_size // 2
            player_y = height - 2 * player_size
            enemies = [{"x": random.randint(0, width - 2 * enemy_radius), "y": random.randint(50, 200)} for _ in range(4)]
            bullets = []
            score = 0
            enemies_on_floor = 0  
            game_state = "playing"
            
    elif game_state == "paused":
        # Manejar eventos mientras el juego está pausado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "playing"


    # Dibujar el fondo. 
    screen.fill(BLACK)
    screen.blit(background_image, background_rect)

    # Dibujar la nave espacial del jugador
    draw_player(player_x, player_y)

    # Dibujar enemigos como círculos
    for enemy in enemies:
        draw_enemy(enemy["x"], enemy["y"])

    # Dibujar disparos
    for bullet in bullets:
        draw_bullet(bullet["x"], bullet["y"])

    # Mostrar el puntaje en la pantalla
    show_score(score) 
    # Mostrar el contador de enemigos en el piso
    font = pygame.font.SysFont(None, 15)
    enemies_on_floor_text = font.render("Enemigos en el piso: " + str(enemies_on_floor), True, WHITE)
    screen.blit(enemies_on_floor_text, (width - 200, 10))
    #Mostrar las instrucciones de menú.
    show_instructions()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(60)
