import pygame, os, csv
from sys import exit

pygame.init()
running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Teapot Adventure")

player_rect = pygame.rect.Rect(0,40,100,100)
velocity = 7
gravity = 10
jump_force = 20
spill_force = 35
s_gravity = 10
s_vel = 0

state = "game"

spilled = False

tea_rect = pygame.rect.Rect(player_rect.left + 30, player_rect.top - 30, 40, 30)

font = pygame.font.Font(os.path.join("Assets", "font.otf"), 128)
font1 = pygame.font.Font(os.path.join("Assets", "font.otf"), 64)
die_txt = font.render("You Died!", False, "Black")
die_txt1 = font1.render("Press Q to respawn", False, "Black")

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
            if state == "game":
                if e.key == pygame.K_SPACE or e.key == pygame.K_w:
                    if player_rect.y >= 980 and spilled == False:
                        jump(jump_force)
                        spilled = True
                        s_gravity = -(spill_force)
                        if keys[pygame.K_a]:
                            s_vel -= 5
                        if keys[pygame.K_d]:
                            s_vel += 5
            if state == "dead":
                if e.key == pygame.K_q:
                    player_rect.x = 0
                    player_rect.y = 40
                    spilled = False
                    tea_rect.x, tea_rect.y = player_rect.left + 30, player_rect.top - 30
                    s_vel = 0
                    state = "game"

    keys = pygame.key.get_pressed()

    if state == "game":
        if player_rect.bottom > 1080:
            player_rect.bottom = 1080
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > 1920:
            player_rect.right = 1920

        if spilled == False:
            tea_rect.x, tea_rect.y = player_rect.left + 30, player_rect.top - 30
        if tea_rect.left < 0:
            tea_rect.left = 0
        if tea_rect.right > 1920:
            tea_rect.right = 1920
        
        gravity += 1
        if gravity >= 10:
            gravity = 10
        
        s_gravity += 1
        if s_gravity >= 10:
            s_gravity = 10

        move(velocity)
        player_rect.y += gravity

        screen.fill("white")

        if spilled:
            if s_vel > 0:
                s_vel -= 0.005
            if s_vel < 0:
                s_vel += 0.005
            pygame.draw.rect(screen, "brown", tea_rect)
            tea_rect.y += s_gravity
            tea_rect.x += s_vel
            if tea_rect.colliderect(player_rect):
                s_vel = 0
                spilled = False
            if tea_rect.y >= 1080:
                tea_rect.y = 1080
                state = "dead"


        pygame.draw.rect(screen, "black", player_rect)

    if state == "dead":
        screen.blit(die_txt, (960 - die_txt.get_width() / 2, 540 - die_txt.get_height() / 2))
        screen.blit(die_txt1, (960 - die_txt1.get_width() / 2, 800))

    pygame.display.update()
    clock.tick(60)
