# -*- coding: utf-8 -*-
import pygame, random, utils
from define import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *


class Player(pygame.sprite.Sprite):

    def __init__(self, screen: "pygame.Surface"):
        super().__init__()
        self.screen = screen
        self.games_played = 1
        self.reset()

    def reset(self):
        """Resets player's position, angle, health score and flag score. Sets skier status to True."""
        self.surface, self.rect = utils.load_png(DEFAULT_SKIER)
        self.rect.center = [X_DIM / 2, Y_DIM * 0.35]
        self.angle = self.flag_score = 0
        self.health_score = 100
        self.status = True

    def turn(self, direction):
        """Loads new image when skier turns and returns angle value"""
        pos = self.rect.center
        self.angle = self.angle + direction
        if self.angle < -2:
            self.angle = -2
        if self.angle > 2:
            self.angle = 2
        self.surface, self.rect = utils.load_png(SKIER_PNG_MAP[self.angle])
        self.rect.center = pos
        return self.angle

    def update(self, flag_group, obstacle_group):
        is_collision = False
        if self.status:
            is_collision = self.move(flag_group, obstacle_group)
        else:
            self.reset()
            self.games_played += 1
            self.screen = pygame.display.set_mode((X_DIM, Y_DIM))
        self.screen.blit(self.surface, self.rect)
        return is_collision

    def move(self, flag_group, obstacle_group):
        """Move the skier left and right based on turn method's return value"""
        self.rect.centerx = min(X_DIM, max(0, self.rect.centerx + self.angle))
        # Check for collisions & flags
        self.score(flag_group)
        return self.collision(obstacle_group)

    def score(self, flags):
        """Updates flag score"""
        col = pygame.sprite.spritecollide(self, flags, False)
        if col and self.health_score > 1:
            col[0].kill()
            self.flag_score += 1
            print("Caught a flag!")

    def collision(self, obstacle):
        """Checks for collision with trees and snowballs and update health score"""
        col = pygame.sprite.spritecollide(self, obstacle, False)
        if self.health_score <= 0 or not col:
            return False
        col[0].kill()
        self.health_score -= 10
        self.angle = 0
        print("Collision with obstacle!")
        # check status
        if self.health_score <= 0:
            self.status = False
        # crash
        pos = self.rect.center
        self.surface, self.rect = utils.load_png(SKIER_PNG_MAP["crash"])
        self.rect.center = pos
        self.screen.blit(self.surface, self.rect)
        return True


class Obstacles(pygame.sprite.Sprite):
    """This class is used to create trees and flags"""

    def __init__(self, image_file: "str", screen: "pygame.Surface"):
        super().__init__()
        self.surface, self.rect = utils.load_png(image_file)
        self.screen = screen
        self.rect.center = (random.choice(list(range(0, X_DIM + 1, 40))), Y_DIM + 10)

    def update(self):
        """Updates position of trees and flags"""
        self.rect.centery -= 1
        self.screen.blit(self.surface, self.rect)
        if self.rect.centery < 0:
            self.kill()
