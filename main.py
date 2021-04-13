import pygame as pg

pg.init()
from game import Game

# Fenetre de jeu
pg.display.set_caption("Cav' Fighter")
screen = pg.display.set_mode((1080, 720))

# Background
background = pg.image.load('assets/game_bg.jpg')
background = pg.transform.scale(background, (1080, 720))
# Charger Jeu
game = Game()

# Boucle pour maintenir affichage jeu
running = True

# Affichage de la fin
police = pg.font.SysFont("Bradley Hand ITC", 30)  # Définition police et taille
police.set_bold(True)
text_endP1 = police.render("Joueur 1 gagne ! ", 1, (255, 0, 0))
text_endP2 = police.render("Joueur 2 gagne !", 1, (255, 0, 0))

while running:

    # Appliquer background
    screen.blit(background, (0, 0))
    if game.is_playing:
        game.window_update(screen)
    else:
        game.choice_window(screen, police)

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

                if event.key == pg.K_SPACE:
                    if len(game.projs1) < 10:  # quota maximum de 10 projectiles à lancer
                        game.create_proj(game.P1)
                        print("J1 : il vous reste", 10 - len(game.projs1), " projectiles à lancer")
                        game.projs1[len(game.projs1) - 1].init_shoot(
                            game.P1)  # on initialise le shoot du dernier élément

                if event.key == pg.K_KP0:
                    if len(game.projs2) < 12:  # quota maximum de 12 projectiles à lancer
                        game.create_proj(game.P2)
                        print("J2 : il vous reste", 12 - len(game.projs2), "projectiles à lancer")
                        game.projs2[len(game.projs2) - 1].init_shoot(game.P2)

                if event.key == pg.K_z:
                    if not game.P1.is_up():
                        game.P1.init_jump()
                if event.key == pg.K_UP:
                    if not game.P2.is_up():
                        game.P2.init_jump()

                if event.key == pg.K_u:
                    if game.P1.health< game.P1.max_health-game.P1.heal:
                        game.P1.health += game.P1.heal
                    else:
                        game.P1.health = game.P1.max_health

                if event.key == pg.K_KP2:
                    if game.P2.health < game.P2.max_health - game.P2.heal:
                        game.P2.health += game.P2.heal
                    else:
                        game.P2.health = game.P2.max_health

                game.pressed[event.key] = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            for player in game.list_player:
                if player.rect.collidepoint(event.pos):
                    game.choose_player(player)

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False
