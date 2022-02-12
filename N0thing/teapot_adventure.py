from calendar import c
import pygame, os, csv
from sys import exit

pygame.init()
running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Teapot Adventure")

player_rect = pygame.rect.Rect(0,40,100,100)

#some important values
velocity = 7
gravity = 10
jump_force = 20
spill_force = 35
s_gravity = 10
s_vel = 0

ground_y = 1080

current_lv = "tut1"

state = "menu"

spilled = False

tea_rect = pygame.rect.Rect(player_rect.left + 30, player_rect.top - 30, 40, 30)

font = pygame.font.Font(os.path.join("Assets", "font.otf"), 128)
font1 = pygame.font.Font(os.path.join("Assets", "font.otf"), 64)
die_txt = font.render("You Died!", False, "Black")
die_txt1 = font1.render("Press Q to respawn", False, "Black")

menu_txt = pygame.transform.rotate(font.render("Teapot Adventure", False, "Black"), -4)
start_txt = font1.render("START", False, "black")

start_rect = pygame.rect.Rect(960 - start_txt.get_width() / 2, 760, start_txt.get_width() + 40, start_txt.get_height() + 20)

start_button_color = "pink"

def move(vel):
    global keys

    if keys[pygame.K_d]:
        player_rect.x += vel
    if keys[pygame.K_a]:
        player_rect.x -= vel

def jump(force):
    player_rect.y -= 1
    global gravity
    gravity = -(force)

#making map

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 64
        self.start_x, self.start_y = 0,0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                   tiles.append(Tile(os.path.join("Assets","tile", "grass64.png"), x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "1":
                   tiles.append(Tile(os.path.join("Assets","tile", "ground64.png"), x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def collide(self, rect):
        global ground_y
        for tile in self.tiles:
            if tile.rect.colliderect(rect):
                if rect.right <= tile.rect.left:
                    rect.right = tile.rect.left

                elif rect.left >= tile.rect.right:
                    rect.left = tile.rect.right

                elif rect.bottom >= tile.rect.top:
                    ground_y = tile.rect.top
                    rect.y -= rect.bottom - tile.rect.top

                elif rect.top <= tile.rect.bottom:
                    rect.y = tile.rect.bottom

                else:
                    ground_y = 1080

tut_lv1 = TileMap(os.path.join("Assets", "worlds", "tutlv_1.csv"), os.path.join("Assets", "tile", "ground_tileset.png"))
tut_lv2 = TileMap(os.path.join("Assets", "worlds", "tutlv_2.csv"), os.path.join("Assets", "tile", "ground_tileset.png"))

def to_next_level(current, rect):
    pass

#Actual gameloop
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN and state == "menu":
            if start_rect.collidepoint(mouse_pos):
                state = "game"

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running == False
                exit()
                    
            #jumping and making the spill
            if state == "game":
                if e.key == pygame.K_SPACE or e.key == pygame.K_w:
                    if player_rect.bottom >= ground_y and spilled == False:
                        jump(jump_force)
                        spilled = True
                        s_gravity = -(spill_force)
                        if keys[pygame.K_a]:
                            s_vel -= 5
                        if keys[pygame.K_d]:
                            s_vel += 5
                
            #respawn
            if state == "dead":
                if e.key == pygame.K_q:
                    player_rect.x = 0
                    player_rect.y = 40
                    spilled = False
                    tea_rect.x, tea_rect.y = player_rect.left + 30, player_rect.top - 30
                    s_vel = 0
                    state = "game"

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    #menu
    if state == "menu":
        screen.fill("lightblue")
        screen.blit(menu_txt, (960 - menu_txt.get_width() / 2.5, 100))
        pygame.draw.rect(screen, start_button_color, start_rect)
        screen.blit(start_txt, (start_rect.x + 20, start_rect.y + 10))
        if start_rect.collidepoint(mouse_pos):
            start_button_color = "red"
                
        else:
            start_button_color = "pink"
        

    if state == "game":
        if player_rect.bottom > 1080:            
            player_rect.bottom = 1080
        if player_rect.left <= 0:
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

       
        tut_lv1.draw_map(screen)
        tut_lv1.collide(player_rect)
        
        #some more stuff to the spill
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
