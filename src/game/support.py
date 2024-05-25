from os import walk
import pygame as pg
import settings
import colorama


def import_image(img_path):
        sprite = pg.image.load(img_path).convert_alpha()
        img_width, img_height = sprite.get_size()
        new_img_width = settings.COEF_SCAL * img_width
        new_img_height = settings.COEF_SCAL * img_height
        sprite = pg.transform.scale(sprite, (new_img_width, new_img_height))
        return sprite
    
    
def upscale_img(sprite):
    img_width, img_height = sprite.get_size()
    img_width = img_width * settings.COEF_SCAL
    img_height = img_height * settings.COEF_SCAL
    
    new_img_width = img_width 
    new_img_height = img_height 
    sprite = pg.transform.scale(sprite, (new_img_width, new_img_height))
    return sprite
    
    

def import_folder(path):
    surface_list = []
    
    for folder_name, sub_folder, img_file in walk(path):
        for image in img_file:
            full_path = path + '/'+ image
            image_surface = import_image(full_path)
            surface_list.append(image_surface)
    
    return surface_list

def printred(text: str):
    print(colorama.Fore.RED, text, colorama.Fore.RESET)

def printgreen(text: str):
    print(colorama.Fore.GREEN, text, colorama.Fore.RESET)