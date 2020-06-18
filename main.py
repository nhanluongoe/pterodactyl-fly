import pygame
import os
import time
import random
import math

WIDTH, HEIGHT = 1000, 500
SIZE = WIDTH, HEIGHT

# Load images
player_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fly-1.png")), (70, 70))
player_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fly-2.png")), (70, 70))

t_rex_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "t-rex-1.png")), (100, 100))
t_rex_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "t-rex-2.png")), (100, 100))

cloud_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "cloud-1.png")), (50, 50))
cloud_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "cloud-2.png")), (50, 50))
cloud_img_3 = pygame.transform.scale(pygame.image.load(os.path.join("images", "cloud-3.png")), (50, 50))

rocket_img = pygame.transform.scale(pygame.image.load(os.path.join("images", "rocket.png")), (100, 52))

tree_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tree-1.png")), (100, 100))
tree_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tree-2.png")), (100, 100))
tree_img_3 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tree-3.png")), (100, 100))





road_img = pygame.transform.scale(pygame.image.load(os.path.join("images", "road.png")), (2*WIDTH, int(HEIGHT/2)))

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = []
        self.animation = True # flag for swap image to create animation effect
        self.velocity = 5

    def render(self, screen):
        if self.animation:
            screen.blit(self.img[0], (self.x, self.y))
            self.animation = not self.animation
        else:
            screen.blit(self.img[1], (self.x, self.y))
            self.animation = not self.animation

    def move(self):
        self.x -= self.velocity

class Player(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [player_img_1, player_img_2]

    def jump(self):
        self.y -= 10
    
    def drown(self):
        self.y += 3

class Trex(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [t_rex_img_1, t_rex_img_2]
        self.velocity = 7


class Cloud(Object):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.img = img

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Tree(Cloud):
    def __init(self, x, y):
        super().__init__(x, y)


class Rocket(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = rocket_img
        self.velocity = 10

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Road:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = road_img
        self.velocity = 5

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= self.velocity


def main():
    run = True
    fps = 120
    score = 0
    clock = pygame.time.Clock()

    player = Player(50, 360)
    t_rexs = [Trex(WIDTH - t_rex_img_1.get_width() - 20, 340)]
    clouds = [
        Cloud(WIDTH - cloud_img_1.get_width() - 600, 20, cloud_img_1),
        Cloud(WIDTH - cloud_img_1.get_width() - 20, 40, cloud_img_2),
        Cloud(WIDTH - cloud_img_1.get_width() - 250, 80, cloud_img_3),
        Cloud(WIDTH - cloud_img_1.get_width() - 400, 120, cloud_img_1)
    ]
    roads = [Road(0, 240)]
    rockets = [
        Rocket(2*WIDTH, 40)
    ]
    trees = [
        Tree(WIDTH, 330, tree_img_1),
        Tree(WIDTH * 1.2, 330, tree_img_2),
        Tree(WIDTH * 2.3, 330, tree_img_3)
    ]

    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Jumping T-Rex")

    # Initialize font
    pygame.font.init()
    score_font = pygame.font.SysFont("pixel", 40)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    def on_render():
        # render background
        screen.blit(background, (0, 0))

        # render label
        score_label = score_font.render("Score: {}".format(math.floor(score)), 1, (0, 0, 0))
        screen.blit(score_label, (WIDTH*2, 10))

        # render infinity road
        for road in roads:
            road.render(screen)
        
        # render trees
        for tree in trees:
            tree.render(screen)

        # render clouds
        for cloud in clouds:
            cloud.render(screen)

        # render t-rex
        for t_rex in t_rexs:
            t_rex.render(screen)

        # render player
        player.render(screen)

        # render rocket
        for rocket in rockets:
            rocket.render(screen)

        

        pygame.display.update()

    # Event loop
    while run:
        clock.tick(fps)
        on_render()

        score += 0.2

        for t_rex in t_rexs:
            t_rex.move()
            if t_rex.x < -10:
                t_rex.x = WIDTH*random.randrange(1, 3)

        for cloud in clouds:
            cloud.move()
            if cloud.x < - 10:
                cloud.x = WIDTH*random.randrange(1, 5)

        for rocket in rockets:
            rocket.move()
            if rocket.x < - 10:
                rocket.x = WIDTH*random.randrange(1, 5)
                rocket.y = random.randrange(20, 360)
                rocket.velocity = random.randrange(6, 15)

        for tree in trees:
            tree.move()
            if tree.x < -10:
                tree.x = WIDTH * random.randrange(1, 3)

        for road in roads:
            road.move()
            if road.x == -WIDTH:
                roads.append(Road(WIDTH, 240))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys =  pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and player.y < 360:
            player.y += 8
        if keys[pygame.K_SPACE] and player.y > 0:
            player.jump()
        if (not keys[pygame.K_SPACE]) and (not keys[pygame.K_DOWN]) and player.y < 360:
            player.drown()    

if __name__ == '__main__':
    main()