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

while running:

    # Appliquer background
    screen.blit(background, (0, 0))
    if game.is_playing:
        # maj de la fenetre
        game.window_update(screen)
    elif game.game_over:
        game.end_window(screen)
    else:
        game.choice_window(screen, police)
    game.try_game_over()

    # Mise à jour de la fenêtre
    pg.display.flip()

    # Si le joueur ferme la fenetre
    for event in pg.event.get():
        # Evenement fermeture de fenetre
        if event.type == pg.QUIT:
            running = False
            game.timer.stop()
            pg.quit()

        # Quelle touche est pressée
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                game.timer.stop()
                pg.quit()
            else:
                if event.key == pg.K_j:
                    if game.P1.mana > 0:
                        game.P1.punch(game.P2)

                if event.key == pg.K_KP1:
                    if game.P2.mana > 0:
                        game.P2.punch(game.P1)

                if event.key == pg.K_SPACE:
                    if game.P1.mana > game.P1.projectile.mana_cost:
                        game.create_proj(game.P1)
                        game.projs1[len(game.projs1) - 1].init_shoot(
                            game.P1)  # on initialise le shoot du dernier élément

                if event.key == pg.K_KP0:
                    if game.P2.mana > game.P2.projectile.mana_cost:
                        game.create_proj(game.P2)
                        game.projs2[len(game.projs2) - 1].init_shoot(game.P2)

                if event.key == pg.K_z:
                    if not game.P1.is_up():
                        game.P1.init_jump()
                if event.key == pg.K_UP:
                    if not game.P2.is_up():
                        game.P2.init_jump()

                if event.key == pg.K_u:
                    if game.P1.mana > 0:
                        game.P1.get_healed()

                if event.key == pg.K_KP2:
                    if game.P2.mana > 0:
                        game.P2.get_healed()

                game.pressed[event.key] = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            for player in game.list_player:
                if player.splashart_rect.collidepoint(event.pos):
                    game.choose_player(player)
            if game.img_replay_rect.collidepoint(event.pos):
                game.new_game()

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False
