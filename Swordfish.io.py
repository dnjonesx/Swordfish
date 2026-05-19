#Swordfish OOP

#General game stuff
import os
os.environ['PYGAME_DETECT_AVX2'] = '1'
import pygame
import sys
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.init()
pygame.font.init()

score = 0
font = pygame.font.Font(None, 35)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60
end_game = 100000000000000

background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (750, 750))

class Swordfish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Image stuff
        self.raw_image = pygame.image.load('swordfish.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (100, 100))
        self.image = self.original_image.copy()

        #Positional stuff
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.alive = True
        self.current_angle = 0

        #Hitboxes
        self.hitbox = self.rect.inflate(-60, -60)
        self.sword_hitbox = pygame.Rect(0, 0, 30, 30)

        #Diagonals
        d1_straight = 25
        d1_diag = 15
        self.offsets1 = {
            0: (d1_straight, 0), 45: (d1_diag, -d1_diag), 90: (0, -d1_straight),
            135: (-d1_diag, -d1_diag), 180: (-d1_straight, 0), 225: (-d1_diag, d1_diag),
            270: (0, d1_straight), 315: (d1_diag, d1_diag)
        }
        d2_straight = -35
        d2_diag = -25
        self.offsets2 = {
            0: (d2_straight, 0), 45: (d2_diag, -d2_diag), 90: (0, -d2_straight),
            135: (-d2_diag, -d2_diag), 180: (-d2_straight, 0), 225: (-d2_diag, d2_diag),
            270: (0, d2_straight), 315: (d2_diag, d2_diag)
        }

    #Non-constants
    def update(self):

        #Movement
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:    move_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  move_y = self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  move_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: move_x = self.speed
        
        self.rect.x += move_x
        self.rect.y += move_y
        
        if move_x > 0 and move_y == 0:    self.current_angle = 180
        elif move_x > 0 and move_y < 0:  self.current_angle = 225
        elif move_x == 0 and move_y < 0:  self.current_angle = 270
        elif move_x < 0 and move_y < 0:  self.current_angle = 315
        elif move_x < 0 and move_y == 0:  self.current_angle = 0
        elif move_x < 0 and move_y > 0:  self.current_angle = 45
        elif move_x == 0 and move_y > 0:  self.current_angle = 90
        elif move_x > 0 and move_y > 0:  self.current_angle = 135

        #Update after movement
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.hitbox.center = self.rect.center
        off1 = self.offsets1[self.current_angle]
        off2 = self.offsets2[self.current_angle]
        self.sword_hitbox.centerx = self.rect.centerx + off1[0] + off2[0]
        self.sword_hitbox.centery = self.rect.centery + off1[1] + off2[1]
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

player = Swordfish()
player_group = pygame.sprite.GroupSingle(player)

#Shark
class Shark(pygame.sprite.Sprite):
    def __init__(self, image, interval):
        super().__init__()

        #Image stuff
        self.raw_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (125, 125))
        self.image = self.original_image.copy()

        #Positional stuff
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(50, 700), random.uniform(50, 700))
        self.interval = interval
        self.timer = 0
        self.time = 0
        self.alive = True
        self.hitbox = self.rect.inflate(-50, -50)
        self.change_x = 0
        self.change_y = 0
        self.current_angle = 0

    #Non-Constants
    def update(self, score):

        #Movement
        if score >= 30: shark_speed = [-7, -6, -5, -4, 0, 4, 5, 6, 7]
        elif score >= 25: shark_speed = [-6, -5, -4, -3, 0, 3, 4, 5, 6]
        elif score >= 20: shark_speed = [-5, -4, -3, 0, 3, 4, 5]
        elif score >= 15: shark_speed = [-5, -4, -3, -2, 0, 2, 3, 4, 5]
        elif score >= 10: shark_speed = [-4, -3, -2, 0, 2, 3, 4]
        elif score >= 5: shark_speed = [-3, -2, -1, 0, 1, 2, 3]
        else: shark_speed = [-2, -1, 0, 1, 2]

        self.timer +=1
        if self.timer >= self.interval:
            self.change_x = random.choice(shark_speed)
            self.change_y = random.choice(shark_speed)
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.left < -25:
            self.rect.left = -25
            self.change_x *= -1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.change_x *= -1

        if self.rect.top < -25:
            self.rect.top = -25
            self.change_y *= -1
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y *= -1

        if self.change_y > 0 and self.change_x == 0: self.current_angle = 90
        elif self.change_y == 0 and self.change_x > 0: self.current_angle = 180
        elif self.change_y == 0 and self.change_x < 0: self.current_angle = 0
        elif self.change_y < 0 and self.change_x == 0: self.current_angle = 270
        elif self.change_y > 0 and self.change_x > 0: self.current_angle = 135
        elif self.change_y < 0 and self.change_x < 0: self.current_angle = 315
        elif self.change_y > 0 and self.change_x < 0: self.current_angle = 45
        elif self.change_y < 0 and self.change_x > 0: self.current_angle = 225
        elif self.change_y == 0 and self.change_x == 0: self.current_angle = 0

        #Update after movement
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.hitbox.center = self.rect.center

shark = Shark("shark.png", 60)
shark_group = pygame.sprite.GroupSingle(shark)

class Fish(pygame.sprite.Sprite):
    def __init__(self, color, image, interval):
        super().__init__()

        #Image stuff
        self.raw_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (75, 75))
        self.image = self.original_image.copy()

        #Positional stuff
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(50, 700), random.uniform(50, 700))
        self.color = color
        self.interval = interval
        self.timer = 0
        self.time = 0
        self.alive = True
        self.hitbox = self.rect.inflate(-20, -20)
        self.change_x = 0
        self.change_y = 0
        self.current_angle = 0

    #Non-Constants
    def update(self, score):
        
        #Movement
        if score >= 40: fish_speed = [-6, -5, -4, -3, -2, 0, 2, 3, 4, 5, 6]
        elif score >= 30: fish_speed = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        elif score >= 20: fish_speed = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        else: fish_speed = [-2, -1, 0, 1, 2,]

        self.timer +=1
        if self.timer >= self.interval:
            self.change_x = random.choice(fish_speed)
            self.change_y = random.choice(fish_speed)
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.left < -25:
            self.rect.left = -25
            self.change_x *= -1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.change_x *= -1

        if self.rect.top < -25:
            self.rect.top = -25
            self.change_y *= -1
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y *= -1

        if self.change_y > 0 and self.change_x == 0: self.current_angle = 90
        elif self.change_y == 0 and self.change_x > 0: self.current_angle = 180
        elif self.change_y == 0 and self.change_x < 0: self.current_angle = 0
        elif self.change_y < 0 and self.change_x == 0: self.current_angle = 270
        elif self.change_y > 0 and self.change_x > 0: self.current_angle = 135
        elif self.change_y < 0 and self.change_x < 0: self.current_angle = 315
        elif self.change_y > 0 and self.change_x < 0: self.current_angle = 45
        elif self.change_y < 0 and self.change_x > 0: self.current_angle = 225
        elif self.change_y == 0 and self.change_x == 0: self.current_angle = 0

        #Update after movement
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.hitbox.center = self.rect.center

fish_colors = [
    ("green", "green_fish.png"),
    ("yellow", "yellow_fish.png"),
    ("orange", "orange_fish.png"),
    ("red", "red_fish.png")
]

all_fish = pygame.sprite.Group()
master_fish_list = []

for color, img in fish_colors:
    new_fish = Fish(color, img, random.choice([35, 40, 45, 50, 55, 60]))
    all_fish.add(new_fish)
    master_fish_list.append(new_fish)

#While loop!
running = True
while running:
    #Keep the game operating stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = current_time
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    #Keep everything updated
    player_group.update()
    all_fish.update(score)
    shark_group.update(score)

    #Revive
    if shark.alive == False and current_time - shark.time > 3000:
        shark.alive = True
        shark_group.add(shark)
    
    for fish in master_fish_list:
        if fish.alive == False and current_time - fish.time > 20000:
                fish.alive = True
                all_fish.add(fish)
    
    #Collisions
    if shark.alive and player.alive and player.sword_hitbox.colliderect(shark.hitbox):
        shark.alive = False
        shark.time = current_time
        score += 1
    for fish in all_fish:
        if shark.alive and fish.alive and shark.hitbox.colliderect(fish.hitbox):
            fish.alive = False
            fish.kill()
            fish.time = current_time
    if player.alive and player.hitbox.colliderect(shark.hitbox) and shark.alive:
        player.alive = False
        player.kill()
        end_game = current_time
    for fish in all_fish:
        if fish.alive and player.alive and player.hitbox.colliderect(fish.hitbox):
            fish.alive = False
            fish.kill()
            fish.time = current_time
            score -= random.choice([1,2,3,4])

    #Fish importance
    if len(all_fish) == 0 and player.alive:
        end_game = current_time
    if len(all_fish) == 0:
        player.alive = False
        player.kill()

    #Actually render the game
    screen.blit(background_image, (0, 0))
    for fish in all_fish:
        if fish.alive: screen.blit(fish.image, fish.rect)
    if shark.alive: screen.blit(shark.image, shark.rect)
    player_group.draw(screen)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    if end_game > current_time:
        screen.blit(score_text, (10, 10))
    else:
        screen.blit(score_text, (SCREEN_HEIGHT // 2 - 60, SCREEN_WIDTH // 2))

    pygame.display.flip()

    if current_time - 3000 > end_game: running = False

running = False
sys.exit()