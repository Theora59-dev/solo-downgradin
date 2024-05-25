import pygame as pg
import settings
from pytmx.util_pygame import *

from settings import LAYER



class Generic(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = settings.LAYER["main"]):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = None
        # self.collision_mask = pg.mask.from_surface(self.image)

        
        
        
class Water(Generic):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frames_index = 0
        
        
        
        super().__init__(pos=pos, surf=self.frames[self.frames_index], groups=groups, z=settings.LAYER['water'])
    
    def animate(self, dt):
        self.frames_index += 5*dt
        
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]
        
    def update(self, dt):
        self.animate(dt)
        
        
class Rocks(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        
        
class Objects(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)


     
class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
 