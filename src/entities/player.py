import pygame as pg
import sys, os

import settings
sys.path.append(settings.BASE_DIR)
from game.support import * 
import controls


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group):
        
        super().__init__(group)
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.all_sprites = group
              

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        

        
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = 18.7* settings.TILES_SIZE
        self.attack_pulse = False
        self.attack_status = False
        self.z = settings.LAYER['main']
        self.player_rect = pg.Surface.get_rect(self.image)
        self.feet = pg.Rect(0, -50, self.player_rect.width * 0.7, self.player_rect.height * 0.3)
        self.old_position = self.pos.copy()
        
        
        

        
        
        
        
    def input(self):
        
        input_keys = pg.key.get_pressed()
        
        if (input_keys[pg.K_z] and input_keys[pg.K_s]):
                self.direction.y = 0
                
        elif (input_keys[pg.K_q] and input_keys[pg.K_d]):
                self.direction.x = 0
        else:
            
            if input_keys[pg.K_z]:
                self.direction.y = -1
                self.status = 'up_run'
            elif input_keys[pg.K_s]:
                self.direction.y = 1
                self.status = 'down_run'
            else:
                self.direction.y = 0
                
            if input_keys[pg.K_q]:
                self.direction.x = -1
                self.status = 'left_run'
            elif input_keys[pg.K_d]:
                self.direction.x = 1
                self.status = 'right_run'
            else:
                self.direction.x = 0
                
        if pg.mouse.get_pressed()[0]:
            self.attack_pulse = True
        else:
            self.attack_pulse = False
            
        
        
            
        
            
            
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attack_pulse == 1:
            self.status = self.status.split('_')[0] + '_attack'
            
            
    def saveloc(self): 
        self.old_position = self.pos.copy()
                  
    
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x - 10

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y - 5
        

        
        
    def move_back(self):
        self.pos = self.old_position
        self.player_rect.topleft = self.pos
        self.feet.midbottom = self.player_rect.midbottom()
    
    
      
    def import_assets(self):
        self.animations = {'up_run' : [], 'down_run' : [], 'right_run' : [], 'left_run' : [],
                           'up_idle' : [], 'down_idle' : [], 'right_idle' : [], 'left_idle' : [],
                           'up_attack' : [], 'down_attack' : [], 'right_attack' : [], 'left_attack' : [],
                           'up_death' : [], 'down_death' : [], 'right_death' : [], 'left_death' : []
                           }
        
        for animation in self.animations.keys():
            path = os.path.join(settings.IMAGES_DIR, "RPG_Hero/") + animation
            self.animations[animation] = import_folder(path)
   
   
    def animate(self, dt):
        if "idle" in self.status:
            self.frame_index += 3 * dt
        elif "attack" in self.status:
            self.frame_index += 10 * dt
            self.attack_pulse = False
        else:
            self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        img_width, img_height = self.image.get_size()
        coef = 1.3
        new_img_width = coef * img_width
        new_img_height = coef * img_height
        self.image = pg.transform.scale(self.image, (new_img_width, new_img_height))
        
         
        

        
    
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.pos[0] = round(self.pos[0])
        self.pos[1] = round(self.pos[1])
        self.player_rect.topleft = self.pos
        self.feet.midbottom = self.player_rect.midbottom
        
 
 