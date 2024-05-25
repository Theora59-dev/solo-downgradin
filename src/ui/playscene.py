import pygame as pg , sys, os
import settings

sys.path.append(settings.BASE_DIR)

class Scene():
    def __init__(self):


        self.Afile = os.path.join(settings.BASE_DIR, "assets/sounds/intro.wav")
        self.Bfile = os.path.join(settings.BASE_DIR, "assets/sounds/KarolPiczak-LesChampsEtoiles.wav")
        pg.mixer.music.load(self.Afile)
        pg.mixer.music.load(self.Bfile)
        pg.mixer.music.queue(self.Bfile)
        pg.mixer.music.play(0, 0, 200)
        

# Jouer la musique
        

# Créer une fenêtre noire


        
    def run(self):
        pass
    
    
    