# Import the pygame module
import pygame, sys, os

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import*

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf =  pygame.transform.scale(pygame.image.load("jet kopyası.png").convert(),(40,40))
        
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.y = 600
        self.rect.x = 800
    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()


        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf =  pygame.transform.scale(pygame.image.load("jet.png").convert(),(40,40))
        
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        
        

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super(Enemy, self).__init__()
        if x == player2.rect:
         self.surf = pygame.image.load("missile kopyası.png").convert()
         self.surf.set_colorkey((255, 255, 255), RLEACCEL)
         self.rect = self.surf.get_rect()
         self.rect.y = x.y + 30
         self.rect.x = x.x + 30
         self.speed = 20
        if x == player.rect:
         self.surf = pygame.image.load("missile.png").convert()
         self.surf.set_colorkey((255, 255, 255), RLEACCEL)
         self.rect = self.surf.get_rect()
         self.rect.y = x.y
         self.rect.x = x.x
         self.speed = -20

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Cloud(pygame.sprite.Sprite):
     def __init__(self):
         super(Cloud, self).__init__()
         self.surf = pygame.image.load("cloud.png").convert()
         self.surf.set_colorkey((0, 0, 0), RLEACCEL)
         # The starting position is randomly generated
         self.rect = self.surf.get_rect(
             center=(
                 random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                 random.randint(0, SCREEN_HEIGHT),
             )
         )
 
     # Move the cloud based on a constant speed
     # Remove the cloud when it passes the left edge of the screen
     def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.key.set_repeat()
pygame.mixer.init()


# scores
score1 = 0
score2 = 0
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)
font = pygame.font.Font('Roboto-Black.ttf', 18)
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
# Create our 'player'
player = Player()
player2 = Player2()
# Create groups to hold enemy sprites, and every sprite
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player2)
clouds = pygame.sprite.Group()
all_sprites.add(clouds)
# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    score_text = font.render(f'PLAYER1: {score1}', True, (0, 0, 0))
    score_text1 = font.render(f'PLAYER2: {score2}', True, (0, 0, 0))
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
             new_enemy = Enemy(player.rect)
             enemies.add(new_enemy)
             all_sprites.add(new_enemy)
        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False
            
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
       
        elif event.type == KEYUP:
         if event.key == K_d:
            new_enemy = Enemy(player2.rect)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player2.update(pressed_keys)
    clouds.update()
    # Update the position of our enemies
    enemies.update()

    # Fill the screen with black
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        score1 += 1/2
        collision_sound.play()
        
        if score1 == 4 or score2 == 4 :
         player.kill()
         player2.kill()
         move_up_sound.stop()
         move_down_sound.stop()
         running = False
    
    elif pygame.sprite.spritecollideany(player2, enemies):
        # If so, remove the player and stop the loop
        score2 += 1/2
        collision_sound.play()
        if score1 == 4 or score2 == 4 :
         player.kill()
         player2.kill()
         move_up_sound.stop()
         move_down_sound.stop()
         running = False

    screen.blit(score_text, (SCREEN_WIDTH/2 -130, 0))
    screen.blit(score_text1, (SCREEN_WIDTH/2 , 0))
    print()
    # Flip everything to the display
    pygame.display.flip()
    clock.tick(34)
