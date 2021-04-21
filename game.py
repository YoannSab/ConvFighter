import pygame as pg
from player import Player
from projectile import Projectile
import time
from threading import Timer
from timer import My_Timer
from plateforme import Plateforme


# Création de la classe Game
class Game:

    def __init__(self):

        self.proj1 = Projectile('balle de fusil', 10, 'assets/fire_ball.png', 30)
        self.proj2 = Projectile('balle de fusil2', 10, 'assets/arrow.png',30)
        self.marc = Player('Marc', 150, 1, 'assets/004-evil.png','assets/marc.png', 10, 5, self.proj1,100, 10)
        self.yoann = Player('Yoann', 110, 1, 'assets/002-angel.png','assets/yoann.png', 7, 2, self.proj2,100, 10)
        self.tristan = Player('Tristan', 160, 1, 'assets/001-sleeping.png','assets/tristan.png', 18, 6, self.proj1,100,10)
        self.arthur = Player('Arthur', 100, 1, 'assets/006-centaur.png','assets/arthur.png',8, 6, self.proj1,100,10)
        self.nathan = Player('Nathan', 120, 1, 'assets/003-bandit.png','assets/nathan.png', 10, 6, self.proj2,100,10)
        self.pierre = Player('Pierre', 80, 1, 'assets/005-nymph butterfly.png','assets/pierre.png', 6, 40, self.proj2,100,10)
        self.list_player = [self.marc, self.yoann, self.tristan, self.arthur, self.nathan, self.pierre]
        self.plat0 = Plateforme(0,400,300,350,20, 'assets/plateforme.png')
        self.plat1 = Plateforme(1, 200, 450, 250, 30, 'assets/plateforme2.png')
        self.plat2 = Plateforme(2, 700, 450, 250, 30, 'assets/plateforme2.png')
        self.list_plateformes = [self.plat0, self.plat1, self.plat2]
        self.P1 = None
        self.P2 = None
        self.pressed = {}
        self.projs1 = []
        self.projs2 = []
        self.is_playing = False
        self.img_go = pg.image.load("assets/game_over.png")
        self.img_go = pg.transform.scale(self.img_go, (300, 200))
        self.img_go_rect = self.img_go.get_rect()
        self.img_go_rect.x = 400
        self.img_go_rect.y = 100
        self.img_replay = pg.image.load("assets/replay.png")
        self.img_replay = pg.transform.scale(self.img_replay, (300, 80))
        self.img_replay_rect = self.img_replay.get_rect()
        self.img_replay_rect.x = 400
        self.img_replay_rect.y = 500
        self.game_over = False
        self.winner = None
        # regen du mana toutes les 1 secondes
        self.timer = My_Timer(1.0, self.mana_regen_in_game)

    def create_proj(self, player):
        if player.number_play == 1:
            self.projs1.append(
                Projectile(player.projectile.name, player.projectile.damage, player.projectile.image_string,player.projectile.mana_cost))
        else:
            self.projs2.append(
                Projectile(player.projectile.name, player.projectile.damage, player.projectile.image_string, player.projectile.mana_cost))

    def choose_player(self, player):
        if self.P1 is None:
            self.P1 = player
            self.P1.number_play = 1
        else:
            self.P2 = player
            self.P2.number_play = 2
        self.launch_game()

    def launch_game(self):
        if self.P1 is not None and self.P2 is not None:
            self.P1.last_direction = 'Right'
            self.P1.pos_start()
            self.P2.last_direction = 'Left'
            self.P2.pos_start()
            self.is_playing = True
            self.timer.start()

    def try_game_over(self):
        if self.is_playing:
            if self.P1.health <= 0 or self.P2.health <= 0:
                self.game_over = True
                self.is_playing = False
                self.timer.stop()
                if self.P1.health <= 0:
                    self.winner = self.P2
                else:
                    self.winner = self.P1

    def new_game(self):
        for player in self.list_player:
            player.health = player.max_health
            player.mana = player.mana_max
        self.P1 = None
        self.P2 = None
        self.winner = None
        self.projs1 = []
        self.projs2 = []
        self.game_over = False

    def end_window(self, screen):
        screen.blit(self.img_go, self.img_go_rect)
        screen.blit(self.img_replay, self.img_replay_rect)
        text_nom_winner = pg.font.SysFont("Calibri", 60).render("Le gagnant est "+self.winner.name+", Bravo !", 1, (0, 187, 254))
        screen.blit(text_nom_winner, (200, 400))

    def choice_window(self, screen, police):
        self.marc.splashart_rect.x = 300
        self.marc.splashart_rect.y = 100
        screen.blit(self.marc.splashart, self.marc.splashart_rect)
        text_nom_marc = police.render(str(self.marc.name), 1, (0, 187, 254))
        screen.blit(text_nom_marc, (self.marc.splashart_rect.x + 30, self.marc.splashart_rect.y - 40))

        self.yoann.splashart_rect.x = 500
        self.yoann.splashart_rect.y = 100
        screen.blit(self.yoann.splashart, self.yoann.splashart_rect)
        text_nom_yoann = police.render(str(self.yoann.name), 1, (0, 187, 254))
        screen.blit(text_nom_yoann, (self.yoann.splashart_rect.x + 30, self.yoann.splashart_rect.y - 40))

        self.tristan.splashart_rect.x = 700
        self.tristan.splashart_rect.y = 100
        screen.blit(self.tristan.splashart, self.tristan.splashart_rect)
        text_nom_tristan = police.render(str(self.tristan.name), 1, (0, 187, 254))
        screen.blit(text_nom_tristan, (self.tristan.splashart_rect.x + 30, self.tristan.splashart_rect.y - 40))

        self.arthur.splashart_rect.x = 300
        self.arthur.splashart_rect.y = 350
        screen.blit(self.arthur.splashart, self.arthur.splashart_rect)
        text_nom_arthur = police.render(str(self.arthur.name), 1, (0, 187, 254))
        screen.blit(text_nom_arthur, (self.arthur.splashart_rect.x + 30, self.arthur.splashart_rect.y - 40))

        self.nathan.splashart_rect.x = 500
        self.nathan.splashart_rect.y = 350
        screen.blit(self.nathan.splashart, self.nathan.splashart_rect)
        text_nom_nathan = police.render(str(self.nathan.name), 1, (0, 187, 254))
        screen.blit(text_nom_nathan, (self.nathan.splashart_rect.x + 30, self.nathan.splashart_rect.y - 40))

        self.pierre.splashart_rect.x = 700
        self.pierre.splashart_rect.y = 350
        screen.blit(self.pierre.splashart, self.pierre.splashart_rect)
        text_nom_pierre = police.render(str(self.pierre.name), 1, (0, 187, 254))
        screen.blit(text_nom_pierre, (self.pierre.splashart_rect.x + 30, self.pierre.splashart_rect.y - 40))

    def window_update(self, screen):
        # Appliquer image P1 et P2
        screen.blit(self.P1.image, self.P1.rect)
        screen.blit(self.P2.image, self.P2.rect)
        for plat in self.list_plateformes:
            screen.blit(plat.image,plat.rect)

        # affichage barre d'hp P1
        bar_hpP1 = pg.Surface((400, 20))
        rect_hpP1 = pg.Rect((2,3), (round((self.P1.health / self.P1.max_health) * (bar_hpP1.get_width()-6)), 15))
        bar_hpP1.fill(pg.Color(0, 69, 11))
        bar_hpP1.fill(pg.Color(3, 233, 42), rect_hpP1)
        screen.blit(bar_hpP1, (10, screen.get_height()-60))

        # affichage barre d'hp P2
        bar_hpP2 = pg.Surface((400, 20))
        rect_hpP2 = pg.Rect((2, 3), (round((self.P2.health / self.P2.max_health) * (bar_hpP2.get_width() - 6)), 15))
        bar_hpP2.fill(pg.Color(0, 69, 11))
        bar_hpP2.fill(pg.Color(3, 233, 42), rect_hpP2)
        screen.blit(bar_hpP2, (screen.get_width()-bar_hpP2.get_width()-10, screen.get_height()-60))

        # affichage barre de mana P1
        bar_manaP1 = pg.Surface((400, 20))
        rect_manaP1 = pg.Rect((3, 2), (round((self.P1.mana / self.P1.mana_max) * (bar_manaP1.get_width() - 6)), 15))
        bar_manaP1.fill(pg.Color(0, 121, 254))
        bar_manaP1.fill(pg.Color(0, 254, 204), rect_manaP1)
        screen.blit(bar_manaP1, (10, screen.get_height()-30))

        # affichage barre de mana P2
        bar_manaP2 = pg.Surface((400, 20))
        rect_manaP2 = pg.Rect((3, 2), (round((self.P2.mana / self.P2.mana_max) * (bar_manaP2.get_width() - 6)), 15))
        bar_manaP2.fill(pg.Color(0, 121, 254))
        bar_manaP2.fill(pg.Color(0, 254, 204), rect_manaP2)
        screen.blit(bar_manaP2, (screen.get_width()-bar_manaP2.get_width()-10, screen.get_height()-30))

        # Verifier les touches pressées
        # P1
        self.P1.try_jump()
       #self.P1.try_block(self.P2)
        self.P1.try_stop_jump(self.list_plateformes)
        self.P1.try_fall(self.list_plateformes)
        if self.pressed.get(pg.K_d) and self.P1.rect.x < 1050 and self.P1.blocked_direction != 'Right':
            time.sleep(0.001)
            if self.P1.jump:
                self.P1.jump_direction = 'Right'
            elif self.P1.fall:
                self.P1.fall_direction = 'Right'
            else:
                self.P1.move_right()

        if self.pressed.get(pg.K_q) and self.P1.rect.x > -100 and self.P1.blocked_direction != 'Left':
            time.sleep(0.001)
            if self.P1.jump:
                self.P1.jump_direction = 'Left'
            elif self.P1.fall:
                self.P1.fall_direction = 'Left'
            else:
                self.P1.move_left()

        # P2
        self.P2.try_jump()
        #self.P2.try_block(self.P1)
        self.P2.try_stop_jump(self.list_plateformes)
        self.P2.try_fall(self.list_plateformes)
        if self.pressed.get(pg.K_RIGHT) and self.P2.rect.x < 1050 and self.P2.blocked_direction != 'Right':
            time.sleep(0.001)
            if self.P2.jump:
                self.P2.jump_direction = 'Right'
            elif self.P2.fall:
                self.P2.fall_direction = 'Right'
            else:
                self.P2.move_right()
        if self.pressed.get(pg.K_LEFT) and self.P2.rect.x > -100 and self.P2.blocked_direction != 'Left':
            time.sleep(0.001)
            if self.P2.jump:
                self.P2.jump_direction = 'Left'
            elif self.P2.fall:
                self.P2.fall_direction = 'Left'
            else:
                self.P2.move_left()

        # Appliquer les projectiles / séparation des projectiles de P1 et P2
        for proj in self.projs1:
            if proj.shot:
                screen.blit(proj.image, proj.rect)
                proj.coord_update()
                proj.try_damage(self.P2)

        for proj in self.projs2:
            if proj.shot:
                screen.blit(proj.image, proj.rect)
                proj.coord_update()
                proj.try_damage(self.P1)

    def mana_regen_in_game(self):
        self.P1.regen_mana()
        self.P2.regen_mana()




