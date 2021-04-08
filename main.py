import pygame as pg

pg.init()
import time
from game import Game

# Fenetre de jeu
pg.display.set_caption("Cav' Fighter")
screen = pg.display.set_mode((1080, 720))

# Background
background = pg.image.load('assets/game_bg.jpg')

# Charger Jeu
game = Game()

# Boucle pour maintenir affichage jeu
running = True

# Valeurs bool pour jump
active = False
up = True

while running and game.P1.health != 0 and game.P2.health != 0:

    # Appliquer background
    screen.blit(background, (-400, -200))

    # Appliquer image P1 et P2
    screen.blit(game.P1.image, game.P1.rect)
    screen.blit(game.P2.image, game.P2.rect)

    # Affichage des points de vie
    police_health = pg.font.SysFont("Arial", 50)  # Définition police et taille
    text_healthP1 = police_health.render(str(game.P1.health), 1, (255, 0, 0))
    text_healthP2 = police_health.render(str(game.P2.health), 1, (255, 0, 0))
    screen.blit(text_healthP1, (game.P1.rect.x + 30, game.P1.rect.y - 60))
    screen.blit(text_healthP2, (game.P2.rect.x + 35, game.P2.rect.y - 60))

    # Verifier les touches pressées
    # P1
    if game.pressed.get(pg.K_d) and game.P1.rect.x < 1050:
        # time.sleep(0.01)
        game.P1.move_right()
    elif game.pressed.get(pg.K_q) and game.P1.rect.x > -100:
        # time.sleep(0.01)
        game.P1.move_left()

    # P2
    if game.pressed.get(pg.K_RIGHT) and game.P2.rect.x < 1050:
        # time.sleep(0.01)
        game.P2.move_right()
    elif game.pressed.get(pg.K_LEFT) and game.P2.rect.x > -100:
        # time.sleep(0.01)
        game.P2.move_left()

    # Mise à jour de la fenêtre
    pg.display.flip()

    # Si le joueur ferme la fenetre
    for event in pg.event.get():
        # Evenement fermeture de fenetre
        if event.type == pg.QUIT:
            running = False
            pg.quit()

        # Quelle touche est pressée

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                pg.quit()
            else:
                if event.key == pg.K_j:
                    game.P1.punch(game.P2)

                if event.key == pg.K_KP1:
                    game.P2.punch(game.P1)

                game.pressed[event.key] = True

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False
