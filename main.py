import pygame
import sys
from pygame.locals import *
from random import randint
import time

pygame.init()

# list of colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong by Michael Dimapindan")


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:     # prevents from paddle going off-screen
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:   # prevents from paddle going off-screen
            self.rect.y = 400


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)


paddle_sound = pygame.mixer.Sound('paddle_ping.wav')
wall_bounce = pygame.mixer.Sound('wall_bounce.wav')
score_sound = pygame.mixer.Sound('miss_sound.wav')

# position of player 1
p1_obj = Paddle(WHITE, 10, 100)
p1_obj.rect.x = 0
p1_obj.rect.y = 200
# position of player 2
p2_obj = Paddle(WHITE, 10, 100)
p2_obj.rect.x = 690
p2_obj.rect.y = 200

ball = Ball(WHITE, 10, 10)

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(p1_obj)
all_sprites_list.add(p2_obj)
all_sprites_list.add(ball)

in_progress = True
timer = pygame.time.Clock()

p1_score = 0
p2_score = 0

# main game loop
while in_progress:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

    keys_input = pygame.key.get_pressed()
    if keys_input[pygame.K_w]:
        p1_obj.move_up(5)
    if keys_input[pygame.K_s]:
        p1_obj.move_down(5)
    if keys_input[pygame.K_UP]:
        p2_obj.move_up(5)
    if keys_input[pygame.K_DOWN]:
        p2_obj.move_down(5)

    all_sprites_list.update()

    if ball.rect.x >= 690:
        score_sound.play()
        p1_score = p1_score + 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        score_sound.play()
        p2_score = p2_score + 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        wall_bounce.play()
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        wall_bounce.play()
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, p1_obj) or pygame.sprite.collide_mask(ball, p2_obj):
        ball.bounce()
        paddle_sound.play()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    text_font = pygame.font.Font(None, 45)

    # score text
    text = font.render(str(p1_score), 1, WHITE)
    screen.blit(text, (250, 10))
    text = text_font.render("P1", True, WHITE)
    screen.blit(text, (245, 60))
    text = font.render(str(p2_score), 1, WHITE)
    screen.blit(text, (420, 10))
    text = text_font.render("P2", True, WHITE)
    screen.blit(text, (415, 60))
    win_text = text_font.render("Wins", True, WHITE)

    # instructions
    text = text_font.render("W", True, WHITE)
    screen.blit(text, (305, 420))
    text = text_font.render("S", True, WHITE)
    screen.blit(text, (310, 460))
    text = text_font.render("UP", True, WHITE)
    screen.blit(text, (365, 420))
    text = text_font.render("DOWN", True, WHITE)
    screen.blit(text, (365, 460))

    if p1_score == 3:
        screen.blit(win_text, (228, 100))
        time.sleep(3)
        in_progress = False
    elif p2_score == 3:
        screen.blit(win_text, (398, 100))
        time.sleep(3)
        in_progress = False

    pygame.display.flip()

    timer.tick(60)

pygame.quit()
