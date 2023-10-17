import pygame
import os

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("gif", "frame_0.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("gif", "frame_1.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("gif", "frame_2.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("gif", "frame_3.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("gif", "frame_4.png")).convert_alpha())
        self.curr_sprite = 0
        self.image = self.sprites[self.curr_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def update(self):
        if self.is_animating == True:
            self.curr_sprite += 0.7
            
            if self.curr_sprite >= len(self.sprites):
                self.curr_sprite = 0
                self.is_animating = False
                
            self.image = self.sprites[int(self.curr_sprite)]
        
    def animate(self): 
        self.is_animating = True