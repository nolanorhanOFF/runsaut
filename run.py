import pygame
import random
import os
import sys

# Initialisation de pygame
pygame.init()
pygame.mixer.init()  # Initialisation du mixer pour les sons

# Charger le son de saut
jump_sound = pygame.mixer.Sound("saut.mp3")

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Runner avec Pouvoirs")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)  # Couleur bleue pour le ciel
BROWN = (139, 69, 19)  # Couleur marron pour la terre
GREEN = (0, 255, 0)    # Couleur verte pour l'herbe
YELLOW = (255, 255, 0)  # Couleur jaune pour les objets qui tombent
CYAN = (0, 255, 255)    # Couleur cyan pour le pouvoir de triple saut

# Joueur
player_size = 40
player_x = 100
player_y = HEIGHT - player_size - 10
player_vel_y = 0
gravity = 0.6
jump_power = -12
is_jumping = False
can_double_jump = False  # Permet de savoir si le joueur peut faire un double saut
can_triple_jump = False  # Permet de savoir si le joueur peut faire un triple saut
has_shield = False

# Obstacles
obstacle_width = 30
obstacle_height = 50
obstacle_speed = 7
obstacles = []

# Pouvoirs
shield_duration = 100
shield_active = 0
dash_duration = 30
dash_active = 0
dash_speed = 14

# Objets qui tombent
falling_objects = []
falling_speed = 5

# Pouvoir de triple saut
triple_jump_power = 1 * 60  # 1 minute
triple_jump_active = 0

# Compteur de score
score = 0

# Menu principal
font = pygame.font.Font(None, 48)

def draw_menu():
    screen.fill(BLUE)  # Fond bleu pour le ciel
    
    # Dessiner l'herbe et la terre
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))  # Herbe
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - 30, WIDTH, 30))    # Terre
    
    # Dessiner des objets qui tombent dans le menu
    if random.randint(1, 80) == 1:
        falling_objects.append([random.randint(0, WIDTH - 20), 0])
    for obj in falling_objects[:]:
        obj[1] += falling_speed
        if obj[1] > HEIGHT:
            falling_objects.remove(obj)
        pygame.draw.circle(screen, YELLOW, (obj[0], obj[1]), 10)

    title = font.render("INFINITE RUNNER", True, WHITE)
    start_text = font.render("Appuyez sur ENTREE pour jouer", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    pygame.display.flip()

def pause_menu():
    screen.fill(BLACK)
    pause_text = font.render("PAUSE - Appuyez sur ECHAP pour continuer", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Fonction pour réinitialiser le jeu
def reset_game():
    global player_x, player_y, player_vel_y, is_jumping, can_double_jump, can_triple_jump, obstacles, score, shield_active, dash_active, falling_objects, triple_jump_active
    player_x = 100
    player_y = HEIGHT - player_size - 10  # Réinitialiser la position du joueur à l'écran
    player_vel_y = 0
    is_jumping = False
    can_double_jump = False
    can_triple_jump = False
    obstacles = []
    score = 0
    shield_active = 0
    dash_active = 0
    triple_jump_active = 0
    falling_objects = []

# Fonction pour sauvegarder le score
def save_score():
    with open("score.txt", "w") as file:
        file.write(str(score))

# Fonction pour charger le score
def load_score():
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            return int(file.read())
    return 0

# Fonction principale du jeu
def game_loop():
    global player_x, player_y, player_vel_y, is_jumping, can_double_jump, can_triple_jump, obstacles, score, shield_active, dash_active, falling_objects, triple_jump_active
    
    # Écran de démarrage
    menu = True
    running = False
    paused = False
    while menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menu = False
                running = True
                reset_game()

    # Horloge
    clock = pygame.time.Clock()
    
    while running:
        if paused:
            pause_menu()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False
            continue
        
        screen.fill(WHITE)
        
        # Dessiner l'herbe et la terre sous le joueur
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))  # Herbe
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - 30, WIDTH, 30))    # Terre

        # Dessiner le joueur (le carré)
        pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_size, player_size))

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not is_jumping:  # Premier saut
                        player_vel_y = jump_power
                        is_jumping = True
                        can_double_jump = True
                        jump_sound.play()  # Jouer le son de saut
                    elif can_double_jump:  # Double saut
                        player_vel_y = jump_power
                        can_double_jump = False  # Ne peut plus double sauter après
                        jump_sound.play()  # Jouer le son de saut
                    elif can_triple_jump:  # Triple saut
                        player_vel_y = jump_power
                        can_triple_jump = False  # Ne peut plus triple sauter après
                        jump_sound.play()  # Jouer le son de saut
                if event.key == pygame.K_b and shield_active == 0:
                    shield_active = shield_duration
                if event.key == pygame.K_d and dash_active == 0:
                    dash_active = dash_duration
                if event.key == pygame.K_ESCAPE:
                    paused = True
        
        # Appliquer la gravité
        player_vel_y += gravity
        player_y += player_vel_y
        
        # Empêcher de tomber
        if player_y >= HEIGHT - player_size - 10:
            player_y = HEIGHT - player_size - 10
            is_jumping = False
            can_double_jump = False  # Réinitialiser la possibilité du double saut
            can_triple_jump = False  # Réinitialiser la possibilité du triple saut
        
        # Gérer le bouclier
        if shield_active > 0:
            shield_active -= 1
            has_shield = True
        else:
            has_shield = False
        
        # Gérer le dash
        if dash_active > 0:
            dash_active -= 1
            obstacle_speed = dash_speed
        else:
            obstacle_speed = 7
        
        # Gérer les obstacles
        if random.randint(1, 60) == 1:
            obstacles.append([WIDTH, HEIGHT - obstacle_height - 10])
        for obs in obstacles[:]:
            obs[0] -= obstacle_speed
            if obs[0] < -obstacle_width:
                obstacles.remove(obs)
                score += 1
            pygame.draw.rect(screen, RED, (obs[0], obs[1], obstacle_width, obstacle_height))
        
        # Générer des objets qui tombent
        if random.randint(1, 100) == 1:
            falling_objects.append([random.randint(0, WIDTH - 20), 0])
        for obj in falling_objects[:]:
            obj[1] += falling_speed
            if obj[1] > HEIGHT:
                falling_objects.remove(obj)
            pygame.draw.circle(screen, YELLOW, (obj[0], obj[1]), 10)

        # Pouvoir de triple saut (cyan)
        if random.randint(1, 200) == 1:
            pygame.draw.rect(screen, CYAN, (random.randint(0, WIDTH - 20), HEIGHT - 50, 20, 20))
        
        # Vérifier les collisions avec les objets qui tombent
        for obj in falling_objects:
            if player_x < obj[0] < player_x + player_size and player_y < obj[1] < player_y + player_size:
                falling_objects.remove(obj)
                can_triple_jump = True  # Activer le triple saut
        
        # Afficher le score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Afficher le temps restant pour le pouvoir de triple saut
        if triple_jump_active > 0:
            triple_jump_active -= 1
        pygame.display.flip()
        
        # Vérifier les collisions avec les obstacles
        for obs in obstacles:
            if player_x < obs[0] < player_x + player_size and player_y < obs[1] < player_y + player_size:
                if has_shield:
                    obstacles.remove(obs)  # Le bouclier protège contre les obstacles
                else:
                    save_score()
                    reset_game()
                    running = False
                    os.execv(sys.executable, ['python'] + sys.argv)  # Relancer le jeu et fermer l'ancien
                    break
        
        clock.tick(60)  # Limiter à 60 images par seconde

    pygame.quit()
    sys.exit()

# Lancer le jeu
game_loop()
