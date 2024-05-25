import os

DEV_MODE = True


FRAMERATE = 3000
WINDOWS_HEIGHT = 720
WINDOWS_WIDTH  = 1280

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images')

COEF_SCAL = 2
TILES_SIZE = 16

BACKGROUND_COLOR = (37,  19,  26)



if DEV_MODE == True:
    MUSIC_VOLUME= 0
else:
    MUSIC_VOLUME= 1
    



LAYER = {
    'ground':           1,
    'roads':            2,
    'decoration':       3,
    'objects':          4,
    'rocks':            5,
    'main':             6,
}


