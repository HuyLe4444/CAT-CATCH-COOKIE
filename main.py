import pygame
import pymunk
import pymunk.pygame_util
import math
import os
from os import listdir
from os.path import isfile, join
pygame.init()
pygame.mixer.init()

BALL_CLICKED = pygame.USEREVENT + 1
BALL_HIT = pygame.USEREVENT + 2

WIDTH, HEIGHT = 800, 800
CAT_WIDTH, CAT_HEIGHT = 32, 32
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAT_CATCH_COOKIE")

FPS = 120
BALL_RADIUS = 15
BALL_MASS = 6
BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'Cookie.png')).convert_alpha()
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (BALL_RADIUS * 2, BALL_RADIUS * 2))

CAT_MASS = 20
CAT_VEL = 3


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

space = pymunk.Space()
space.gravity = (0, 981)

def calculate_distance(p1, p2):
        return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
class Ball(pygame.sprite.Sprite):
    def ball_force(self, line):
        self.body.body_type = pymunk.Body.DYNAMIC
        angle = calculate_angle(*line)
        force = calculate_distance(*line) * 50
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        self.body.apply_impulse_at_local_point((-fx, -fy), (0, 0))


    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'Cookie.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = pos # (WIDTH/2, HEIGHT/2)
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.mass = BALL_MASS
        self.shape.color = (255, 0, 0, 100)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4
        space.add(self.body, self.shape)
        
    def destroy(self):
        space.remove(self.body, self.shape)
        self.kill()


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(width, height, direction=False):
    path = join("Assets")
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites


class Cat(pygame.sprite.Sprite):
    COLOR = (0, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets(32, 32, True)
    ANIMATION_DELAY = 15
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.hit = False
        self.hit_count = 0
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def get_hit(self):
        self.hit = True
        self.x_vel = 0
        self.y_vel = 0
        self.hit_count = 0
            
    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count // fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.x_vel = 0
            self.y_vel = 0
            self.hit = False
            self.hit_count = 0
        
    def update_sprite(self):
        sprite_sheet = "Idle"
        
        if self.hit:
            sprite_sheet = "Eat"
        elif self.x_vel != 0:
            sprite_sheet = "Run"
            
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        
    def draw(self, win):
        WIN.blit(self.sprite, (self.rect.x, self.rect.y))
        
        
def Cat_movement(cat, ball):
    cat.x_vel = 0
    
    if ball != None:
        if ball.body.position.x > cat.rect.x:
            cat.move_right(CAT_VEL)
        elif ball.body.position.x < cat.rect.x:
            cat.move_left(CAT_VEL)


def create_bounadries():
    rects = [
        [(WIDTH/2, HEIGHT - 10), (WIDTH, 20)],
        [(WIDTH/2, 10), (WIDTH, 20)],
        [(10, HEIGHT/2), (20, HEIGHT)],
        [(WIDTH - 10, HEIGHT/2), (20, HEIGHT)]
    ]
    
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)
        
def get_background(name):
    image = pygame.image.load(os.path.join("Assets", name)).convert()
    _, _, width, height = image.get_rect()
    titles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            titles.append(pos)
            
    return titles, image

def draw_window(cat, ball, draw_option, line, background, bg_image):
    for tile in background:
        WIN.blit(bg_image, tile)

    if ball:
        ball_hit_box = pygame.Rect(ball.body.position.x, ball.body.position.y, BALL_RADIUS, BALL_RADIUS)
        cat_hit_box = pygame.Rect(cat.rect.x, cat.rect.y, CAT_WIDTH, CAT_HEIGHT)
        if cat_hit_box.colliderect(ball_hit_box):
            pygame.event.post(pygame.event.Event(BALL_HIT))
    
    cat.draw(WIN)
    
    if line:
        pygame.draw.line(WIN, BLACK, line[0], line[1], 3)
    
    space.debug_draw(draw_option)
    
    if ball:
        WIN.blit(BALL_IMAGE, (ball.body.position.x - BALL_RADIUS, ball.body.position.y - BALL_RADIUS))
    #     if ball.body.position.colliderect(cat.rect):
    #         cat.get_hit()
    #         ball = None
    
    pygame.display.update()

    
def main():
    clock = pygame.time.Clock()
    run = True
    draw_option = pymunk.pygame_util.DrawOptions(WIN)
    background, bg_image = get_background("Pink.png")
        
    cat = Cat(WIDTH//2, HEIGHT - 50 - CAT_HEIGHT, CAT_WIDTH, CAT_HEIGHT)
    
    create_bounadries()
    
    pressed_pos = None
    ball = None
        
    while run:
        line = None
        
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                self_clicked = False
                
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = Ball(pressed_pos)
        
                elif pressed_pos:
                    ball.ball_force(line)
                    pressed_pos = None
                else:
                    ball.destroy()
                    ball = None
                    
            if event.type == BALL_HIT:
                if ball:
                    cat.get_hit()
                    ball.destroy()
                    ball = None
        

        cat.loop(FPS)
        Cat_movement(cat, ball)
        draw_window(cat, ball, draw_option, line, background, bg_image)
        space.step(1 / FPS)
        
if __name__ == "__main__":
    main()