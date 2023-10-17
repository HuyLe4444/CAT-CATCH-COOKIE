import pygame
import pymunk
import pymunk.pygame_util
import math
import time
import tkinter as tk
from tkinter import Scrollbar, Text
from gif import Grass
import os
from os import listdir
from os.path import isfile, join
from button import Button

# Initialize pygame and audio
pygame.init()
pygame.mixer.init()

# Define custom events
BALL_CLICKED = pygame.USEREVENT + 1
BALL_HIT = pygame.USEREVENT + 2
BUTTON_CLICKED = pygame.USEREVENT + 3

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
CAT_WIDTH, CAT_HEIGHT = 32, 32
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAT-CATCH-COOKIE")

# Frames per second
FPS = 120

# Ball properties
BALL_RADIUS = 15
BALL_MASS = 6
BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'Cookie.png')).convert_alpha()
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (BALL_RADIUS * 2, BALL_RADIUS * 2))

# Background Image
BACKDROP = pygame.transform.scale(pygame.image.load(os.path.join('Pomodoro_Assets', 'backdrop.png')), (WIDTH, HEIGHT))

# Cat properties
CAT_MASS = 20
CAT_VEL = 3

# Button image
WHITE_BUTTON = pygame.image.load("Pomodoro_assets/button.png")

# Load fonts
FONT = pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 80)
SHOP_FONT = pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 30)
COIN_FONT = pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20)

# Timer text and position
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(1000, 150))

# Create buttons
START_STOP_BUTTON = Button(WHITE_BUTTON, (1000, 220), 170, 60, "START", 
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
POMODORO_BUTTON = Button(None, (860, 100), 120, 30, "Pomodoro", 
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (985, 100), 120, 30, "Short Break", 
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (1110, 100), 120, 30, "Long Break", 
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
DRINK_WATER_BUTTON = Button(WHITE_BUTTON, (1100, 650), 80, 40, "DRINK",
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
TOUCH_GRASS_BUTTON = Button(WHITE_BUTTON, (1100, 750), 80, 40, "TOUCH",
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
SHOP_BUTTON = Button(WHITE_BUTTON, (1000, 470), 170, 60, "Shop",
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
BUY_BUTTON = Button(WHITE_BUTTON, (-1000, -1000), 80, 40, "BUY",
                    pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

# Time durations in seconds
POMODORO_LENGTH = 1500 # 1500 secs / 25 mins
SHORT_BREAK_LENGTH = 300 # 300 secs / 5 mins
LONG_BREAK_LENGTH = 900 # 900 secs / 15 mins

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 215, 0)
GOLD = (212, 175, 55)

# Create a physics space
space = pymunk.Space()
space.gravity = (0, 981)

# List to store buy buttons
buy_buttons = []

# Default color for the cat
chosen_color = "black"

# moving_sprites = pygame.sprite.Group()
# grass = Grass(10, 10)
# moving_sprites.add(grass)

# grass = []
# grass.append(pygame.image.load(os.path.join("gif", "frame_0.png")).convert_alpha())
# grass.append(pygame.image.load(os.path.join("gif", "frame_1.png")).convert_alpha())
# grass.append(pygame.image.load(os.path.join("gif", "frame_2.png")).convert_alpha())
# grass.append(pygame.image.load(os.path.join("gif", "frame_3.png")).convert_alpha())
# grass.append(pygame.image.load(os.path.join("gif", "frame_4.png")).convert_alpha())

# Function to calculate distance between two points
def calculate_distance(p1, p2):
        return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

# Function to calculate the angle between two points
def calculate_angle(p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
# Ball class for game objects
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
        
# class BuyButton(Button):

#     def __init__(self, surface=None, pos=None, width=None, height=None, text_input=None, font=None, base_color=None, hovering_color=None, dress=None):
#         super().__init__(surface, pos, width, height, text_input, font, base_color, hovering_color)
#         self.dress = dress

# Define a class to represent a shop that sells different dress colors
class Shop:
    def __init__(self):
        # Initialize a dictionary with dress colors and their corresponding prices
        self.dresses = {
            "black": 3600,
            "blue": 3600,
            "brown": 3600,
            "red": 3600,
            "radioactive": 7200,
            "gameboy": 7200,
            "sealpoint": 7200
        }
        
    # Method to draw the shop interface on the screen
    def draw(self, screen):
        # Fill the screen with a background color
        screen.fill((52,78,91))
        
        # Define the initial vertical position for dress items
        y = 100
    
        # Loop through dress colors and their prices to display them in the shop
        for dress, price in self.dresses.items():
            dress_text = dress + ": " + str(price)
            # BUY_BUTTON = Button(WHITE_BUTTON, (500, y + 15), 80, 40, "BUY",
            #         pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
            # BUY_BUTTON.update(WIN)
            # BUY_BUTTON.change_color(pygame.mouse.get_pos())
            
            # Render text to surface
            dress_surf = SHOP_FONT.render(dress_text, True, BLACK)

            # Blit the surface
            screen.blit(dress_surf, (100, y))  
            
            y += 80 # Increase the vertical position for the next dress item
    
    # Method to draw "BUY" buttons for each dress item in the shop
    def draw_btn(self, screen):

        y = 100
        for dress in self.dresses:
            # Create "BUY" buttons for each dress item
            buy_buttons.append(Button(WHITE_BUTTON, (500, y + 15), 80, 40, "BUY",
                            pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034", dress=dress))
            
            
            y += 80
    
    # Method to process a dress purchase
    def buy(self, dress, COIN):
        if COIN >= self.dresses[dress]:
            print("Bought", dress)
            # COIN -= self.dresses[dress]
            chosen_color = dress # Assign the purchased dress color
        else:
            print("Not enough coins!")


# Function to flip sprites horizontally
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# Function to load sprite sheets for cat animations
def load_sprite_sheets(width, height, color, direction=False):
    path = join("Assets", color) # Define the path to the folder containing sprites for a specific dress color
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
            # Store the sprites for both left and right directions in the dictionary
            all_sprites[image.replace(".png", "") + "_right"] = flip(sprites)
            all_sprites[image.replace(".png", "") + "_left"] = (sprites)
        else:
            # Store the sprites for a single direction in the dictionary
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites

# Define a class to represent a cat character with various animations
class Cat(pygame.sprite.Sprite):
    # Class constants and properties for cat animations
    COLOR = (0, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets(32, 32, chosen_color, True)
    ANIMATION_DELAY = 15
    
    # Method to change the cat's dress color
    def change_dress(self, color):
        self.SPRITES = load_sprite_sheets(32, 32, color, True)
        self.update_sprite()
    
    # Initialize the cat with its initial properties
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
        
    # Method to move the cat
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    # Method to move the cat to the left
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    # Method to move the cat to the right
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    # Method to handle when the cat gets hit
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
    
    # Method to update the cat's animation frame
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
        
    # Method to draw the cat on the screen
    def draw(self, win):
        WIN.blit(self.sprite, (self.rect.x, self.rect.y))
        
# Function to control cat movement based on the ball's position
def Cat_movement(cat, ball):
    cat.x_vel = 0
    
    if ball != None:
        if ball.body.position.x > cat.rect.x:
            cat.move_right(CAT_VEL)
        elif ball.body.position.x < cat.rect.x:
            cat.move_left(CAT_VEL)

# Function to create boundaries for the game world
def create_bounadries():
    rects = [
        [(1200/2, 800 - 10), (1200, 20)],
        [(800/2, 10), (1600, 20)],
        [(10, 800/2), (20, 800)],
        [(800 - 10, 800/2), (20, 800)],
        [(1200 - 10, 1200/2), (800, 20)],
        [(1200 - 10, 1200/2), (20, 1200)]
    ]
    
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)
        
# Function to get the background image for the game
def get_background(name):
    image = pygame.image.load(os.path.join("Assets", name)).convert()
    _, _, width, height = image.get_rect()
    titles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            titles.append(pos)
            
    return titles, image

# Function to draw the game window
def draw_window(cat, ball, draw_option, line, background, bg_image, current_seconds, COIN, reminder_drink_text, reminder_touch_text, current_screen, shop_window, dress_own, is_animation):    
    # for tile in background:
    #     WIN.blit(bg_image, tile)
    if current_screen == "main":
        WIN.fill((52,78,91)) # Fill the window with a background color
        
        if ball:
            ball_hit_box = pygame.Rect(ball.body.position.x, ball.body.position.y, BALL_RADIUS, BALL_RADIUS)
            cat_hit_box = pygame.Rect(cat.rect.x, cat.rect.y, CAT_WIDTH, CAT_HEIGHT)
            if cat_hit_box.colliderect(ball_hit_box):
                pygame.event.post(pygame.event.Event(BALL_HIT))
                
        # WIN.blit(BACKDROP, (780, 260))
        # WIN.blit(BACKDROP, (780, 10))
        
        cat.draw(WIN)
        
        if line:
            pygame.draw.line(WIN, BLACK, line[0], line[1], 3)
        
        space.debug_draw(draw_option) # Draw physics shapes
        
        if ball:
            WIN.blit(BALL_IMAGE, (ball.body.position.x - BALL_RADIUS, ball.body.position.y - BALL_RADIUS))
            
        # Update and draw buttons
        START_STOP_BUTTON.update(WIN)
        START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
        POMODORO_BUTTON.update(WIN)
        POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
        SHORT_BREAK_BUTTON.update(WIN)
        SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
        LONG_BREAK_BUTTON.update(WIN)
        LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
        DRINK_WATER_BUTTON.update(WIN)
        DRINK_WATER_BUTTON.change_color(pygame.mouse.get_pos())
        TOUCH_GRASS_BUTTON.update(WIN)
        TOUCH_GRASS_BUTTON.change_color(pygame.mouse.get_pos())
        SHOP_BUTTON.update(WIN)
        SHOP_BUTTON.change_color(pygame.mouse.get_pos())
        
        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
        timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        WIN.blit(timer_text, timer_text_rect)
        
        text = COIN_FONT.render("COIN: " + str(COIN), 1, WHITE)
        WIN.blit(text, (955, 400))
            
        WIN.blit(reminder_drink_text, (920, 635))
        WIN.blit(reminder_touch_text, (920, 737))
        
        # if is_animation:
        #     for image in grass:
        #         WIN.blit(image, (850, 710))
                
                
        #     is_animation = False
        
        # moving_sprites.draw(WIN)
        # moving_sprites.update()
        
    elif current_screen == "shop":
        shop_window.draw(WIN)
        shop_window.draw_btn(WIN)
        for button in buy_buttons:
            if button not in dress_own:
                button.update(WIN)
                button.change_color(pygame.mouse.get_pos())
                
    
                
    
    pygame.display.update()

# Main game loop
def main():
    clock = pygame.time.Clock()
    run = True
    is_animation = False
    current_screen = "main"
    shop_window = Shop()
    draw_option = pymunk.pygame_util.DrawOptions(WIN)
    background, bg_image = get_background("Pink.png")
    global chosen_color
    
    coin_inc = True
    COIN = 100000
    
    current_seconds = POMODORO_LENGTH
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    started = False
        
    cat = Cat(WIDTH//2, HEIGHT - 40 - CAT_HEIGHT, CAT_WIDTH, CAT_HEIGHT)
    
    dress_own = []
    
    create_bounadries()
    
    pressed_pos = None
    ball = None
    
    reminder_drink_text = COIN_FONT.render("Drink Water", False, WHITE)
    reminder_touch_text = COIN_FONT.render("Touch Grass", False, WHITE)
        
    while run:
        line = None
            
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    current_screen = "main"
            
            if pygame.mouse.get_pos() < (800, 800):
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
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "shop":
                    for button in buy_buttons:
                        if button.check_for_input(pygame.mouse.get_pos()):
                            if button.dress not in dress_own:
                                COIN -= shop_window.dresses[button.dress]
                                chosen_color = button.dress
                                cat.change_dress(chosen_color)
                                shop_window.buy(button.dress, COIN)
                                dress_own.append(button.dress)
                                buy_buttons.remove(button)
                                    
                if SHOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_screen = "shop"
                if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    if started:
                        started = False
                    else:
                        started = True
                # if TOUCH_GRASS_BUTTON.check_for_input(pygame.mouse.get_pos()):
                #     is_animation = True
                    
                if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = POMODORO_LENGTH
                    started = False
                    coin_inc = True
                if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = SHORT_BREAK_LENGTH
                    started = False
                    coin_inc = False
                if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = LONG_BREAK_LENGTH
                    started = False
                    coin_inc = False
                if started:
                    START_STOP_BUTTON.text_input = "STOP"
                    START_STOP_BUTTON.text = pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20).render(
                                            START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
                else:
                    START_STOP_BUTTON.text_input = "START"
                    START_STOP_BUTTON.text = pygame.font.Font("Pomodoro_assets/ArialRoundedMTBold.ttf", 20).render(
                                            START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
            if event.type == pygame.USEREVENT and started:
                current_seconds -= 1
                if coin_inc:
                    COIN += 1
        
        # print(chosen_color)
        cat.loop(FPS)
        Cat_movement(cat, ball)
        draw_window(cat, ball, draw_option, line, background, bg_image, current_seconds, COIN, reminder_drink_text, reminder_touch_text, current_screen, shop_window, dress_own, is_animation)
        space.step(1 / FPS)
        
    
        
if __name__ == "__main__":
    main()