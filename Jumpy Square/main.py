# Jumpy Square

import pygame
import sys
from random import randint


# Functions
def window():
    global run
    global speed

    screen.fill((0, 0, 0))
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()


def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, False, color)
    text_rect = text_object.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_object, text_rect)


def main_menu():
    global high_score
    global highscore_file

    def start_game():
        global play
        global vely
        global score

        global color1
        global color2
        global color3

        play = True
        score = 0

        vely = 0
        player_rect.x, player_rect.y = 100, 300
        obstacle1_rect.x = 800
        obstacle2_rect.x = 800 + (1 / 3 * 880)
        obstacle3_rect.x = 800 + (2 / 3 * 880)

        obstacle1_rect.y = randint(-400, -100)
        obstacle2_rect.y = randint(-400, -100)
        obstacle3_rect.y = randint(-400, -100)

        color1 = (randint(0, 200), randint(50, 100), randint(100, 200), 255)
        color2 = (randint(100, 200), randint(0, 200), randint(50, 100), 255)
        color3 = (randint(50, 100), randint(100, 200), randint(0, 200), 255)

        draw_text(str(score), font, (255, 255, 255), screen, 400, 50)

    draw_text('Jumpy Square!', font, (255, 255, 255), screen, 400, 50)
    draw_text('Press Enter to Begin', font, (255, 255, 255), screen, 400, 300)
    draw_text('Last Score: ' + str(score), font, (255, 255, 255), screen, 400,
              450)
    draw_text('High Score: ' + str(high_score), font, (255, 255, 255), screen,
              400, 500)

    if score > int(high_score):
        high_score = score
        highscore_file = open('highscore.txt', 'w')
        highscore_file.write(str(high_score))

    if (userInput[pygame.K_RETURN]
            or pygame.mouse.get_pressed()[0]) and not play:
        start_game()


def play_game():
    global play
    global score
    global vely
    global color1
    global color2
    global color3
    global speed

    vely += 0.8
    player_rect.y += vely
    if userInput[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        vely = -10

    angle = -3 * vely
    if angle < -80:
        angle = -80

    if obstacle1_rect.x < -80:
        obstacle1_rect.x = 800
        obstacle1_rect.y = randint(-400, -100)
        color1 = (randint(100, 200), randint(100, 200), randint(100, 200), 255)
    elif obstacle2_rect.x < -80:
        obstacle2_rect.x = 800
        obstacle2_rect.y = randint(-400, -100)
        color2 = (randint(100, 200), randint(100, 200), randint(100, 200), 255)
    elif obstacle3_rect.x < -80:
        obstacle3_rect.x = 800
        obstacle3_rect.y = randint(-400, -100)
        color3 = (randint(100, 200), randint(100, 200), randint(100, 200), 255)

    obstacle1_rect.x -= 5
    obstacle2_rect.x -= 5
    obstacle3_rect.x -= 5

    hitbox_overlap1 = player_mask.overlap_mask(
        obstacle1_mask,
        (obstacle1_rect.x - player_rect.x, obstacle1_rect.y - player_rect.y))
    hitbox_overlap2 = player_mask.overlap_mask(
        obstacle2_mask,
        (obstacle2_rect.x - player_rect.x, obstacle2_rect.y - player_rect.y))
    hitbox_overlap3 = player_mask.overlap_mask(
        obstacle3_mask,
        (obstacle3_rect.x - player_rect.x, obstacle3_rect.y - player_rect.y))

    if hitbox_overlap1.count() > 0 or hitbox_overlap2.count(
    ) > 0 or hitbox_overlap3.count() > 0 or player_rect.y > 600:
        play = False
    if player_rect.y < 0:
        player_rect.y = 0

    if obstacle1_rect.centerx == 100 or obstacle2_rect.centerx in [
            100, 98
    ] or obstacle3_rect.centerx in [100, 96]:
        score += 1

        speed += 0.125

    screen.blit(
        obstacle1_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=color1),
        obstacle1_rect)
    screen.blit(
        obstacle2_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=color2),
        obstacle2_rect)
    screen.blit(
        obstacle3_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=color3),
        obstacle3_rect)
    screen.blit(pygame.transform.rotate(player, angle),
                (player_rect.x - 2, player_rect.y - 2))
    draw_text(str(score), font, (255, 255, 255), screen, 400, 50)


# Main
pygame.init()

highscore_file = open('highscore.txt', 'r')

icon = pygame.image.load('assets/icon.png')
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Jumpy Square!')
pygame.display.set_icon(icon)

font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 32)
clock = pygame.time.Clock()

player = pygame.image.load('assets/square.png')
player.set_colorkey((0, 0, 0))
obstacle = pygame.image.load('assets/obstacle.png')
obstacle.set_colorkey((0, 0, 0))

player = pygame.transform.scale(player, (25, 25))
obstacle = pygame.transform.scale(obstacle, (80, 1200))

player_rect = player.get_rect()
obstacle1_rect = obstacle.get_rect()
obstacle2_rect = obstacle.get_rect()
obstacle3_rect = obstacle.get_rect()

player_mask = pygame.mask.from_surface(player)
obstacle1_mask = pygame.mask.from_surface(obstacle)
obstacle2_mask = pygame.mask.from_surface(obstacle)
obstacle3_mask = pygame.mask.from_surface(obstacle)

vely = 0

color1 = None
color2 = None
color3 = None

score = 0
high_score = highscore_file.readline()

play = False
run = True
speed = 30
while run:
    window()

    userInput = pygame.key.get_pressed()

    if play:
        play_game()
    else:
        main_menu()

    pygame.display.update()
