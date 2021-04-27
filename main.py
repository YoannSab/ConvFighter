import pygame as pg
from game import Game

pg.init()

# Fenetre de jeu
pg.display.set_caption("Conv' Fighter")
screen = pg.display.set_mode((1080, 720))
# Background
background = pg.image.load('assets/game_bg3.jpg')
background = pg.transform.scale(background, (1080, 720))
option = pg.transform.scale(pg.image.load('assets/option.png'), (40, 40))
option_rect = option.get_rect()
option_rect.x = screen.get_width() - 70
option_rect.y = 20

# Charger Jeu
game = Game()

# Boucle pour maintenir affichage jeu
running = True
# Affichage de la fin
police = pg.font.SysFont("Arial", 30)  # Définition police et taille
police.set_bold(True)

while running:
    # Appliquer background

    screen.blit(background, (0, 0))
    screen.blit(option, option_rect)
    if game.want_menu:
        game.menu(screen)
    elif game.is_playing:
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

                # choix des personnages
                if (event.key == pg.K_d or event.key == pg.K_RIGHT) and not game.choice_is_done:
                    if game.player_courant is None:
                        game.player_courant = game.list_player[len(game.list_player) - 1]
                    if not game.list_player.index(game.player_courant) == len(game.list_player) - 1:
                        game.player_courant = game.list_player[game.list_player.index(game.player_courant) + 1]
                    else:
                        game.player_courant = game.list_player[0]
                    game.select_sound.play()

                if (event.key == pg.K_q or event.key == pg.K_LEFT) and not game.choice_is_done:
                    if game.player_courant is None:
                        game.player_courant = game.list_player[1]
                    if not game.list_player.index(game.player_courant) == 0:
                        game.player_courant = game.list_player[game.list_player.index(game.player_courant) - 1]
                    else:
                        game.player_courant = game.list_player[len(game.list_player) - 1]
                    game.select_sound.play()

                if (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER) and not game.choice_is_done and game.player_courant is not None:
                    if not game.player_courant == game.P1:
                        game.choose_player(game.player_courant)
                    game.click_sound.play()
                game.pressed[event.key] = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            if not game.choice_is_done and not game.want_menu:
                for player in game.list_player:
                    if player.splashart_rect.collidepoint(event.pos):
                        game.click_sound.play()
                        if player != game.P1:
                            game.choose_player(player)
                        else:
                            print("deja pris")
                if game.play_button_rect.collidepoint(event.pos):
                    game.click_sound.play()
                    game.try_launch_game()

            if game.img_replay_rect.collidepoint(event.pos) and game.game_over:
                game.new_game()
            if option_rect.collidepoint(event.pos):
                game.click_sound.play()
                game.want_menu = True
            if game.want_menu:
                for button in game.list_button:
                    if button.rect.collidepoint(event.pos):
                        button.function()
                        game.click_sound.play()

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False

