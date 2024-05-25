import pygame as pg
import sys
import os
from pytmx.util_pygame import *

from src.levels.level_sound import *
from game.support import *
from pygame.sprite import AbstractGroup

import settings
# sys.path.append(settings.BASE_DIR)

from src.entities.player import Player
from src.levels.sprite import *
from src.ui.dialog import *


class Level:
    
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.all_sprites = Camera_grp() 
        self.setup()
        self.music = play_music()
        self.dialog_box = DialogBox()
        self.text_display_time = 0
        self.getkey2 = 0


    def setup(self):
        self.tmx_data = load_pygame('assets/images/maps_tmx/MAP_Tiles.tmx')
               
        self.draw_tiles_layer("Floor", "ground")
        self.draw_tiles_layer("Decoration","decoration")
        # self.draw_tiles_layer("Objs", "objects")
        # self.draw_tiles_layer("House_bottom", "house_bottom")
        # self.draw_tiles_layer("Roads", "roads")
        
        path = os.path.join(settings.IMAGES_DIR, "Fantasy Tileset/Animations/water/anim_base/")
        water_frames = import_folder(path)
        
        for obj in self.tmx_data.get_layer_by_name('Objs'):
             Objects((obj.x * settings.COEF_SCAL , obj.y * settings.COEF_SCAL), upscale_img(obj.image), self.all_sprites, obj.name)
            
            
            
            
            
            
        # for x, y, surf in self.tmx_data.get_layer_by_name('Water').tiles():
        #     Water((x * settings.TILES_SIZE * settings.COEF_SCAL , y * settings.TILES_SIZE * settings.COEF_SCAL), water_frames, self.all_sprites)       
        
        # for obj in self.tmx_data.get_layer_by_name('All_rocks'):
        #     Rocks((obj.x * settings.COEF_SCAL , obj.y * settings.COEF_SCAL), upscale_img(obj.image), self.all_sprites, obj.name)
             
        
        # Generic(pos    = (0, 0),
        #         surf   = import_image(os.path.join(settings.BASE_DIR, "assets/images/maps_tmx/tiles.png")),
                
        #         groups = self.all_sprites,
        #         z = settings.LAYER['ground']
        #         )
        
        
        self.walls = []
        self.first_locked_doors = []
        self.first_open_door = []
        self.chest = []
        self.pass_first_locked_door = []
        self.chandelier = []
        self.finished = []
        self.have2key = 0
        self.full_pass = 0
        self.finished_bool : bool = 0
        self.havekey : bool = 0
        
        
        
        xpos, ypos = 488 * settings.COEF_SCAL, 483 *settings.COEF_SCAL
        self.player = Player((xpos, ypos), self.all_sprites)
        self.teleport_player("1_spawnpoint")
        
       
    def run(self, dt):
        
        
        self.text_display_time -= dt
        self.all_sprites.customize_draw(self.player)
        self.player.saveloc()
        self.all_sprites.update(dt)
        self.collision_detect()
        
        if self.text_display_time > 0 and self.getkey2 == 1:
            self.dialog_box.render(self.screen, "Vous avez obtenu la 2ème clef !!")
        else:
            self.getkey2 = 0
            
            
            


        
        
    
   
        
   # Autres fonctions utiles
   
   
   
    def collision_detect(self):
        
        
        for sprite in self.all_sprites.sprites():
            try:
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()
                elif sprite.feet.collidelist(self.first_locked_doors) >-1 and self.full_pass == 0:
                    self.dialog_box.render(self.screen, "Cette porte ne semble pas s'ouvrir de ce coté...")
                    sprite.move_back()
                
                    
                    
                    
                if sprite.feet.collidelist(self.pass_first_locked_door) > -1 and self.full_pass == 0:
                    printgreen("Collision avec pass_first_locked_door")
                    self.teleport_player("tp_locked_door")
                    
                if sprite.feet.collidelist(self.chandelier) > -1 and self.full_pass == 0 and self.have2key == 0:
                    printgreen("Collision avec le chandelier, vous avez recu la 2eme clef !!")
                    self.dialog_box.render(self.screen, "Vous avez obtenu la 2ème clef !!")
                    self.have2key = 1
                    self.getkey2 = 1
                    self.text_display_time = 5 
                    
                    
                if sprite.feet.collidelist(self.finished) > -1 and self.full_pass == 0 and self.have2key == 1:
                    printgreen("Vous avez finis le jeux, félicitation !!")
                    self.dialog_box.render(self.screen, "Vous avez finis le jeu, félicitation !")
                    self.finished_bool = 1
                    
                
                if sprite.feet.collidelist(self.first_open_door) > -1 and self.full_pass == 0 and self.havekey == 1:
                    self.teleport_player("first_door_spawnpoint")
                
                
                if sprite.feet.collidelist(self.first_open_door) > -1 and self.full_pass == 0:
                    self.dialog_box.render(self.screen, "Cette porte à l'air étrange...")
                    sprite.move_back()
                    
                    
                    
                if sprite.feet.collidelist(self.chest) > -1 and self.full_pass == 0 :
                    self.dialog_box.render(self.screen, "Vous avez obtenu la clef !!")
                    self.havekey = 1
                    sprite.move_back()
            except:
                pass
            

        
        
        self.event()
        
                
       
   

    def draw_tiles_layer(self, tiled_tilesname, settings_layername):
        for x, y, surf in self.tmx_data.get_layer_by_name(tiled_tilesname).tiles():
            
            img_width, img_height = surf.get_size()
            new_img_width = settings.COEF_SCAL * img_width
            new_img_height = settings.COEF_SCAL * img_height
            surf = pg.transform.scale(surf, (new_img_width, new_img_height))
            Generic((x * settings.TILES_SIZE * settings.COEF_SCAL , y * settings.TILES_SIZE * settings.COEF_SCAL), surf ,  self.all_sprites, settings.LAYER[settings_layername])
            
      
    def event(self):
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "first_locked_door":
                self.first_locked_doors.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "first_open_door":
                self.first_open_door.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "chest":
                self.chest.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "pass_first_locked_door":
                self.pass_first_locked_door.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "chandelier":
                self.chandelier.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))
            if obj.type == "game_finished":
                self.finished.append(pg.Rect((obj.x* settings.COEF_SCAL) + 50, (obj.y * settings.COEF_SCAL) + 50, obj.width * settings.COEF_SCAL, obj.height * settings.COEF_SCAL,))

            
            
            
            
            
                
                
                
    def teleport_player(self, name : str):
        point = self.get_object(name)
        self.player.pos[0] = point.x * settings.COEF_SCAL
        self.player.pos[1] = point.y * settings.COEF_SCAL
        self.player.saveloc()
        
    def get_object(self, name):
        return self.tmx_data.get_object_by_name(name)
      
      
      
      
      
      
        
class Camera_grp(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2()
        self.camera = 0
        
    def customize_draw(self, player):
        
        self.offset.x = player.rect.centerx - settings.WINDOWS_WIDTH  /2
        self.offset.y = player.rect.centery - settings.WINDOWS_HEIGHT /2
        
        for layer in settings.LAYER.values():
            for sprite in sorted(self.sprites(), key=lambda sprite : sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect  = sprite.rect.copy()
                    offset_rect.center -= self.offset 
                    self.display_surface.blit(sprite.image, offset_rect)






