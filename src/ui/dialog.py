
import pygame as pg
from src.game.support import *
import settings

class DialogBox:
    def __init__(self) -> None:
        self.x = 50
        self.y = 50
        self.text_index = 0
        self.letter_index = 0
        
        
        self.box = import_image(settings.IMAGES_DIR + "/dialog_box.png")
        self.box = pg.transform.scale(self.box, (settings.WINDOWS_WIDTH - 30, 130))
        self.font = pg.font.Font(settings.BASE_DIR + "/assets/fonts/KIN668.TTF", 35)
        
        self.reading = True
        
        
    def render(self, screen, textinput : str):
        self.textinput = [textinput]
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.textinput[self.text_index]):
                self.letter_index = self.letter_index
                
            
            screen.blit(self.box, (0, settings.WINDOWS_HEIGHT - 150))
            text = self.font.render(self.textinput[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (100, settings.WINDOWS_HEIGHT - 120))
            
    def nexttext(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index > len(self.textinput):
            self.reading = False