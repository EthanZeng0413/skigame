# -*- coding: utf-8 -*-
import pygame, sys, utils, skiing_obj
from define import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *


class SkiingGame(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.font = pygame.font.SysFont(("bauhaus93"), 35)
        self.smallfont = pygame.font.SysFont(("bauhaus93"), 25)
        self.surface, self.rect = utils.load_png(BACKGROUND_IMAGE)
        self.speed = -1
        self.pos_list = [0, self.rect.height]
        self.display_width = X_DIM
        self.display_height = Y_DIM
        pygame.display.set_caption("滑雪大赛!  Tips: 使用左右方向键移动")

    def playmusic(self):
        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.play(-1)

    def draw_floor(self):
        """Displays game title and scrolls background image"""
        for i in range(len(self.pos_list)):
            self.pos_list[i] += self.speed
            self.screen.blit(self.surface, (0, self.pos_list[i]))

            if self.pos_list[i] < -self.rect.height:
                self.pos_list[i] = self.rect.height - 1


class Engine:
    """The Engine class runs the game by calling the 'playgame' method."""

    def __init__(self, screen, skier: "skiing_obj.Player"):
        self.font = pygame.font.SysFont(("bauhaus93"), 35)
        self.smallfont = pygame.font.SysFont(("bauhaus93"), 25)
        self.screen = screen
        self.skier = skier
        print("Game created")

    def update_score_panel(self):
        """Displays health score and flag score"""
        skier = self.skier
        if skier.status:
            health_score_surface = self.font.render(f"HEALTH SCORE: {int(skier.health_score)}", True, (0, 0, 0))
            health_score_rect = health_score_surface.get_rect(center=(X_DIM / 2, Y_DIM * 0.05))
            self.screen.blit(health_score_surface, health_score_rect)
            flag_score_surface = self.font.render(f"FLAG SCORE: {int(skier.flag_score)}", True, (0, 0, 0))
            flag_score_rect = flag_score_surface.get_rect(center=(X_DIM / 2, Y_DIM * 0.1))
            self.screen.blit(flag_score_surface, flag_score_rect)
        else:
            good_score_surface = self.font.render(f"YOU SCORED {int(skier.flag_score)} FLAGS!", True, (0, 0, 0))
            self.screen.blit(good_score_surface, good_score_surface.get_rect(center=(X_DIM / 2, Y_DIM * 0.2)))
            print(f"Flag score is: {skier.flag_score}")
            print(f"Total games played is: {skier.games_played}")

    def playgame(self):
        clock = pygame.time.Clock()

        # Set background and clock variables
        game = SkiingGame(self.screen)
        game.playmusic()

        ### Declare sprite container groups
        tree_and_flag_group = pygame.sprite.Group()
        obstacle_group = pygame.sprite.Group()
        tree_group = pygame.sprite.Group()
        flag_group = pygame.sprite.Group()

        ### Define Pygame userevents to make trees, flags and snowballs at specified time intervals
        pygame.time.set_timer(CREATETREE_EVENT, CREATETREE_TIMER_DELAY)
        pygame.time.set_timer(CREATEFLAG_EVENT, CREATEFLAG_TIMER_DELAY)

        skier = self.skier
        while True:
            clock.tick(FPS)
            screen.fill(BACKGROUND_COLOR)
            game.draw_floor()

            # Monitor user-input and create trees/flags/snowballs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # checks if a key is pressed
                    if event.key == pygame.K_LEFT:
                        skier.angle = skier.turn(-1)
                    elif event.key == pygame.K_RIGHT:
                        skier.angle = skier.turn(1)
                    elif event.key == pygame.K_RETURN:
                        self.playgame()

                if event.type == CREATETREE_EVENT:
                    tree_group.add(skiing_obj.Obstacles(SKIER_PNG_MAP["tree"], self.screen))
                if event.type == CREATEFLAG_EVENT:
                    flag_group.add(skiing_obj.Obstacles(SKIER_PNG_MAP["flag"], self.screen))

                # Update sprite groups
                tree_and_flag_group.add(tree_group)
                tree_and_flag_group.add(flag_group)
                obstacle_group.add(tree_group)

            # update status
            is_collision = skier.update(flag_group, obstacle_group)
            tree_and_flag_group.update()
            self.update_score_panel()
            pygame.display.flip()
            if not self.skier.status and is_collision:
                pygame.time.delay(FINAL_DELAY)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((int(X_DIM), int(Y_DIM * 1.3)))
    icon, _ = utils.load_png(ICON_IMAGE)
    pygame.display.set_icon(icon)
    # START GAME
    Engine(screen, skiing_obj.Player(screen)).playgame()
