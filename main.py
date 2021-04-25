import pygame as pg

pg.init()
from game import Game

# Fenetre de jeu
pg.display.set_caption("Conv' Fighter")
screen = pg.display.set_mode((1080, 720))
# Background
background = pg.image.load('assets/game_bg3.jpg')
background = pg.transform.scale(background, (1080, 720))
# Charger Jeu
game = Game()

# Boucle pour maintenir affichage jeu
running = True

# Affichage de la fin
police = pg.font.SysFont("Bradley Hand ITC", 30)  # Définition police et taille
police.set_bold(True)
player_courant = None
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
                # coup de poing
                if event.key == pg.K_j:
                    if not game.P1.cooldown:
                        game.P1.punch(game.P2)
                        game.P1.cooldown = True
                        game.cd_P1.start()

                if event.key == pg.K_KP1:
                    if not game.P2.cooldown:
                        game.P2.punch(game.P1)
                        game.P2.cooldown = True
                        game.cd_P2.start()
                # tir de projectile
                if event.key == pg.K_SPACE:
                    if game.P1.mana > game.P1.projectile.mana_cost and not game.P1.is_shooting:
                        game.create_proj(game.P1)
                        game.projs1[len(game.projs1) - 1].shot = True
                        game.P1.current_index = 0
                        game.P1.is_shooting = True

                if event.key == pg.K_KP0:
                    if game.P2.mana > game.P2.projectile.mana_cost and not game.P2.is_shooting:
                        game.create_proj(game.P2)
                        game.projs2[len(game.projs2) - 1].shot = True
                        game.P2.current_index = 0
                        game.P2.is_shooting = True
                # saut
                if event.key == pg.K_z:
                    if not game.P1.is_up(game.list_plateformes, game.P2):
                        game.P1.init_jump()

                if event.key == pg.K_UP:
                    if not game.P2.is_up(game.list_plateformes, game.P1):
                        game.P2.init_jump()
                # tombe
                if event.key == pg.K_s:
                    if not game.P1.is_on_player(game.P2):
                        game.P1.traverse_plateforme = True
                        game.P1.fall_direction = None

                if event.key == pg.K_DOWN:
                    if not game.P2.is_on_player(game.P1):
                        game.P2.traverse_plateforme = True
                        game.P2.fall_direction = None
                # heal
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
                    game.choice_sound.play()
                    if player != game.P1:
                        screen.blit(pg.image.load('assets/dark_green.png'), player.splashart_rect)
                        pg.time.wait(100)
                        game.choose_player(player)
                    else:
                        print("deja pris")
            if game.img_replay_rect.collidepoint(event.pos):
                game.new_game()

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False
    if not game.choice_is_done:
        for player in game.list_player:
            if player.splashart_rect.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                screen.blit(pg.image.load('assets/green.png'), player.splashart_rect)
                if not player == player_courant:
                    game.select_sound.play()
                player_courant = player
                break
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    # Mise à jour de la fenêtre
    pg.display.flip()
