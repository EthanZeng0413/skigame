# -*- coding: utf-8 -*-
import os, pygame
from define import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

def load_png(name) -> "Tuple[pygame.Surface, pygame.Rect]":
    """
    Load image and return image object
    """
    fullname = os.path.join("res", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()
