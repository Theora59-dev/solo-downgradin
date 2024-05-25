import pygame as pg
from pygame.locals import *
import os, sys, time
import cmath
import settings
sys.path.append(settings.BASE_DIR)
from src.levels.level import Level
from src.ui.dialog import *
from array import array
import moderngl
import struct


class Window():

    def __init__(self):
        
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        
        
        
        
        #self.display = pg.display.set_mode((settings.WINDOWS_WIDTH , settings.WINDOWS_HEIGHT))
        self.screen = pg.display.set_mode((settings.WINDOWS_WIDTH , settings.WINDOWS_HEIGHT), pg.OPENGL|pg.DOUBLEBUF)
        self.display = pg.Surface((settings.WINDOWS_WIDTH , settings.WINDOWS_HEIGHT))

        
  
        
        pg.display.set_caption('Solo Downgrading')
        self.clock = pg.time.Clock()
        self.level = Level()
        self.dialog_box = DialogBox()

        self.game_loop = True
        
        
        
        
        self.playlist = [os.path.join(settings.BASE_DIR, "assets/sounds/intro.wav"), 
                         os.path.join(settings.BASE_DIR, "assets/sounds/KarolPiczak-LesChampsEtoiles.wav")]
        pg.mixer.music.load(self.playlist.pop(0))
        
        for song in self.playlist:
            pg.mixer.music.queue(song)
            
        pg.mixer.music.set_endevent(pg.USEREVENT)
        pg.mixer.music.play()
        pg.mixer.music.set_volume(settings.MUSIC_VOLUME)

            



        
        
        # joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
        
        
        
        
        
    def run(self):
        font = pg.font.Font(None,  40)  
        analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }   
        
        
        start_time = pg.time.get_ticks()
        transition_time = 23000                     #en ms
        if settings.DEV_MODE == True:
            transition_time = 0
        self.image = pg.image.load(os.path.join(settings.BASE_DIR, "assets/images/narrator-icon-0.png"))
        
        
        ctx = moderngl.create_context()
        quad_buffer = ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        

        vert_shader = '''
            #version 330 core

            in vec2 vert;
            in vec2 texcoord;
            out vec2 uvs;

            void main() {
                uvs = texcoord;
                gl_Position = vec4(vert, 0.0, 1.0);
            }
            '''

        Afrag_shader = '''
            #version 330 core

            uniform sampler2D tex;
            uniform float time;
            uniform vec2 resolution;

            in vec2 uvs;
            out vec4 f_color;

            float handleCoord(float c, float dc) {
                float result = 0.0;
                float min = c - 0.5 * dc - 0.5;
                float max = c + 0.5 * dc - 0.5;
                float floorMin = floor(min);
                float floorMax = floor(max);

                if (floorMin == floorMax) {
                    min = 0.0;
                }

                result = (floorMax - 1.0) + (floorMax + min) / dc;
                return result;
            }

            void main() {
                float tile_factor = -1;

                vec2 atlasSize = vec2(1920/tile_factor, 1080/tile_factor); // Taille de la texture
                vec2 uv = uvs * atlasSize; // Coordonnées de texture en espace texel
                vec2 duv = 1.0 / atlasSize; // Taille d'un texel

                uv = vec2(handleCoord(uv.x, duv.x), handleCoord(uv.y, duv.y));
                f_color = texture(tex, uv / atlasSize);
            }
            '''
            
        frag_shader = '''
            #version 330 core

            uniform sampler2D tex;
            uniform float time;
            uniform vec2 resolution;

            in vec2 uvs;
            out vec4 f_color;

            void main() {
                float x = time;
                float zoom = 0.6 + 0.4 * sin(x*0.02);
                
                vec4 color = texture(tex, uvs);
                                
                color.r *= zoom;
                color.g *= zoom;
                color.b *= zoom;

                f_color = color;

            }
            '''
        



        program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])
        

        def surf_to_texture(surf):
            tex = ctx.texture(surf.get_size(), 4)
            tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
            tex.swizzle = 'BGRA'
            tex.write(surf.get_view('0'))
            return tex
        
        direction = [0, 0]
        
        
        
        
        
        
        
        
        
        
        
        


        
        t = 0
        while self.game_loop == True:
            dt = self.clock.tick(settings.FRAMERATE) / 1000
            t += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_loop = False
                    pg.display.quit()
                    pg.quit()
                    sys.exit()
                    break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        #self.dialog_box.nexttext()
                        pass

                                    
                            # if analog_keys[4] > 0:  # Left trigger
                            #     pass
                            # if analog_keys[5] > 0:  # Right Trigger
                            #     pass
                    
            
                

                    
            
            ###################################################
            ################# CODE DE JEU ICI #################
            ###################################################
            
            
            self.screen.fill(settings.BACKGROUND_COLOR)
            time_elapsed = pg.time.get_ticks() - start_time
            if time_elapsed > transition_time:
                
                self.level.run(dt)
                
                
                
                get_fps = self.clock.get_fps()
                fps_text = font.render('FPS: {:.2f}'.format(get_fps), True, (255,  255,  255))
                self.screen.blit(fps_text, (settings.WINDOWS_WIDTH - 170, 10 ))
                
                
                
                
                
                
                
                
                frame_tex = surf_to_texture(self.screen)     #- NE PAS TOUCHER
                frame_tex.use(0)
                program['tex'] = 0
                program['time'] = t
                # print(0.5 + 0.5 * cmath.sin(t * 0.01))
                render_object.render(mode=moderngl.TRIANGLE_STRIP)            
                frame_tex.release()
                

                

                
                
                if self.level.finished_bool == 1:
                    pg.display.quit()
                    break
            else:
                

                
                
                
                
                
                
                
                
                
                
                screen_rect = self.screen.get_rect() 
                screen_center = screen_rect.center 
                image_rect = self.image.get_rect()
                image_rect.center = screen_center 
                self.display.blit(self.image, image_rect)


                   
            
            
                
            
            



            
            ####################################################
            ####################################################
            ####################################################     
            
            
            pg.display.flip()



if __name__ == 'ui.game':
    
    
    game = Window()
    game.run()
    
    

