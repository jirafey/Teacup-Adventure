import pygame, os, csv
from sys import exit

pygame.init()
running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Teapot Adventure")

player_rect = pygame.rect.Rect(0, 40, 100, 100)
velocity = 7
gravity = 10
jump_force = 20

tea_rect = pygame.rect.Rect(player_rect.left + 15, player_rect.top - 15, 20, 15)


def move(vel):
    global keys

    if keys[pygame.K_d]:
        player_rect.x += vel
    if keys[pygame.K_a]:
        player_rect.x -= vel


def jump(force):
    global gravity
    gravity = -(force)


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running == False
                exit()
            if e.key == pygame.K_SPACE or e.key == pygame.K_w:
                if player_rect.y >= 980:
                    jump(jump_force)

    keys = pygame.key.get_pressed()

    if player_rect.bottom > 1080:
        player_rect.bottom = 1080

    gravity += 1
    if gravity >= 10:
        gravity = 10

    move(velocity)
    player_rect.y += gravity

    screen.fill("white")
    pygame.draw.rect(screen, "black", player_rect)

    pygame.display.update()
    clock.tick(60)
